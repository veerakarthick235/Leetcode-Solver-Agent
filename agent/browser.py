import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Browser:
    def __init__(self):
        opts = Options()
        opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(options=opts)

    def get_current_slug(self):
        """Extracts the problem name from the URL"""
        try:
            return self.driver.current_url.split("/problems/")[-1].split("/")[0]
        except:
            return "unknown-problem"

    def optimize_tokens(self, text):
        """
        TOKEN OPTIMIZER: Strips unnecessary HTML and whitespace 
        to maximize Gemini quota efficiency.
        """
        if not text: return ""
        # Remove all HTML tags
        clean_text = re.sub(r'<[^>]*>', '', text)
        # Collapse multiple newlines/spaces into single spaces
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    def get_text(self):
        """Scrapes and optimizes the problem description"""
        try:
            raw_text = self.driver.find_element(By.CSS_SELECTOR, "div[data-track-load='description_content']").text
            return self.optimize_tokens(raw_text)
        except:
            try:
                raw_text = self.driver.find_element(By.TAG_NAME, "body").text
                return self.optimize_tokens(raw_text)
            except:
                return ""

    def get_starter_code(self):
        """Scrapes the default code signature from the Monaco editor"""
        try:
            return self.driver.execute_script("return monaco.editor.getModels()[0].getValue();")
        except:
            return ""

    def run_code(self, code):
        """Injects code safely using Force-Click and Banner-Removal logic"""
        try:
            # 1. Pop-up & Banner Killer: Clears UI elements that intercept clicks
            self.driver.execute_script("""
                var blockers = document.querySelectorAll('.lc-md\\\\:h-8, [class*="overlay"], [class*="tooltip"], .guide-container');
                blockers.forEach(el => el.remove());
            """)
            
            # 2. Force Click: Use JS click to bypass 'ElementClickIntercepted' errors
            try:
                editor_element = self.driver.find_element(By.CLASS_NAME, "view-lines")
                self.driver.execute_script("arguments[0].click();", editor_element)
            except:
                pass # Continue even if click fails, as we use direct injection below
            
            # 3. Monaco Injection
            safe_code = json.dumps(code)
            js_code = f"monaco.editor.getModels()[0].setValue({safe_code});"
            self.driver.execute_script(js_code)
            
            time.sleep(1)
            
            # 4. Click Run
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "Run" in btn.text:
                    self.driver.execute_script("arguments[0].click();", btn)
                    break
        except Exception as e:
            print(f"❌ Browser Injection Error (Handled): {e}")

    def submit(self):
        """Clicks Submit via JavaScript to ensure it isn't blocked"""
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "Submit" in btn.text:
                    self.driver.execute_script("arguments[0].click();", btn)
                    return "Submitted"
            return "Failed"
        except:
            return "Error"

    def click_next(self):
        """Navigates to the next problem"""
        try:
            # Try finding the right-chevron icon
            next_btn = self.driver.find_element(By.XPATH, "//a[contains(@href, '/problems/') and .//*[contains(@data-icon, 'chevron-right')]]")
            self.driver.execute_script("arguments[0].click();", next_btn)
            return True
        except:
            try:
                # Backup: Find by 'Next' text
                next_btn = self.driver.find_element(By.XPATH, "//span[text()='Next']")
                self.driver.execute_script("arguments[0].click();", next_btn)
                return True
            except:
                return False
