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
import math
from datetime import datetime


# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

AUDIVERIS_DIR = r"C:\Program Files\Audiveris"
AUDIVERIS_EXE = os.path.join(AUDIVERIS_DIR, "Audiveris.exe")

OUTPUT_DIR = r"C:\programing\notebeepedison\AudiverisOutput"


# -------------------------------------------------------------------
# BROWSER AUTOMATION (EdPy)
# -------------------------------------------------------------------

class Online:
    """Handles only the Selenium / EdPy web stuff."""
    
    def __init__(self, code):
        self.code = code
        


    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.edpyapp.com/")
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


# -------------------------------------------------------------------
# AUDIVERIS RUNNER (PDF -> MXL)
# -------------------------------------------------------------------

class AudiverisRunner:
    """Responsible only for running Audiveris on a PDF."""

    def __init__(self, exe_path: str, output_dir: str):
        self.exe_path = exe_path
        self.output_dir = output_dir

    def process_pdf_to_mxl(self, pdf_path: str):
        """
        Run the two-step Audiveris process on the given PDF.

        IMPORTANT: This is intentionally written to match your old working
        code as closely as possible. No check=True, same argument order,
        same use of raw f-strings.
        """
        exe_path = self.exe_path
        out_dir = self.output_dir
        pdf = str(pdf_path)

        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"Audiveris.exe not found at {exe_path}")

        if not os.path.isfile(pdf):
            raise FileNotFoundError(f"PDF not found at {pdf}")

        os.makedirs(out_dir, exist_ok=True)

        print("Exists?", os.path.isfile(exe_path))
        print(str(out_dir))
        print(str(pdf))

        # ---------- FIRST PASS (your original COMMAND1) ----------
        # Audiveris.exe -batch -export -output "<output>" "<pdf>"
        subprocess.run([
            exe_path,
            "-batch",
            "-export",
            "-output",
            rf"{str(out_dir)}",
            rf"{str(pdf)}"
        ])
        time.sleep(5)  # give Audiveris time

        # ---------- SECOND PASS (your original COMMAND2) ----------
        # Audiveris.exe -batch -export -output "<output>" -export-format musicxml "<pdf>"
        subprocess.run([
            exe_path,
            "-batch",
            "-export",
            "-output",
            rf"{str(out_dir)}",
            "-export-format", "musicxml",
            rf"{str(pdf)}"
        ])
        time.sleep(5)



# -------------------------------------------------------------------
# MUSICXML NOTE EXTRACTOR (MXL -> ["D4", "F#3", "Rest", ...])
# -------------------------------------------------------------------

class MusicXmlNoteExtractor:
    """Finds newest .mxl in a folder and extracts note names from it."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def _open_newest_musicxml_root(self):
        files = glob.glob(os.path.join(self.output_dir, "*.mxl"))
        if not files:
            print("No .mxl files found in", self.output_dir)
            return None

        newest_file = max(files, key=os.path.getctime)
        print("[Extractor] Using newest MXL:", newest_file)

        try:
            with zipfile.ZipFile(newest_file, 'r') as z:
                xml_name = None
                for name in z.namelist():
                    if name.lower().endswith(".xml"):
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

    def extract_events(self):
        root = self._open_newest_musicxml_root()
        if root is None:
            return []

        events = []
        divisions = 1  # fallback

        for part in root.findall(".//part"):
            for measure in part.findall("measure"):

                # update divisions if present in this measure
                div_el = measure.find(".//attributes/divisions")
                if div_el is not None and div_el.text and div_el.text.strip().isdigit():
                    divisions = int(div_el.text.strip())

                for note_el in measure.findall("note"):

                    # --- FILTER: DROP BASS/OTHER STAFF ---
                    staff_text = note_el.findtext("staff")  # "1", "2", ...
                    if staff_text is not None and staff_text.strip() != "1":
                        continue

                    # OPTIONAL: keep only main voice
                    voice_text = note_el.findtext("voice")  # "1", "2", ...
                    if voice_text is not None and voice_text.strip() != "1":
                        continue
                    # -------------------------------------

                    # skip grace notes
                    if note_el.find("grace") is not None:
                        continue

                    dur_el = note_el.find("duration")
                    dur = int(dur_el.text.strip()) if dur_el is not None and dur_el.text else 0

                    # rest
                    if note_el.find("rest") is not None:
                        events.append({"type": "rest", "duration": dur, "divisions": divisions})
                        continue

                    pitch = note_el.find("pitch")
                    if pitch is None:
                        events.append({"type": "rest", "duration": dur, "divisions": divisions})
                        continue

                    step = (pitch.findtext("step") or "").strip()
                    octave = (pitch.findtext("octave") or "").strip()
                    alter = pitch.findtext("alter")

                    accidental = ""
                    if alter is not None and alter.strip() == "1":
                        accidental = "#"
                    elif alter is not None and alter.strip() == "-1":
                        accidental = "b"

                    note_name = f"{step}{accidental}{octave}"
                    events.append({"type": "note", "note": note_name, "duration": dur, "divisions": divisions})

        return events
   #def extract_notes(self):
   #    """Returns a list of notes like ['F3', 'A3', 'D4', 'Rest', ...]."""
   #    root = self._open_newest_musicxml_root()
   #    if root is None:
   #        return []

   #    notes = []

   #    for note_el in root.iter("note"):
   #        pitch = note_el.find("pitch")

   #        if pitch is None:
   #            notes.append("Rest")
   #            continue

   #        step_el = pitch.find("step")
   #        octave_el = pitch.find("octave")
   #        alter_el = pitch.find("alter")

   #        if step_el is None or octave_el is None:
   #            notes.append("Rest")
   #            continue

   #        step = (step_el.text or "").strip()
   #        octave = (octave_el.text or "").strip()

   #        accidental = ""
   #        if alter_el is not None and alter_el.text is not None:
   #            val = alter_el.text.strip()
   #            if val == "1":
   #                accidental = "#"
   #            elif val == "-1":
   #                accidental = "b"

   #        note_name = f"{step}{accidental}{octave}"
   #        notes.append(note_name)

   #    return notes

class TurningIntoEDpyCode:
    NOTE_OFFSETS = {
        "C": 0, "C#": 1, "Db": 1,
        "D": 2, "D#": 3, "Eb": 3,
        "E": 4,
        "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10,
        "B": 11
    }

    def __init__(self, events, tempo_bpm: int = 120, out_dir: str = "edisoncode"):
        if not events:
            raise ValueError("events list is empty or None")

        self.events = events
        self.tempo_bpm = int(tempo_bpm)
        self.out_dir = out_dir

        # Create a new file path ONCE per run.
        self.createTXT(out_dir=self.out_dir)

    # ---------------- FILE METHODS (split as you want) ---------------- #

    def createTXT(self, out_dir: str = "edisoncode") -> None:
        """Create a unique path for this run and initialize/clear the file."""
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"edison_{ts}.txt"
        self.path = os.path.join(out_dir, filename)

        # Initialize empty file so appends start clean
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("")

    def save_edpy_code(self, code_line: str) -> None:
        """Append ONE line to the file."""
        with open(self.path, "a", encoding="utf-8") as f:
            # ensure exactly one newline
            f.write(code_line.rstrip("\n") + "\n")

    # ---------------- INTERNAL ---------------- #

    @classmethod
    def _note_to_period(cls, note: str) -> str:
        note = (note or "").strip()
        if not note or note.lower().startswith("rest"):
            return "Ed.NOTE_REST"

        i = 0
        while i < len(note) and not note[i].isdigit():
            i += 1

        step = note[:i].replace("♯", "#").replace("♭", "b")
        octave_str = note[i:] or "4"

        try:
            octave = int(octave_str)
        except ValueError:
            return "Ed.NOTE_REST"

        if step:
            step = step[0].upper() + step[1:]

        if step not in cls.NOTE_OFFSETS:
            return "Ed.NOTE_REST"

        semitone_from_C0 = cls.NOTE_OFFSETS[step] + octave * 12
        C0 = 16.351597831287414
        freq = C0 * (2 ** (semitone_from_C0 / 12.0))
        period = int(round(8_000_000 / freq))

        while period > 32767:
            period //= 2
        if period < 1:
            period = 1

        return str(period)

    def _ticks_to_ms(self, dur_ticks: int, divisions: int) -> int:
        if not divisions or divisions <= 0:
            divisions = 1
        if dur_ticks is None or dur_ticks < 0:
            dur_ticks = 0

        quarter_ms = 60000.0 / float(self.tempo_bpm)
        ms = int(round(quarter_ms * (float(dur_ticks) / float(divisions))))
        return max(ms, 1)

    # ---------------- GENERATION ---------------- #

    def generate_to_file(self) -> None:
        """
        Writes the EdPy program line-by-line into the prepared txt file.
        """

  
        self.save_edpy_code("def main():")
        self.save_edpy_code(f"    Ed.Tempo({self.tempo_bpm})")
        self.save_edpy_code("")

        for ev in self.events:
            ev_type = (ev.get("type") or "").lower()
            dur = ev.get("duration", 0)
            div = ev.get("divisions", 1)
            ms = self._ticks_to_ms(dur, div)             
            if ev_type == "rest":
                self.save_edpy_code(f"    Ed.PlayTone(Ed.NOTE_REST, {ms})")
            else:
                note_name = ev.get("note", "Rest")
                period = self._note_to_period(note_name)
                self.save_edpy_code(f"    Ed.PlayTone({period}, {ms})")
            #MAKING EDPY WAIT FOR TONE TO END
            self.save_edpy_code("    while Ed.ReadMusicEnd() == 0:")
            self.save_edpy_code("        pass")
        self.save_edpy_code("main()")


    


# -------------------------------------------------------------------
# MAIN APP (USER INPUT + TKINTER FILE PICKER + ORCHESTRATION)
# -------------------------------------------------------------------

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
        """Full flow: choose PDF, run Audiveris, extract notes, print them."""
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

        edpy_generator = TurningIntoEDpyCode(notes, tempo_bpm=120)
        edpy_generator.generate_to_file()

    def run(self):
        """CLI menu: Notes or PDF scan. Currently only PDF scan implemented."""
        while True:
            choice = input("Choose an option: 1) Notes (not implemented)  2) PDF scan: ").strip()
            if choice == '1' or choice == '2':

                if choice == "1":
                    print("Option 1 (text behavior) not implemented yet.")
                    return
                elif choice == "2":
                    print("Option 2 selected: PDF scan.")
                    self.run_from_pdf()
                    return
                def newest_file(folder: str, pattern: str = "*"):
                    files = glob.glob(os.path.join(folder, pattern))
                    if not files:
                        return None
                    return max(files, key=os.path.getmtime)
                
                print("here")
                with open (newest_file(), "r") as f:
                    code = f.read()
                print("there")
                online = Online(code = code)
                online.find_blank()
                online.write_text(code)
            else:
                print("Invalid choice. Please enter 1 or 2.")


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    app = NotesApp()
    app.run()


    # Later, when you’re ready to push to EdPy via Selenium:
    # edpy_code = build_edpy_program(app.notes)  # you'd implement this
    # online = Online()
    # editor_xpath = '...'
    # online.write_text(edpy_code, editor_xpath)
    # online.run_code(run_button_xpath)
