#!/usr/bin/env python3
"""Test script to verify LeetCode Auto-Solver setup"""

import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_environment():
    """Test environment variables"""
    logger.info("Testing environment configuration...")
    
    required_vars = [
        "CHROME_DEBUGGER_URL",
        "EMERGENT_LLM_KEY",
        "MEMORY_FILE"
    ]
    
    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✓ {var}: {value[:20]}...")
        else:
            logger.error(f"✗ {var}: NOT SET")
            all_ok = False
    
    return all_ok


def test_imports():
    """Test required imports"""
    logger.info("\nTesting imports...")
    
    imports = [
        ("selenium", "selenium"),
        ("dotenv", "python-dotenv"),
        ("emergentintegrations", "emergentintegrations")
    ]
    
    all_ok = True
    for module, package in imports:
        try:
            __import__(module)
            logger.info(f"✓ {package}")
        except ImportError as e:
            logger.error(f"✗ {package}: {e}")
            all_ok = False
    
    return all_ok


def test_chrome_connection():
    """Test Chrome DevTools connection"""
    logger.info("\nTesting Chrome connection...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_url = os.getenv("CHROME_DEBUGGER_URL", "127.0.0.1:9222")
        
        options = Options()
        options.add_experimental_option("debuggerAddress", chrome_url)
        
        driver = webdriver.Chrome(options=options)
        logger.info(f"✓ Connected to Chrome at {chrome_url}")
        logger.info(f"✓ Current URL: {driver.current_url}")
        
        # Don't close - keep browser running
        # driver.quit()
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Chrome connection failed: {e}")
        logger.info("\nTo fix: Launch Chrome with:")
        logger.info("  google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile &")
        return False


def test_file_structure():
    """Test file structure"""
    logger.info("\nTesting file structure...")
    
    required_files = [
        "main.py",
        "browser.py",
        "brain.py",
        "memory.py",
        "config.py",
        ".env",
        "requirements.txt"
    ]
    
    all_ok = True
    for filename in required_files:
        if os.path.exists(filename):
            logger.info(f"✓ {filename}")
        else:
            logger.error(f"✗ {filename}: NOT FOUND")
            all_ok = False
    
    # Check directories
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./logs", exist_ok=True)
    logger.info("✓ data/ directory")
    logger.info("✓ logs/ directory")
    
    return all_ok


async def test_brain():
    """Test Gemini AI integration"""
    logger.info("\nTesting Gemini AI integration...")
    
    try:
        from brain import CodeBrain
        
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            logger.error("✗ EMERGENT_LLM_KEY not set")
            return False
        
        brain = CodeBrain(api_key)
        
        # Test with simple problem
        test_problem = """Write a Python function that returns the sum of two numbers.
        
Function signature:
class Solution:
    def add(self, a: int, b: int) -> int:
"""
        
        logger.info("Generating test solution...")
        code = await brain.generate_solution(test_problem)
        
        if code and "def add" in code:
            logger.info("✓ Gemini API working")
            logger.info(f"Generated code preview: {code[:100]}...")
            return True
        else:
            logger.error("✗ Generated code invalid")
            return False
            
    except Exception as e:
        logger.error(f"✗ Brain test failed: {e}")
        return False


def test_memory():
    """Test memory persistence"""
    logger.info("\nTesting memory persistence...")
    
    try:
        from memory import MemoryStore
        
        memory = MemoryStore("./data/test_problems.json")
        
        # Test save
        memory.save("test-problem", "pass", "def test(): pass", 1)
        logger.info("✓ Memory save")
        
        # Test retrieve
        result = memory.get("test-problem")
        if result and result["status"] == "pass":
            logger.info("✓ Memory retrieve")
        else:
            logger.error("✗ Memory retrieve failed")
            return False
        
        # Test stats
        stats = memory.get_stats()
        logger.info(f"✓ Memory stats: {stats}")
        
        # Cleanup
        os.remove("./data/test_problems.json")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Memory test failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("="*60)
    logger.info("LeetCode Auto-Solver - Setup Test")
    logger.info("="*60)
    
    results = {
        "Environment": test_environment(),
        "Imports": test_imports(),
        "File Structure": test_file_structure(),
        "Memory": test_memory(),
        "Chrome Connection": test_chrome_connection(),
    }
    
    # Skip brain test in basic check (requires API call)
    # Uncomment to test Gemini integration:
    # import asyncio
    # results["Gemini AI"] = asyncio.run(test_brain())
    
    logger.info("\n" + "="*60)
    logger.info("TEST RESULTS")
    logger.info("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✅ All tests passed! System ready.")
        logger.info("\nNext steps:")
        logger.info("1. Ensure Chrome is running with remote debugging")
        logger.info("2. Log in to LeetCode in that Chrome instance")
        logger.info("3. Run: python main.py <leetcode_url>")
        return 0
    else:
        logger.error("\n❌ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
