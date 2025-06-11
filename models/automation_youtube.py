import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class YouTubeBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    
    def open_youtube(self):
        if not self.driver:
            self.initialize_driver()
        self.driver.get("https://www.youtube.com")
        self.driver.maximize_window()
        time.sleep(2)  # Wait for page to load

    def search_video(self, query):
        try:
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
        except Exception as e:
            print("Failed to search:", e)

    def play_first_video(self):
        try:
            time.sleep(2)
            first_video = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer #video-title")))
            first_video.click()
            print("Video started.")
            time.sleep(5)
        except Exception as e:
            print("Failed to play video:", e)

    def skip_ad_if_present(self):
        try:
            ad_wait = WebDriverWait(self.driver, 15)
            skip_btn = ad_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button")))
            time.sleep(1)
            skip_btn.click()
            print("Skipped ad.")
            time.sleep(1)
        except:
            print("No skippable ad found.")
            
    def like_video(self):
        try:
            like_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//ytd-toggle-button-renderer[@is-icon-button])[1]//button")))
            like_button.click()
            print("Video liked.")
        except Exception as e:
            print("Failed to like video:", e)

    def dislike_video(self):
        try:
            dislike_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//ytd-toggle-button-renderer[@is-icon-button])[2]//button")))
            dislike_button.click()
            print("Video disliked.")
        except Exception as e:
            print("Failed to dislike video:", e)

    def subscribe_channel(self):
        try:
            subscribe_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//ytd-subscribe-button-renderer//tp-yt-paper-button")))
            if "SUBSCRIBE" in subscribe_button.text.upper():
                subscribe_button.click()
                print("Subscribed to channel.")
            else:
                print("Already subscribed.")
        except Exception as e:
            print("Failed to subscribe:", e)

    def unsubscribe_channel(self):
        try:
            subscribe_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//ytd-subscribe-button-renderer//tp-yt-paper-button")))
            if "SUBSCRIBED" in subscribe_button.text.upper():
                subscribe_button.click()
                confirm_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//yt-confirm-dialog-renderer//tp-yt-paper-button[@aria-label='Unsubscribe']")))
                confirm_btn.click()
                print("Unsubscribed from channel.")
            else:
                print("Not subscribed.")
        except Exception as e:
            print("Failed to unsubscribe:", e)

    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Error closing browser: {e}")
