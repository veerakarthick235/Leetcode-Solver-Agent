import time
import logging
from browser import Browser
from brain import CodeBrain
from memory import Memory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("🤖 AGENT STARTED: Pure API High-Accuracy Mode")
    browser = Browser()
    brain = CodeBrain()
    memory = Memory()

    while True:
        start_time = time.time()
        try:
            slug = browser.get_current_slug()
            logger.info(f"📍 PROBLEM: {slug}")

            if memory.is_solved(slug):
                logger.info(f"⏩ {slug} already solved. Skipping...")
            else:
                # 1. Perception: Scrape context
                desc = browser.get_text()
                starter = browser.get_starter_code()
                
                # 2. Intelligence: Pure Gemini API call
                logger.info("🧠 Generating high-accuracy solution...")
                code = brain.generate_solution(desc, starter)
                
                if code:
                    # 3. Action: Inject and verify
                    logger.info("⚡ Injecting code...")
                    browser.run_code(code)
                    
                    # Wait 7s for LeetCode results to display
                    time.sleep(7)
                    
                    # 4. Final Submission
                    logger.info("🏆 Submitting...")
                    browser.submit()
                    memory.save(slug, code, "Accepted")
                else:
                    logger.error("❌ API failed to provide code.")

            # 5. Maintaining 20s Pace
            wait_time = max(0, 20 - (time.time() - start_time))
            time.sleep(wait_time)

            # 6. Navigation
            if not browser.click_next():
                break
            time.sleep(3)

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
