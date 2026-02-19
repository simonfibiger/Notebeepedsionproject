import os
from datetime import datetime

class TurningIntoEDpyCode:
  

    def __init__(self, notes):
      
        self.note_offsets = {
            "C": 0, "C#": 1, "Db": 1,
            "D": 2, "D#": 3, "Eb": 3,
            "E": 4,
            "F": 5, "F#": 6, "Gb": 6,
            "G": 7, "G#": 8, "Ab": 8,
            "A": 9, "A#": 10, "Bb": 10,
            "B": 11
    }

        self.edison_min = self.note_to_midi("A6") 
        self.edison_max = self.note_to_midi("C8")
        self.notes = notes

        self.midi_to_edison = {
                self.note_to_midi("A6"): "Ed.NOTE_A_6",
                self.note_to_midi("A#6"): "Ed.NOTE_A_SHARP_6",
                self.note_to_midi("B6"): "Ed.NOTE_B_6",
                self.note_to_midi("C7"): "Ed.NOTE_C_7",
                self.note_to_midi("C#7"): "Ed.NOTE_C_SHARP_7",
                self.note_to_midi("D7"): "Ed.NOTE_D_7",
                self.note_to_midi("D#7"): "Ed.NOTE_D_SHARP_7",
                self.note_to_midi("E7"): "Ed.NOTE_E_7",
                self.note_to_midi("F7"): "Ed.NOTE_F_7",
                self.note_to_midi("F#7"): "Ed.NOTE_F_SHARP_7",
                self.note_to_midi("G7"): "Ed.NOTE_G_7",
                self.note_to_midi("G#7"): "Ed.NOTE_G_SHARP_7",
                self.note_to_midi("A7"): "Ed.NOTE_A_7",
                self.note_to_midi("A#7"): "Ed.NOTE_A_SHARP_7",
                self.note_to_midi("B7"): "Ed.NOTE_B_7",
                self.note_to_midi("C8"): "Ed.NOTE_C_8",
            }
       
    
     

         
        

    def note_to_midi(self, note):
        i = 0
        while i < len(note) and not note[i].isdigit():
            i += 1
        step = note[:i]
        octave = int(note[i:])
        return (octave + 1) * 12 + self.note_offsets[step]
    def transpose_to_edison(self, midi):
        while midi < self.edison_min:
            midi += 12
        while midi > self.edison_max:
            midi -= 12
        return midi


    def note_lenghts(self, event):
        dur = event.get("duration", 0)
        div = event.get("divisions", 1)

        if div <= 0:
            print(f"Warning: divisions is missing, defaulting to 1")
            return "Ed.NOTE_QUARTER"  
            

        quarter_notes = dur / div

        if quarter_notes >= 4.0:
            return "Ed.NOTE_WHOLE"
        elif quarter_notes >= 2.0:
            return "Ed.NOTE_HALF"
        elif quarter_notes >= 1.0:
            return "Ed.NOTE_QUARTER"
        elif quarter_notes >= 0.5:
            return "Ed.NOTE_EIGHTH"
        else:
            return "Ed.NOTE_SIXTEENTH"

    def createTXT(self, out_dir: str = "edisoncode") -> None:
        """Create a unique path for this run and initialize/clear the file."""
        os.makedirs(out_dir, exist_ok=True) 
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"edison_{ts}.edpy"
        self.path = os.path.join(out_dir, filename)

        # Initialize empty file so appends start clean
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("")

    def save_edpy_code(self, code_line: str) -> None:
        """Append ONE line to the file."""
        with open(self.path, "a", encoding="utf-8") as f:
            # ensure exactly one newline
            f.write(code_line.rstrip("\n") + "\n")

    def generate_to_file(self):

        self.createTXT()

        self.save_edpy_code("import Ed")
        self.save_edpy_code("Ed.EdisonVersion = Ed.V3")
        self.save_edpy_code("Ed.Tempo = Ed.TEMPO_FAST")
        self.save_edpy_code("Ed.DistanceUnits = Ed.CM")
        self.save_edpy_code("")

        # create play function (MUCH cleaner output)
        self.save_edpy_code("def play(note, duration):")
        self.save_edpy_code("    Ed.PlayTone(note, duration)")
        self.save_edpy_code("    while Ed.ReadMusicEnd() == Ed.MUSIC_NOT_FINISHED:")
        self.save_edpy_code("        pass")
        self.save_edpy_code("")

        # generate melody
        for event in self.notes:

            length = self.note_lenghts(event)

            if event["type"] == "rest":

                self.save_edpy_code(f"play(Ed.NOTE_REST, {length})")

            else:

                midi = self.note_to_midi(event["note"])
                midi = self.transpose_to_edison(midi)

                ed_note = self.midi_to_edison.get(midi)

                if ed_note is None:
                    continue

                self.save_edpy_code(f"play({ed_note}, {length})")

            
#Ed.PlayTone(Ed.NOTE_A_SHARP_6, Ed.NOTE_QUARTER)

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
        self.save_edpy_code("main()")"""
