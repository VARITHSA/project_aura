import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class GoogleBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def start(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(self.driver_path), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.google.com")
        print("🌐 Google loaded")

    def search(self, query):
        try:
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_input.clear()
            search_input.send_keys(query)
            search_input.submit()  # Simulates pressing Enter
            print(f"🔍 Searching for: {query}")
            time.sleep(3)  # wait for results to load
        except Exception as e:
            print("❌ Search failed:", e)

    def close(self):
        if self.driver:
            self.driver.quit()
            print("🛑 GoogleBot closed")
