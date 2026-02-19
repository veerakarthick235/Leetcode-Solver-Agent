import json
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class Browser:
    def __init__(self):
        opts = Options()
        opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        opts.page_load_strategy = 'eager' 
        self.driver = webdriver.Chrome(options=opts)

    def get_current_slug(self):
        try:
            return self.driver.current_url.split("/problems/")[-1].split("/")[0]
        except:
            return "unknown-problem"

    def get_text(self):
        """Scrapes problem description with AUTO-SCROLL."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.elfjS, div[data-track-load='description_content']"))
            )
            selectors = ["div.elfjS", "div[data-track-load='description_content']", "div.question-content"]
            target_elem = None
            for s in selectors:
                try:
                    target_elem = self.driver.find_element(By.CSS_SELECTOR, s)
                    if target_elem: break
                except: continue

            if target_elem:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", target_elem)
                time.sleep(0.5) 
                return target_elem.text
            return self.driver.find_element(By.TAG_NAME, "body").text[:2000]
        except: return ""

    def get_starter_code(self):
        try:
            return self.driver.execute_script("return monaco.editor.getModels()[0].getValue();")
        except: return ""

    def run_code(self, code):
        try:
            safe_code = json.dumps(code)
            self.driver.execute_script(f"monaco.editor.getModels()[0].setValue({safe_code});")
            
            xpath_selectors = [
                "//button[contains(@data-e2e-locator, 'console-run-button')]",
                "//div[@data-cy='run-code-btn']",
                "//button[contains(text(), 'Run')]"
            ]
            for xpath in xpath_selectors:
                try:
                    btn = WebDriverWait(self.driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    self.driver.execute_script("arguments[0].click();", btn)
                    return True
                except: continue
            return False
        except: return False

    def get_run_result(self):
        """
        Instant check. Returns ('PENDING', ''), ('SUCCESS', '...'), ('FAILURE', '...') or ('UNKNOWN', '')
        Does NOT block. Checks SUCCESS/FAILURE *before* PENDING.
        """
        try:
            # 1. Check for SUCCESS (Priority 1)
            if self.driver.find_elements(By.XPATH, "//*[contains(@class, 'text-green') and contains(text(), 'Accepted')]"):
                return "SUCCESS", "Passed"

            # 2. Check for FAILURE (Priority 2)
            error_keywords = ["Wrong Answer", "Runtime Error", "Compile Error", "Time Limit Exceeded", "Output Limit Exceeded"]
            for err in error_keywords:
                if self.driver.find_elements(By.XPATH, f"//*[contains(@class, 'text-red') and contains(text(), '{err}')]"):
                    # Try to get error details
                    try:
                        details = self.driver.find_element(By.CSS_SELECTOR, "div.whitespace-pre-wrap").text
                        return "FAILURE", f"{err}: {details[:100]}"
                    except:
                        return "FAILURE", err

            # 3. Check for Pending/Running (Priority 3)
            if self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Pending') or contains(text(), 'Running')]"):
                return "PENDING", "Waiting..."

            return "UNKNOWN", ""
        except:
            return "UNKNOWN", "Error"

    def submit(self):
        try:
            xpath_selectors = [
                "//button[contains(@data-e2e-locator, 'console-submit-button')]",
                "//div[@data-cy='submit-code-btn']"
            ]
            for xpath in xpath_selectors:
                try:
                    btn = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    self.driver.execute_script("arguments[0].click();", btn)
                    return True
                except: continue
            return False
        except: return False

    def click_next(self):
        selectors = [
            "nav button[aria-label='Next Question']", 
            "//a[contains(@href, '/problems/') and descendant::*[local-name()='svg' and contains(@data-icon, 'chevron-right')]]"
        ]
        for s in selectors:
            try:
                btn = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, s)))
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except: continue
        return False
        
    def refresh(self):
        self.driver.refresh()
