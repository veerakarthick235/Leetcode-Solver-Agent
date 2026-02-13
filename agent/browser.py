"""Perception/Action layer for LeetCode Auto-Solver using Selenium"""

import time
import logging
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

from config import SELECTORS, TIMEOUTS, POLLING_INTERVALS

logger = logging.getLogger(__name__)


class LeetCodeBrowser:
    """Selenium-based browser automation for LeetCode UI"""
    
    def __init__(self, debugger_url: str):
        """Connect to existing Chrome instance via DevTools Protocol
        
        Args:
            debugger_url: Chrome DevTools endpoint (e.g., '127.0.0.1:9222')
        """
        self.driver = self._connect_to_chrome(debugger_url)
        logger.info(f"Connected to Chrome at {debugger_url}")
    
    def _connect_to_chrome(self, debugger_url: str) -> webdriver.Chrome:
        """Connect to existing Chrome instance
        
        Args:
            debugger_url: DevTools endpoint
        
        Returns:
            webdriver.Chrome: Connected driver instance
        """
        options = Options()
        options.add_experimental_option("debuggerAddress", debugger_url)
        driver = webdriver.Chrome(options=options)
        return driver
    
    def scrape_problem_description(self, problem_url: str) -> str:
        """Extract problem description from LeetCode problem page
        
        Args:
            problem_url: Full LeetCode problem URL
        
        Returns:
            str: Raw problem description text
        
        Raises:
            TimeoutException: If description not found
        """
        logger.info(f"Navigating to {problem_url}")
        self.driver.get(problem_url)
        
        try:
            # Wait for page load
            wait = WebDriverWait(self.driver, TIMEOUTS["page_load"])
            
            # Try multiple selectors for problem description
            selectors = SELECTORS["problem_description"].split(", ")
            description_element = None
            
            for selector in selectors:
                try:
                    description_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector.strip()))
                    )
                    if description_element:
                        break
                except TimeoutException:
                    continue
            
            if not description_element:
                raise TimeoutException("Could not find problem description")
            
            description = description_element.text
            logger.info(f"Scraped description ({len(description)} chars)")
            return description
            
        except Exception as e:
            logger.error(f"Error scraping description: {e}")
            raise
    
    def inject_code(self, code: str) -> bool:
        """Inject Python code into Monaco editor
        
        Args:
            code: Python solution code (no markdown formatting)
        
        Returns:
            bool: True if injection successful
        """
        try:
            logger.info("Injecting code into editor...")
            
            # Wait for editor to be ready
            wait = WebDriverWait(self.driver, TIMEOUTS["editor_ready"])
            
            # Try to find Monaco editor or textarea
            editor = None
            try:
                editor = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS["monaco_editor"]))
                )
            except TimeoutException:
                # Fallback to textarea
                editor = wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                )
            
            # Click to focus
            editor.click()
            time.sleep(0.5)
            
            # Select all and delete
            editor.send_keys(Keys.CONTROL + "a")
            time.sleep(0.2)
            editor.send_keys(Keys.DELETE)
            time.sleep(0.2)
            
            # Type new code
            editor.send_keys(code)
            time.sleep(0.5)
            
            logger.info("Code injected successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error injecting code: {e}")
            return False
    
    def run_tests(self) -> None:
        """Click 'Run' button to execute test cases
        
        Raises:
            NoSuchElementException: If run button not found
        """
        try:
            logger.info("Clicking Run button...")
            
            # Try multiple selectors for run button
            selectors = SELECTORS["run_button"].split(", ")
            
            for selector in selectors:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    run_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector.strip()))
                    )
                    run_button.click()
                    logger.info("Run button clicked")
                    return
                except (TimeoutException, NoSuchElementException):
                    continue
            
            raise NoSuchElementException("Could not find Run button")
            
        except Exception as e:
            logger.error(f"Error clicking Run button: {e}")
            raise
    
    def get_test_result(self, timeout: int = 30) -> Dict:
        """Poll for test result and parse outcome
        
        Args:
            timeout: Maximum seconds to wait for result
        
        Returns:
            dict: {
                "status": "pass" | "fail" | "timeout",
                "message": str,
                "test_cases": list
            }
        """
        logger.info(f"Waiting for test results (timeout: {timeout}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check for result container
                result_element = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["result_container"])
                
                if result_element and result_element.text:
                    result_text = result_element.text.lower()
                    
                    # Check for success
                    if "accepted" in result_text or "success" in result_text:
                        logger.info("✓ Tests passed!")
                        return {
                            "status": "pass",
                            "message": "All tests passed",
                            "test_cases": []
                        }
                    
                    # Check for failure
                    if "wrong answer" in result_text or "error" in result_text or "fail" in result_text:
                        logger.warning("✗ Tests failed")
                        return {
                            "status": "fail",
                            "message": result_text,
                            "test_cases": [result_text]
                        }
                
            except (NoSuchElementException, StaleElementReferenceException):
                pass
            
            # Poll interval
            time.sleep(POLLING_INTERVALS["result_check"])
        
        # Timeout reached
        logger.warning("Timeout waiting for test results")
        return {
            "status": "timeout",
            "message": "Test execution timeout",
            "test_cases": []
        }
    
    def submit_solution(self) -> bool:
        """Click 'Submit' button to finalize solution
        
        Returns:
            bool: True if submission successful
        """
        try:
            logger.info("Submitting solution...")
            
            # Try multiple selectors for submit button
            selectors = SELECTORS["submit_button"].split(", ")
            
            for selector in selectors:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    submit_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector.strip()))
                    )
                    submit_button.click()
                    logger.info("Submit button clicked")
                    time.sleep(2)  # Wait for submission confirmation
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            logger.warning("Could not find Submit button")
            return False
            
        except Exception as e:
            logger.error(f"Error submitting solution: {e}")
            return False
    
    def close(self):
        """Close browser connection (do not quit Chrome process)"""
        logger.info("Closing browser connection")
        # Don't quit the browser, just disconnect
        # self.driver.quit()  # Commented out to keep Chrome running
