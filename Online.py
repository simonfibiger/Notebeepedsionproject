import glob
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Online:
    URL = "https://www.edpyapp.com/v3/"
    CODE_FOLDER = r"C:\programing\notebeepedison\edisoncode"

    # Stable selectors
    FILE_MENU = (By.XPATH, "//header//li[1]/a")
    LOAD_MENU = (By.XPATH, "//header//li[1]//li[3]/a")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    LOAD_BUTTON = (By.XPATH, "//div[contains(@class,'modal')]//button[contains(text(),'Load')]")
    PROGRAM_BUTTON = (By.ID, "aProgram")

    def __init__(self, visible=False):
        self.driver = self._create_driver(visible)
        self.wait = WebDriverWait(self.driver, 20)

        self.driver.get(self.URL)

    # -------------------------
    # Driver setup
    # -------------------------

    def _create_driver(self, visible):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        if visible:
            driver.set_window_size(1920, 1080)
            driver.set_window_position(100, 100)
        else:
            driver.set_window_size(1920, 1080)
            driver.set_window_position(-2000, 0)

        return driver

    def show_browser(self):
        self.driver.set_window_position(100, 100)
        self.driver.maximize_window()

    # -------------------------
    # File handling
    # -------------------------

    def find_newest_file(self, folder=None):
        folder = folder or self.CODE_FOLDER

        files = glob.glob(os.path.join(folder, "*"))

        if not files:
            raise FileNotFoundError("No files found in edisoncode folder")

        newest = max(files, key=os.path.getmtime)
        return os.path.abspath(newest)

    # -------------------------
    # Selenium helpers
    # -------------------------

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def upload_file(self, path):
        file_input = self.wait.until(
            EC.presence_of_element_located(self.FILE_INPUT)
        )
        file_input.send_keys(path)

    # -------------------------
    # Main workflow
    # -------------------------

    def load_latest_file(self):
        path = self.find_newest_file()

        print(f"Uploading: {path}")

        self.click(self.FILE_MENU)
        self.click(self.LOAD_MENU)
        self.upload_file(path)
        self.click(self.LOAD_BUTTON)

    def program_robot(self):
        self.click(self.PROGRAM_BUTTON)

    def run(self, show_when_done=True, keep_open=True):
        self.load_latest_file()
        self.program_robot()

        if show_when_done:
            self.show_browser()

        if keep_open:
            input("Automation complete. Press Enter to exit.")



# -------------------------
# Entry point
# -------------------------

if __name__ == "__main__":
    online = Online(visible=False)
    online.run(show_when_done=True)
