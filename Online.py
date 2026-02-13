import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import glob
import os

import keyboard

class Online:
    """Handles only the Selenium / EdPy web stuff."""
    

    def __init__(self, code):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.edpyapp.com/v3/")
        time.sleep(2)
        print("opened")
    
    def find_newest(self, folder: str = "C:\\programing\\notebeepedison\\edisoncode", pattern: str = "*"):
        files = glob.glob(os.path.join(folder, pattern))
        if not files:
            return None
        return max(files, key=os.path.getmtime)

    def get_file(self, xpath='/html/body/div[21]/div/div[1]/div/header/div/div/div[1]/ul/li[1]/a'):
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        button = self.driver.find_element(By.XPATH, '/html/body/div[21]/div/div[1]/div/header/div/div/div[1]/ul/li[1]/ul/li[3]/a')
        button.click()
        button = self.driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[2]/div[1]/div/div[2]/input')
        button.click()

    def file_manager(self):
        finded = self.find_newest()
        if finded is None:
            print("No files found in edisoncode folder.")
            return None
        else:           
            keyboard.write(f'C:\programing\notebeepedison\edisoncode\{os.path.basename(finded)}')
            keyboard.press_and_release('enter')
    def click_load(self, xpath = "/html/body/div[9]/div/div/div[3]/button"):
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        button = self.driver.find_element(By.XPATH, '/html/body/div[21]/div/div[1]/div/header/div/div/div[3]/ul/li[1]/a[1]')
        button.click()
    





      
    def connect_robot():
        pass


    """def run_code(self, xpath: str):
   
        time.sleep(1)
        run_button = self.driver.find_element(By.XPATH, xpath)
        run_button.click()"""
