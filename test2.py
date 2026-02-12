import subprocess

exe_path = r"C:\Program Files\Audiveris\Audiveris.exe"

subprocess.run([exe_path, "-batch"])


# -------------------------------------------------------------------
# AUDIVERIS RUNNER (PDF -> MXL)
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# MUSICXML NOTE EXTRACTOR (MXL -> ["D4", "F#3", "Rest", ...])
# -------------------------------------------------------------------


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


# -------------------------------------------------------------------
# MAIN APP (USER INPUT + TKINTER FILE PICKER + ORCHESTRATION)
# -------------------------------------------------------------------