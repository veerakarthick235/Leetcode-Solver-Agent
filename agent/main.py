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

            if memory.is_solved(slug):
                logger.info(f"⏩ {slug} already solved. Skipping.")
                browser.click_next()
                time.sleep(3)
                continue

            desc = browser.get_text()
            starter = browser.get_starter_code()
            
            code = brain.generate_solution(desc, starter)
            
            if code:
                logger.info("⚡ Running Code...")
                browser.run_code(code)
                
                # Smart Poll: Wait up to 10 seconds for a result
                status = "PENDING"
                msg = ""
                for _ in range(50): # 50 * 0.2s = 10s max
                    status, msg = browser.get_run_result()
                    if status in ["SUCCESS", "FAILURE"]:
                        break
                    time.sleep(0.2)
                
                if status == "SUCCESS":
                    logger.info("✅ Tests Passed! Submitting...")
                    browser.submit()
                    memory.save(slug, code, "Accepted")
                    logger.info("🏆 Submission Successful!")
                else:
                    # Skip submit on Failure, Timeout, or Pending
                    clean_msg = str(msg).split('\n')[0][:100]
                    logger.warning(f"⚠️ Failed ({status}: {clean_msg}). Skipping submit.")
            else:
                logger.error("❌ Brain failed to generate code.")

            logger.info("➡️ Moving to next...")
            if not browser.click_next():
                browser.refresh()
                time.sleep(5)
                if not browser.click_next():
                    browser.driver.get("https://leetcode.com/problemset/all/")
                    time.sleep(8)
            
            time.sleep(3)

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
