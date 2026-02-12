import zipfile
import xml.etree.ElementTree as ET
import os
import glob

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