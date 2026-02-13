"""Intelligence layer for LeetCode Auto-Solver using Gemini-1.5-Flash"""

import asyncio
import logging
import time
from typing import Optional
import sys
import os

# Add parent backend path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger(__name__)


class CodeBrain:
    """Gemini-based AI for generating LeetCode solutions"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini chat client
        
        Args:
            api_key: Emergent LLM key for Gemini access
        """
        self.chat = LlmChat(
            api_key=api_key,
            session_id="leetcode-solver",
            system_message=self._get_system_prompt()
        ).with_model("gemini", "gemini-3-flash-preview")
        
        self.api_calls = 0
        self.call_times = []
        logger.info("CodeBrain initialized with Gemini-3-Flash")
    
    def _get_system_prompt(self) -> str:
        """Define AI behavior for code generation
        
        Returns:
            str: System prompt for Gemini
        """
        return """You are a LeetCode solution generator. Your ONLY job is to write Python code that solves the given problem.

RULES:
1. Output ONLY the function implementation - no markdown, no explanations, no ```python``` tags
2. Use the exact function signature from the problem
3. Do NOT include test cases or example usage
4. Write clean, efficient code with minimal comments
5. Handle edge cases (empty input, single element, None values, etc.)
6. Use proper Python type hints if provided in the problem
7. Follow LeetCode's expected format exactly

Format example:
class Solution:
    def functionName(self, param1: Type, param2: Type) -> ReturnType:
        # Your implementation here
        pass

Remember: Return ONLY the code, nothing else. No explanations before or after.
"""
    
    async def generate_solution(self, problem_description: str, retry_context: Optional[str] = None) -> str:
        """Generate Python solution for LeetCode problem
        
        Args:
            problem_description: Full problem text from LeetCode
            retry_context: Optional error message from failed test (for retry)
        
        Returns:
            str: Raw Python code (no markdown formatting)
        
        Raises:
            Exception: If API call fails
        """
        prompt = self._build_prompt(problem_description, retry_context)
        
        try:
            # Rate limiting check
            await self._enforce_rate_limit()
            
            logger.info("Generating solution with Gemini...")
            user_message = UserMessage(text=prompt)
            response = await self.chat.send_message(user_message)
            
            self.api_calls += 1
            self.call_times.append(time.time())
            
            # Clean response
            code = self._clean_code_response(response)
            logger.info(f"Generated solution ({len(code)} chars)")
            return code
            
        except Exception as e:
            logger.error(f"Error generating solution: {e}")
            raise
    
    def _build_prompt(self, description: str, retry_context: Optional[str] = None) -> str:
        """Construct prompt for AI
        
        Args:
            description: Problem statement
            retry_context: Error message from previous attempt (if retry)
        
        Returns:
            str: Complete prompt for Gemini
        """
        if retry_context:
            return f"""Your previous solution failed with this error:
{retry_context}

Please fix the solution for this problem:
{description}

Remember: Output ONLY raw Python code, no markdown.
"""
        else:
            return f"""Solve this LeetCode problem:
{description}

Output ONLY the Python function implementation. No markdown, no explanations.
"""
    
    def _clean_code_response(self, response: str) -> str:
        """Remove markdown formatting if present
        
        Args:
            response: Raw API response
        
        Returns:
            str: Clean Python code
        """
        code = response.strip()
        
        # Remove markdown code blocks
        if "```python" in code:
            code = code.split("```python", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        elif code.startswith("```"):
            code = code.split("```", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        
        # Remove any trailing markdown
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
    
    async def _enforce_rate_limit(self, max_calls: int = 10, period: int = 60):
        """Enforce rate limiting (10 calls per minute)
        
        Args:
            max_calls: Maximum calls allowed in period
            period: Time window in seconds
        """
        now = time.time()
        
        # Remove calls outside current window
        self.call_times = [t for t in self.call_times if t > now - period]
        
        if len(self.call_times) >= max_calls:
            sleep_time = period - (now - self.call_times[0]) + 1
            logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.1f}s")
            await asyncio.sleep(sleep_time)
