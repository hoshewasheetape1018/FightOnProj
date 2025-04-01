import tkinter as tk
from dialogreader import DialogSystem

# Initialize Level 1 with its own dialog & questions


root = tk.Tk()
root.geometry("1000x750")  # Set window size
dialog_system = DialogSystem(root, level=1)

root.mainloop()

