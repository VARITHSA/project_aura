import time

import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WikipediaBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.engine = pyttsx3.init()



    def open_wiki(self):
        self.driver.get("https://www.wikipedia.org/")
        time.sleep(2)

    def search_topic(self, query):
        if not self.driver:
            print("❌ Web driver not initialized.")
            return

        try:
            print("🌐 Opening Wikipedia...")
            self.driver.get("https://www.wikipedia.org/")
        
            self.wait.until(EC.presence_of_element_located((By.NAME, "search")))
        
            print("🔎 Searching Wikipedia...")
            search_box = self.driver.find_element(By.NAME, "search")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)

        # Wait for the paragraph to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output > p")))
            paragraph = self.driver.find_element(By.CSS_SELECTOR, "div.mw-parser-output > p").text

            print(f"📄 Wikipedia Summary:\n{paragraph}")
            self.engine.say(paragraph[:400])
            self.engine.runAndWait()

        except Exception as e:
            print("❌ Error while searching Wikipedia:", e)
            self.engine.say("Sorry, I couldn't find anything.")
            self.engine.runAndWait()


    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print("Error closing browser:", e)
