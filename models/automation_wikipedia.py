import time

import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WikipediaBot:
    def __init__(self, driver_path="chromedriver.exe"):
        self.driver_path = driver_path
        self.driver = None
        self.engine = pyttsx3.init()

    def initialize_driver(self):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def open_wiki(self):
        if not self.driver:
            self.initialize_driver()
        self.driver.get("https://www.wikipedia.org/")
        time.sleep(2)

    def search_topic(self, query):
        if not self.driver:
            self.initialize_driver()
            self.open_wiki()

        try:
            search_box = self.driver.find_element(By.NAME, "search")
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)

            # Extract first paragraph
            paragraph = self.driver.find_element(By.CSS_SELECTOR, "p").text
            print(f"Wikipedia Summary: {paragraph}")
            self.engine.say(paragraph)
            self.engine.runAndWait()
        except Exception as e:
            print("Error while searching Wikipedia:", e)
            self.engine.say("Sorry, I couldn't find anything.")
            self.engine.runAndWait()

    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print("Error closing browser:", e)
