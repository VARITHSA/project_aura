import time

import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WikipediaBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.engine = pyttsx3.init()
        
    def open_weki(self):
        self.driver.get("https://www.wikipedia.org/")
        time.sleep(2)
        
    def search_topic(self, query):
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
        self.driver.quit()
        
