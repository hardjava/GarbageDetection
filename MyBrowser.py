from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class BrowserController:
    def __init__(self, url):
        self.driver_path = 'E:\chromedriver-win64\chromedriver-win64\chromedriver.exe'
        self.download_path= 'C:\\Users\\Song\\Desktop\\GarbageProject\\img'
        self.url = url
        self.driver = None

    def start_browser(self):
        chrome_options = Options()

        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.url)
        print(f"Connect to {self.url}")

    def click_button(self, button_id):
        try:
            toggle_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, button_id))
            )
            toggle_button.click()
        except Exception as e:
            print(f"Button Except: {e}")
    
    def click_save_img(self, button_id):
        try:
            download_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, button_id))
            )
            download_button.click()
            time.sleep(5)
            downloaded_file = self.get_latest_file_in_directory()
            if downloaded_file:
                print(f"Downloaded file: {downloaded_file}")
                return downloaded_file
            else:
                print("No downloaded file found.")
            return None
        except Exception as e:
            print(f"Button Except: {e}")
            return None

    def close_browser(self):
        if self.driver:
            self.driver.quit()
    
    def get_latest_file_in_directory(self):
        try:
            files = os.listdir(self.download_path)
            if not files:
                return None
            latest_file = max(
                (os.path.join(self.download_path, f) for f in files),
                key=os.path.getctime
            )
            return os.path.basename(latest_file)
        except Exception as e:
            print(f"Error finding latest file: {e}")
            return None