"""Controller layer for LeetCode Auto-Solver Agent

This is the main orchestrator that coordinates browser automation,
AI code generation, and persistent storage to autonomously solve
LeetCode problems.
"""

import asyncio
import logging
import os
import sys
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

from browser import LeetCodeBrowser
from brain import CodeBrain
from memory import MemoryStore
from config import RETRY_CONFIG

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "./logs/solver.log")

os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def extract_problem_slug(url: str) -> str:
    """Extract problem identifier from LeetCode URL
    
    Args:
        url: LeetCode problem URL
    
    Returns:
        str: Problem slug (e.g., 'two-sum')
    
    Examples:
        https://leetcode.com/problems/two-sum/ → 'two-sum'
        https://leetcode.com/problems/add-two-numbers/description/ → 'add-two-numbers'
    """
    match = re.search(r'/problems/([a-z0-9-]+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract problem slug from URL: {url}")


async def solve_problem(
    problem_url: str,
    browser: LeetCodeBrowser,
    brain: CodeBrain,
    memory: MemoryStore,
    max_retries: Optional[int] = None
) -> Dict:
    """Main state machine for solving a single problem
    
    States:
    1. CHECK_HASH: Query memory for existing solution
    2. SCRAPE: Extract problem description from DOM
    3. GENERATE: Call AI to generate solution code
    4. INJECT: Insert code into Monaco editor
    5. RUN_TESTS: Submit and wait for test results
    6. VERIFY: Parse result (pass/fail)
    7. SAVE: Persist to memory
    8. (Optional) RETRY: If failed, regenerate with error context
    
    Args:
        problem_url: LeetCode problem URL
        browser: Browser automation instance
        brain: AI code generation instance
        memory: Persistence layer instance
        max_retries: Maximum retry attempts (default from config)
    
    Returns:
        dict: {"slug": str, "status": str, "code": str, "attempts": int}
    """
    if max_retries is None:
        max_retries = int(os.getenv("MAX_RETRIES", RETRY_CONFIG["max_retries"]))
    
    # Extract slug
    slug = extract_problem_slug(problem_url)
    logger.info(f"\n{'='*60}")
    logger.info(f"Starting to solve: {slug}")
    logger.info(f"{'='*60}")
    
    # STATE 1: CHECK_HASH
    existing = memory.get(slug)
    if existing and existing["status"] == "pass":
        logger.info(f"✓ Problem {slug} already solved. Skipping.")
        return existing
    
    # STATE 2: SCRAPE
    try:
        description = browser.scrape_problem_description(problem_url)
    except Exception as e:
        logger.error(f"Failed to scrape problem: {e}")
        return {"slug": slug, "status": "error", "error": str(e)}
    
    # STATE 3-7: GENERATE, INJECT, RUN_TESTS, VERIFY, SAVE (with retry logic)
    retry_context = None
    
    for attempt in range(1, max_retries + 1):
        logger.info(f"\nAttempt {attempt}/{max_retries}")
        
        try:
            # STATE 3: GENERATE
            code = await brain.generate_solution(description, retry_context)
            logger.info(f"Generated solution:\n{code[:200]}...")
            
            # STATE 4: INJECT
            if not browser.inject_code(code):
                logger.error("Failed to inject code")
                continue
            
            # STATE 5: RUN_TESTS
            browser.run_tests()
            
            # STATE 6: VERIFY
            result_timeout = int(os.getenv("RESULT_TIMEOUT", 30))
            result = browser.get_test_result(timeout=result_timeout)
            
            if result["status"] == "pass":
                # Success!
                logger.info(f"✓ Problem {slug} solved successfully!")
                
                # Submit solution
                browser.submit_solution()
                
                # STATE 7: SAVE
                memory.save(slug, "pass", code, attempts=attempt)
                
                return {
                    "slug": slug,
                    "status": "pass",
                    "code": code,
                    "attempts": attempt
                }
            
            elif result["status"] == "fail":
                # STATE 8: RETRY
                logger.warning(f"Test failed: {result['message'][:200]}")
                retry_context = f"Test failed: {result['message']}\nFailed test cases: {result['test_cases']}"
                
                if attempt < max_retries:
                    logger.info(f"Retrying with error context...")
                    continue
                else:
                    logger.error(f"Max retries reached. Saving failure.")
                    memory.save(slug, "fail", code, attempts=attempt)
                    return {
                        "slug": slug,
                        "status": "fail",
                        "code": code,
                        "attempts": attempt,
                        "error": result["message"]
                    }
            
            elif result["status"] == "timeout":
                logger.warning(f"Test execution timeout")
                memory.save(slug, "timeout", code, attempts=attempt)
                return {
                    "slug": slug,
                    "status": "timeout",
                    "code": code,
                    "attempts": attempt
                }
        
        except Exception as e:
            logger.error(f"Error in attempt {attempt}: {e}")
            if attempt >= max_retries:
                memory.save(slug, "fail", "", attempts=attempt)
                return {
                    "slug": slug,
                    "status": "error",
                    "attempts": attempt,
                    "error": str(e)
                }
    
    # Should not reach here
    return {"slug": slug, "status": "error", "error": "Unknown error"}


async def solve_all_problems(problem_urls: List[str]) -> List[Dict]:
    """Process list of LeetCode problems
    
    Args:
        problem_urls: List of LeetCode problem URLs
    
    Returns:
        list: Results for each problem
    """
    # Initialize components
    chrome_url = os.getenv("CHROME_DEBUGGER_URL", "127.0.0.1:9222")
    api_key = os.getenv("EMERGENT_LLM_KEY")
    memory_file = os.getenv("MEMORY_FILE", "./data/problems.json")
    
    if not api_key:
        raise ValueError("EMERGENT_LLM_KEY not found in environment")
    
    logger.info(f"Initializing LeetCode Auto-Solver...")
    logger.info(f"Chrome: {chrome_url}")
    logger.info(f"Memory: {memory_file}")
    logger.info(f"Problems to solve: {len(problem_urls)}")
    
    browser = LeetCodeBrowser(chrome_url)
    brain = CodeBrain(api_key)
    memory = MemoryStore(memory_file)
    
    results = []
    
    try:
        for i, url in enumerate(problem_urls, 1):
            logger.info(f"\n\n{'#'*60}")
            logger.info(f"Problem {i}/{len(problem_urls)}")
            logger.info(f"{'#'*60}")
            
            try:
                result = await solve_problem(url, browser, brain, memory)
                results.append(result)
                
                status_symbol = {
                    "pass": "✓",
                    "fail": "✗",
                    "timeout": "⏱",
                    "error": "⚠"
                }.get(result.get("status"), "?")
                
                logger.info(f"{status_symbol} {result.get('slug')}: {result.get('status')}")
                
            except KeyboardInterrupt:
                logger.info("\nInterrupted by user. Stopping...")
                break
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                results.append({"url": url, "status": "error", "error": str(e)})
        
        # Print summary
        logger.info(f"\n\n{'='*60}")
        logger.info("SUMMARY")
        logger.info(f"{'='*60}")
        
        stats = memory.get_stats()
        logger.info(f"Total problems attempted: {stats['total']}")
        logger.info(f"Solved: {stats['solved']}")
        logger.info(f"Failed: {stats['failed']}")
        logger.info(f"Timeout: {stats['timeout']}")
        logger.info(f"Success rate: {stats['success_rate']:.1%}")
        
    finally:
        browser.close()
    
    return results


def main():
    """Entry point: Run LeetCode Auto-Solver
    
    Usage:
        python main.py <problem_url_1> <problem_url_2> ...
        
    Example:
        python main.py https://leetcode.com/problems/two-sum/
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <problem_url_1> [problem_url_2] ...")
        print("\nExample:")
        print("  python main.py https://leetcode.com/problems/two-sum/")
        print("  python main.py https://leetcode.com/problems/two-sum/ https://leetcode.com/problems/add-two-numbers/")
        sys.exit(1)
    
    problem_urls = sys.argv[1:]
    
    # Run async solver
    asyncio.run(solve_all_problems(problem_urls))


if __name__ == "__main__":
    main()
