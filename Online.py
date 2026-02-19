import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import glob
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard

class Online:
    """Handles only the Selenium / EdPy web stuff."""
    

    def __init__(self, code):
        print("Initializing Online class...")
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_experimental_option("detach", True)
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
        
        wait = WebDriverWait(self.driver, 3)

        wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//header//li[1]/a")
    )).click()

        wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//header//li[1]//li[3]/a")
    )).click()


        wait.until(EC.element_to_be_clickable(By.ID, "modLoadFiles")).click()

        time.sleep(1)
  
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
