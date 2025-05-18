import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class BookMyShowAutomator:
    def __init__(self, driver_path: str, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.default_city = "Bengaluru"  # Default city if none specified
    
    def open_site(self):
        """Open BookMyShow website and handle initial location selection"""
        self.driver.get("https://in.bookmyshow.com/")
        self.driver.maximize_window()
        time.sleep(3)  # Increased wait time for initial page load
        
        # Try multiple approaches to handle city selection
        try:
            # First try: Look for the location modal that appears on first visit
            try:
                location_modal = self.wait.until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        '//div[contains(@class, "sc-dkrFOg") or contains(@class, "sc-1b8cbd5c-0")]'
                    ))
                )
                print("Found location modal, attempting to select city...")
                return self.select_city(self.default_city)
            except TimeoutException:
                pass

            # Second try: Look for the current city element and click it
            try:
                # Try different possible selectors for the city element
                city_selectors = [
                    '//div[contains(@class, "sc-1b8cbd5c-0")]//span[contains(@class, "sc-1b8cbd5c-1")]',
                    '//div[contains(@class, "sc-1b8cbd5c-0")]',
                    '//div[contains(@class, "sc-1b8cbd5c-0")]//div[contains(@class, "sc-1b8cbd5c-1")]',
                    '//div[contains(@class, "sc-1b8cbd5c-0")]//div[contains(@class, "sc-1b8cbd5c-2")]',
                    '//div[contains(@class, "sc-1b8cbd5c-0")]//div[contains(@class, "sc-1b8cbd5c-3")]'
                ]
                
                current_city_element = None
                for selector in city_selectors:
                    try:
                        current_city_element = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if current_city_element:
                            break
                    except:
                        continue

                if current_city_element:
                    # Get current city text
                    current_city = current_city_element.text.strip()
                    print(f"Current city detected: {current_city}")
                    
                    if current_city.lower() != self.default_city.lower():
                        # Click the city element to open location modal
                        try:
                            current_city_element.click()
                            time.sleep(2)
                            return self.select_city(self.default_city)
                        except ElementClickInterceptedException:
                            # If click is intercepted, try JavaScript click
                            self.driver.execute_script("arguments[0].click();", current_city_element)
                            time.sleep(2)
                            return self.select_city(self.default_city)
                    else:
                        print(f"Already in {self.default_city}")
                        return True
                else:
                    print("Could not find city selection element with any known selector")
                    return False

            except Exception as e:
                print(f"Error in second city selection attempt: {str(e)}")
                return False

        except Exception as e:
            print(f"Error in city selection process: {str(e)}")
            return False

    def select_city(self, city_name: str):
        """Select a city from the location modal"""
        try:
            # Try different selectors for the city list
            city_list_selectors = [
                '//ul[contains(@class, "sc-dkrFOg")]//li',
                '//div[contains(@class, "sc-dkrFOg")]//li',
                '//div[contains(@class, "sc-1b8cbd5c-0")]//ul//li',
                '//div[contains(@class, "sc-1b8cbd5c-0")]//div[contains(@class, "sc-1b8cbd5c-1")]//li'
            ]
            
            cities = None
            for selector in city_list_selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    cities = self.driver.find_elements(By.XPATH, selector)
                    if cities:
                        break
                except:
                    continue
            
            if not cities:
                print("Could not find city list with any known selector")
                return False
            
            # Try to find and click the city
            city_found = False
            for city in cities:
                try:
                    city_text = city.text.strip().lower()
                    if city_name.lower() in city_text:
                        # Try regular click first
                        try:
                            city.click()
                        except ElementClickInterceptedException:
                            # If regular click fails, try JavaScript click
                            self.driver.execute_script("arguments[0].click();", city)
                        
                        print(f"City '{city_name}' selected successfully.")
                        time.sleep(2)  # Wait for city selection to take effect
                        city_found = True
                        break
                except Exception as e:
                    print(f"Error clicking city element: {str(e)}")
                    continue
            
            if not city_found:
                print(f"City '{city_name}' not found in the list.")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error selecting city: {str(e)}")
            return False

    def search_movie(self, movie_name: str):
        """Search for a movie in the selected city"""
        try:
            # Click the search icon
            search_icon = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    '//div[@data-testid="SearchIcon"]'
                ))
            )
            search_icon.click()
            time.sleep(1)

            # Enter movie name in search box
            search_input = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    '//input[@placeholder="Search for Movies, Events, Plays, Sports and Activities"]'
                ))
            )
            search_input.clear()
            search_input.send_keys(movie_name)
            time.sleep(2)  # Wait for search suggestions
            
            # Press Enter to search
            search_input.send_keys(Keys.ENTER)
            print(f"Searching for movie: {movie_name}")
            time.sleep(3)  # Wait for search results
            
            return True
            
        except Exception as e:
            print(f"Error searching for movie: {str(e)}")
            return False

    def click_first_result(self):
        """Click on the first movie result"""
        try:
            # Wait for and click the first movie result
            first_result = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    '(//div[contains(@class, "sc-7o7nez-0")])[1]'
                ))
            )
            first_result.click()
            print("Selected first movie result")
            time.sleep(2)  # Wait for movie details to load
            return True
            
        except Exception as e:
            print(f"Error selecting movie result: {str(e)}")
            return False

    def close(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error closing browser: {str(e)}")
    
    
