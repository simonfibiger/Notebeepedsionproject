from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import glob
import os
import tkinter as tk
from tkinter import filedialog
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from TurningIntoEDpyCode import TurningIntoEDpyCode
from MusicXmlNoteExtractor import MusicXmlNoteExtractor
from AudiverisRunner import AudiverisRunner
from Online import Online

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

AUDIVERIS_DIR = r"C:\Program Files\Audiveris"
AUDIVERIS_EXE = os.path.join(AUDIVERIS_DIR, "Audiveris.exe")

OUTPUT_DIR = r"C:\programing\notebeepedison\AudiverisOutput"

ED_NOTE_CONST = {
    "A6": "Ed.NOTE_A_6",
    "A#6": "Ed.NOTE_A_SHARP_6",
    "Bb6": "Ed.NOTE_A_SHARP_6",
    "B6": "Ed.NOTE_B_6",

    "C7": "Ed.NOTE_C_7",
    "C#7": "Ed.NOTE_C_SHARP_7",
    "Db7": "Ed.NOTE_C_SHARP_7",
    "D7": "Ed.NOTE_D_7",
    "D#7": "Ed.NOTE_D_SHARP_7",
    "Eb7": "Ed.NOTE_D_SHARP_7",
    "E7": "Ed.NOTE_E_7",
    "F7": "Ed.NOTE_F_7",
    "F#7": "Ed.NOTE_F_SHARP_7",
    "Gb7": "Ed.NOTE_F_SHARP_7",
    "G7": "Ed.NOTE_G_7",
    "G#7": "Ed.NOTE_G_SHARP_7",
    "Ab7": "Ed.NOTE_G_SHARP_7",
    "A7": "Ed.NOTE_A_7",
    "A#7": "Ed.NOTE_A_SHARP_7",
    "Bb7": "Ed.NOTE_A_SHARP_7",
    "B7": "Ed.NOTE_B_7",

    "C8": "Ed.NOTE_C_8",
}


class NotesApp:
    """High-level app that interacts with the user and orchestrates everything."""

    def __init__(self):
        self.path_to_output = OUTPUT_DIR
        self.path_to_audiveris = AUDIVERIS_DIR

        self.audiveris = AudiverisRunner(AUDIVERIS_EXE, self.path_to_output)
        self.extractor = MusicXmlNoteExtractor(self.path_to_output)

    def ask_pdf_path(self) -> str:
        """Show a file dialog to select a PDF."""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        return file_path

    def run_from_pdf(self):

        pdf_path = self.ask_pdf_path()
        if not pdf_path:
            print("No file selected.")
            return

        print("[App] Selected PDF:", pdf_path)
        print("Audiveris exe exists?", os.path.isfile(AUDIVERIS_EXE))

        self.audiveris.process_pdf_to_mxl(pdf_path)

        notes = self.extractor.extract_events()
        print("\n--- Extracted Notes ---\n")
        for n in notes:
            print(n)

        edpy_generator = TurningIntoEDpyCode(notes)
        edpy_generator.generate_to_file()
        print("here")

    def run(self):
        """CLI menu: Notes or PDF scan. Currently only PDF scan implemented."""
        while True:
            choice = input("Choose an option: 1) Notes (not implemented)  2) PDF scan: ").strip()
            if choice == '1' or choice == '2':
                
                if choice == "1":
                    print("Option 1 (text behavior) not implemented yet.")
                elif choice == "2":
                    print("Option 2 selected: PDF scan. Please use the simple version notes version of the song you want edsion to play")
                    self.run_from_pdf()
                def newest_file(folder: str = "C:\\programing\\notebeepedison\\edisoncode", pattern: str = "*"):
                    files = glob.glob(os.path.join(folder, pattern))
                    if not files:
                        return None
                    return max(files, key=os.path.getmtime)
                
                print("here")
                try:
                    with open (newest_file(), "r") as f:
                        code = f.read()
                except Exception as e:
                    print(e)
                    print("Failed to read the newest edpy code file.")
                    print("try to generate again")
                    app.run()
                print("there")
                online = Online(code = code)
                online.get_file()
                online.file_manager()
                online.click_load()

            else:
                print("Invalid choice. Please enter 1 or 2.")



if __name__ == "__main__":
    app = NotesApp()
    app.run()

