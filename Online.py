import time 
from selenium import webdriver
from selenium.webdriver.common.by import By

class Online:
    """Handles only the Selenium / EdPy web stuff."""
    

    def __init__(self, code):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.edpyapp.com/v3/")
        time.sleep(2)
        print("opened")

    def find_blank(self, xpath='/html/body/div[21]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/span/text()'):
        time.sleep(1)
        return self.driver.find_element(By.XPATH, xpath)

    def write_text(self, text: str, xpath: str):
        """Writes the given text into the EdPy editor."""
        time.sleep(1)
        blank = self.driver.find_element(By.XPATH, xpath)
        blank.clear()
        blank.send_keys(self.code)
    def connect_robot():
        pass


    """def run_code(self, xpath: str):
   
        time.sleep(1)
        run_button = self.driver.find_element(By.XPATH, xpath)
        run_button.click()"""
