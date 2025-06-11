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
        try:
            self.driver.get("https://www.google.com")
            self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            print("🌐 Google loaded successfully")
        except Exception as e:
            print(f"❌ Failed to open Google: {str(e)}")
            raise  # Re-raise the exception to properly handle it in the workflow

    def search(self, query):
        try:
            # First ensure we're on Google
            if "google.com" not in self.driver.current_url:
                self.driver.get("https://www.google.com")
                self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            
            # Perform the search
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_input.clear()
            search_input.send_keys(query)
            search_input.submit()  # Simulates pressing Enter
            
            # Wait for search results to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#search")))
            print(f"🔍 Google search results loaded for: {query}")
            
        except Exception as e:
            print(f"❌ Google search failed: {str(e)}")
            raise  # Re-raise the exception to properly handle it in the workflow

    def close(self):
        if self.driver:
            self.driver.quit()
            print("🛑 GoogleBot closed")
