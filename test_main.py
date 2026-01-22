from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import subprocess
from PIL import Image
import time
import glob
import os
import tkinter as tk
from tkinter import filedialog
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import sys


CCOMMAND1 = "Audiveris.exe -batch -export -output \"C:\\programing\\notebeepedison\\AudiverisOutput\" \"C:\\programing\\notebeepedison\\notes\\Pirates-of-the-Caribbean-intermediate.pdf\""

COMMAND2 = "Audiveris.exe -batch -export -output \"C:\\programing\\notebeepedison\\AudiverisOutput\" -export-format musicxml \"C:\\programing\\notebeepedison\\notes\\Pirates-of-the-Caribbean-intermediate.pdf\""

# open browser
class Online:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.edpyapp.com/")
        time.sleep(2)
    def find_blank(self, xpath='//*[@id="root"]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div/textarea'):
        time.sleep(1)
        blank = self.driver.find_element(By.XPATH,xpath)
        return blank
    def write_text(self,text, xpath = ""):
        time.sleep(1)
        blank = self.driver.find_element(By.XPATH,xpath)
        blank.send_keys(text)
        blank.send_keys(Keys.ENTER)
    def run_code(self, xpath = ""):
        time.sleep(1)
        run_button = self.driver.find_element(By.XPATH,xpath)
        run_button.click()
class Notes:
    def __init__(self):
        # automatically call input handler when Notes is instantiated
        self.choice = None
        self.path_to_output = "C:/programing/notebeepedison/AudiverisOutput"
        self.path_to_audveris = "C:/Program Files/Audiveris"
        self.notes = self.handle_user_input()
        
    

    def handle_user_input(self):
        # loop until a valid choice is provided
        while True:
            choice = input("Choose an option Notes or PDF scan (1 or 2): ").strip()
            if choice == "1":
                self.choice = "1"
                # implement behavior for option 1 here
                print("Option 1 selected")
                self.text_bahavior()
                break
            elif choice == "2":
                self.choice = "2"
                # implement behavior for option 2 here
                print("Option 2 selected")
                self.photo_behavior()
                print("fuck")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
    def text_bahavior(self):
        # define behavior for option 1
        pass
    def photo_behavior(self):
        print("got here")
        def ask_image_path():
            root = tk.Tk()
            root.withdraw()  # hide main window
            root.attributes('-topmost', True)  # force dialog to appear on top            # hide completely
            file_path = filedialog.askopenfilename(title="selefct a pdf file", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
            print(file_path)

            return file_path
        path = ask_image_path()
        def note_to_text(self, path = path):
            print("Exists?", os.path.isfile(self.path_to_audveris + r"\Audiveris.exe"))
            print (str(self.path_to_output))
            print(str(path))
            exe_path = os.path.join(self.path_to_audveris, "Audiveris.exe")
            subprocess.run([
                    exe_path,            
                    "-batch",
                    "-export",
                    "-output",
                    rf"{str(self.path_to_output)}",
                    rf"{str(path)}"
                ], 
            
            )
            time.sleep(5) # wait for the process to complete
            subprocess.run([
                exe_path,           
                "-batch",
                "-export",
                "-output",  
                rf"{self.path_to_output}",
                "-export-format", "musicxml",
                rf"{str(path)}"]
                )
            time.sleep(5)

        note_to_text(self)
        self.transformer()
    def transformer(self):

 

        def open_newest_musicxml():
            files = glob.glob(os.path.join(self.path_to_output, "*.mxl"))

            if not files:
                print("No .mxl files found.")
                return None

            newest_file = max(files, key=os.path.getctime)

            try:
                with zipfile.ZipFile(newest_file, 'r') as z:
                    # MusicXML files usually end with .xml
                    xml_name = None
                    for name in z.namelist():
                        if name.endswith(".xml"):
                            xml_name = name
                            break

                    if xml_name is None:
                        print("No XML file found inside MXL.")
                        return None

                    xml_data = z.read(xml_name)
                    root = ET.fromstring(xml_data)
                    return root

            except zipfile.BadZipFile:
                print("ERROR: The .mxl file is corrupted or not a valid ZIP.")
                return None

        def transform_to_text(root):
            if root is None:
                print("No XML loaded.")
                return

            print("\n--- Extracted Notes ---\n")

            notes = []
            for note in root.iter("note"):
                pitch = note.find("pitch")

                if pitch is None:
                    print("Rest")
                    continue

                step = pitch.find("step").text
                octave = pitch.find("octave").text

                alter = pitch.find("alter")
                accidental = ""
                if alter is not None:
                    if alter.text == "1":
                        accidental = "#"
                    elif alter.text == "-1":
                        accidental = "b"
                note = f"{step}{accidental}{octave}"
                notes.append(note)
                print(note)
     

        # ---- RUN THE FUNCTIONS ----
        root = open_newest_musicxml()
        transform_to_text(root)
        return notes

                
        

        
  
if __name__ == "__main__":
    # Initialize classes
    #online = Online()
    notes = Notes()
    


    #online.find_blank()
    #online.write_text(text = "")
    #online.run_code()



    
