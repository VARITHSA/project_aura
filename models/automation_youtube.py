import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class YouTubeBot:
    def __init__(self, driver_path="chromedriver.exe"):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_youtube(self):
        self.driver.get("https://www.youtube.com")
        self.driver.maximize_window()

    def search_video(self, query):
        try:
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
        except Exception as e:
            print("Failed to search:", e)

    def play_first_video(self):
        try:
            first_video = self.wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
            first_video.click()
            print("Video started.")
        except Exception as e:
            print("Failed to play video:", e)

    def skip_ad_if_present(self):
        try:
            ad_wait = WebDriverWait(self.driver, 15)
            skip_btn = ad_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button")))
            skip_btn.click()
            print("Skipped ad.")
        except:
            print("No skippable ad found.")

    def quit(self):
        self.driver.quit()