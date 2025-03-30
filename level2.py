import tkinter as tk
from dialogreader import DialogSystem


root = tk.Tk()
root.geometry("1000x750")  # Set window size
dialog_system = DialogSystem(root, "level2_dialog.json", "questions.json")
root.mainloop()
