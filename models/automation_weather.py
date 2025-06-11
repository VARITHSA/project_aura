# models/automation_weather.py

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WeatherBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    
    def get_weather(self, location="Bangalore"):
        if not self.driver:
            self.initialize_driver()

        try:
            self.driver.get("https://www.google.com/")
            self.driver.maximize_window()

            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys(f"weather in {location}")
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)

            temperature = self.wait.until(EC.presence_of_element_located((By.ID, "wob_tm"))).text
            condition = self.driver.find_element(By.ID, "wob_dc").text
            time_info = self.driver.find_element(By.ID, "wob_dts").text

            print(f"🌦️ Weather in {location} as of {time_info}: {temperature}°C, {condition}")
        except Exception as e:
            print("Failed to retrieve weather:", e)

    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Error closing WeatherBot browser: {e}")
