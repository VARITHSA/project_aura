import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class StackOverflowFlowBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_stackoverflow(self):
        self.initialize_driver()
        self.driver.get("https://stackoverflow.com/")
        self.driver.maximize_window()
        self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        logging.info("✅ StackOverflow opened.")

    def search_query(self, query):
        try:
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-post-summary--content-title a")))
            logging.info(f"🔍 Searched for: {query}")
        except Exception as e:
            logging.error(f"❌ Failed to search: {e}")

    def open_top_result(self):
        try:
            top_links = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-post-summary--content-title a")))
            if not top_links:
                logging.warning("⚠️ No search results found.")
                return
            top_link = top_links[0]
            link_text = top_link.text
            top_link.click()
            self.wait.until(EC.presence_of_element_located((By.ID, "question-header")))
            logging.info(f"📄 Opened top result: {link_text}")
        except Exception as e:
            logging.error(f"❌ Failed to open top result: {e}")

    def extract_accepted_answer(self):
        try:
            answer = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".answer.accepted-answer .js-post-body")))
            answer_text = answer.text.strip()
            if answer_text:
                logging.info("✅ Accepted Answer:\n" + "-"*60)
                logging.info(answer_text[:500] + "..." if len(answer_text) > 500 else answer_text)
                return answer_text
            else:
                logging.warning("⚠️ Accepted answer is empty.")
        except Exception as e:
            logging.warning(f"⚠️ No accepted answer found or couldn't load. Error: {e}")
        return None

    def save_answer_to_file(self, filename="accepted_answer.txt"):
        try:
            answer_text = self.extract_accepted_answer()
            if answer_text:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(answer_text)
                logging.info(f"✅ Saved accepted answer to '{filename}'")
        except Exception as e:
            logging.error(f"❌ Failed to save answer to file: {e}")

    def upvote_question(self):
        try:
            upvote_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-vote-up-btn")))
            upvote_btn.click()
            logging.info("👍 Attempted to upvote the question. (Login may be required)")
        except Exception as e:
            logging.warning(f"❌ Failed to upvote: {e}")

    def go_to_user_profile(self):
        try:
            user_link = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".user-details a")))
            profile_url = user_link.get_attribute("href")
            user_link.click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-card-name")))
            logging.info(f"👤 Navigated to user profile: {profile_url}")
        except Exception as e:
            logging.error(f"❌ Failed to navigate to user profile: {e}")

    def reset(self):
        try:
            self.driver.get("https://stackoverflow.com/")
            self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            logging.info("🔄 Reset to StackOverflow home.")
        except Exception as e:
            logging.error(f"❌ Failed to reset to home: {e}")

    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
                logging.info("🛑 Browser closed.")
        except Exception as e:
            logging.error(f"❌ Error closing browser: {e}")
