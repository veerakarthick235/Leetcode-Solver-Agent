import os
import requests
import re
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class CodeBrain:
    def __init__(self):
        self.api_key = os.getenv("BYTEZ_API_KEY", "").strip()
        self.url = "https://api.bytez.com/v1/chat/completions"
        self.model = "openai/gpt-4o-mini" 

    def _clean(self, text):
        """Cleans Markdown and ensures valid imports."""
        if not text: return None
        
        # 1. Extract Code
        pattern = r"```java(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches: 
            text = max(matches, key=len).strip()
        else:
            pattern_generic = r"```(.*?)```"
            matches_generic = re.findall(pattern_generic, text, re.DOTALL)
            if matches_generic: 
                text = max(matches_generic, key=len).strip()

        # 2. SANITIZATION (Removed forced 'class Solution' rename)
        # We only remove package declarations
        text = re.sub(r"^\s*package\s+[\w.]+;", "", text, flags=re.MULTILINE)
        
        # 3. FORCE IMPORTS (Crucial for Java)
        imports = "import java.util.*;\nimport java.math.*;\nimport java.io.*;\n"
        if "import java.util" not in text:
            text = imports + text
            
        return text.strip()

    def _query_model(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.0
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                return self._clean(content)
            else:
                logger.error(f"❌ API Error {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Connection Error: {e}")
            return None

    def generate_solution(self, desc, starter_code):
        """Generates a solution matching the Starter Code's class name."""
        prompt = f"""
        ROLE: Java LeetCode Expert.
        TASK: Write a 100% CORRECT Java solution.
        
        RULES:
        1. CLASS NAME: You MUST use the EXACT class name defined in the STARTER CODE below (e.g., 'class Trie', 'class Solution'). Do NOT rename it.
        2. NO MAIN METHOD.
        3. IMPORTS: Assume imports are handled.
        4. NULL SAFETY: Check for nulls.
        5. OUTPUT: Return ONLY the Java code.
        
        PROBLEM:
        {desc}

        STARTER CODE:
        {starter_code}
        """
        return self._query_model([{"role": "user", "content": prompt}])

    def generate_fix(self, desc, bad_code, error_msg):
        """Fixes the Java code."""
        logger.info("🧠 Brain is fixing the Java bug...")
        prompt = f"""
        The previous Java solution failed. Fix the error.
        
        ERROR:
        {error_msg}
        
        FAILED CODE:
        {bad_code}
        
        TASK: Return the CORRECTED Java class code. Keep the same class name.
        """
        return self._query_model([{"role": "user", "content": prompt}])
