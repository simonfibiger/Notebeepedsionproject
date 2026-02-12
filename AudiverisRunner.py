import subprocess
import os
import time


class AudiverisRunner:
    """Responsible only for running Audiveris on a PDF."""

    def __init__(self, exe_path: str, output_dir: str):
        self.exe_path = exe_path
        self.output_dir = output_dir

    def process_pdf_to_mxl(self, pdf_path: str):
        
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

       
        subprocess.run([
            exe_path,
            "-batch",
            "-export",
            "-output",
            rf"{str(out_dir)}",
            rf"{str(pdf)}"
        ])
        time.sleep(5)  # give Audiveris time

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
        print("[AudiverisRunner] Processing complete.")

