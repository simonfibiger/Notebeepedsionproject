import tkinter as tk
from tkinter import filedialog

def ask_image_path():
    root = tk.Tk()
    root.overrideredirect(True)   # no border, no display
    root.withdraw()                # hide completely

    file_path = filedialog.askopenfilename(title="selefct a pdf file", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    print(file_path)
    return file_path
ask_image_path()