import os
import requests
import re
import time
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class CodeBrain:
    def __init__(self):
        self.bytez_key = os.getenv("BYTEZ_API_KEY", "").strip()
        # Ensure the URL is the correct base for chat completions
        self.url = "https://api.bytez.com/v1/chat/completions" 
        
        # VERIFIED ALTERNATIVES: Try these one by one if 404 persists
        # 1. deepseek-ai/deepseek-coder-1.3b-instruct (Commonly on free tier)
        # 2. meta-llama/Llama-3.1-8B-Instruct
        self.model = "openai/gpt-4o-mini" 

    def _clean(self, text):
        if not text: return None
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return max(matches, key=len).strip()
        if "class Solution" in text:
            return text[text.find("class Solution"):].strip()
        return text.strip()

    def generate_solution(self, desc, starter_code):
        headers = {
            "Authorization": f"Bearer {self.bytez_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Solve LeetCode in Python. STARTER: {starter_code}\nPROBLEM: {desc}\nRULES: Output ONLY RAW PYTHON 'class Solution:'."
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        try:
            logger.info(f"🚀 Querying Bytez Catalog for: {self.model}...")
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                full_text = response.json()['choices'][0]['message']['content']
                logger.info("✅ Solution received successfully!")
                return self._clean(full_text)
            else:
                logger.error(f"❌ Bytez API Error {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"❌ Connection Error: {e}")
        
        return None
