import tkinter as tk
from dialogreader import DialogSystem  # Import the DialogSystem class

def start_level(level_num):
    """Starts a specific level with its own dialog and question file."""
    root = tk.Tk()
    root.geometry("800x600")  

    dialog_file = f"level{level_num}_dialog.json"
    question_file = f"level{level_num}_questions.json"

    dialog_system = DialogSystem(root, dialog_file, question_file)
    root.mainloop()
