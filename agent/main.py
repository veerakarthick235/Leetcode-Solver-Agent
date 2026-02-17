import time
import logging
from browser import Browser
from brain import CodeBrain
from memory import Memory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("🤖 AGENT STARTED: Turbo Java Mode (One Shot | No Waiting)")
    browser = Browser()
    brain = CodeBrain()
    memory = Memory()

    while True:
        try:
            slug = browser.get_current_slug()
            logger.info(f"📍 PROBLEM: {slug}")

            # 1. Skip if already solved
            if memory.is_solved(slug):
                logger.info(f"⏩ {slug} already solved. Skipping.")
                browser.click_next()
                time.sleep(3) # Short pause for page load
                continue

            # 2. Perception
            desc = browser.get_text()
            starter = browser.get_starter_code()
            
            # 3. Generate Solution
            code = brain.generate_solution(desc, starter)
            
            if code:
                logger.info("⚡ Running Code...")
                browser.run_code(code)
                
                # Wait briefly for execution (Java takes 2-4s to compile)
                time.sleep(5)
                
                # 4. Check Result
                status, msg = browser.get_run_result()
                
                if status == "SUCCESS":
                    logger.info("✅ Tests Passed! Submitting...")
                    browser.submit()
                    memory.save(slug, code, "Accepted")
                    logger.info("🏆 Submission Successful!")
                else:
                    # 5. ON FAILURE: Log and Skip Immediately
                    clean_msg = msg.split('\n')[0][:100]
                    logger.warning(f"⚠️ Failed ({clean_msg}). Skipping to next.")
            else:
                logger.error("❌ Brain failed to generate code.")

            # 6. Navigation (Immediate)
            logger.info("➡️ Moving to next...")
            if not browser.click_next():
                logger.warning("⚠️ Navigation stuck. Refreshing...")
                browser.refresh()
                time.sleep(5)
                if not browser.click_next():
                    browser.driver.get("https://leetcode.com/problemset/all/")
                    time.sleep(8)
            
            # Tiny buffer to let the next page start loading
            time.sleep(3)

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
