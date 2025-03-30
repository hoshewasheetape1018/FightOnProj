import tkinter as tk
from PIL import Image, ImageTk  # PIL is needed for image handling
import pygame
import json
from questionchecker import check_answer

class DialogSystem:
    def __init__(self, root, dialog_file, question_file):
        self.root = root
        self.dialog_data = self.load_json(dialog_file)
        self.questions = self.load_json(question_file)
        self.current_index = 0
        self.level1_score = 0
        
        pygame.mixer.init()
        
        self.dialog_label = tk.Label(root, text="", wraplength=400)
        self.dialog_label.pack()
        
        self.sprite_label = tk.Label(root)  # Label for sprite images
        self.sprite_label.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_dialog)
        self.next_button.pack()
        
        self.input_entry = tk.Entry(root)
        self.enter_button = tk.Button(root, text="Enter", command=self.check_input)
        
        self.next_dialog()
        
    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
        
    def load_sprite(self, chara_name, expression):
        """Loads and displays the character sprite."""
        if chara_name and expression:
            sprite_path = f"assets/images/{chara_name}_{expression}.png"  # Adjust folder path if needed
            try:
                image = Image.open(sprite_path)
                image = image.resize((200, 200))  # Resize if needed
                self.sprite_image = ImageTk.PhotoImage(image)
                self.sprite_label.config(image=self.sprite_image)
                print(f"Displaying: {sprite_path}")  # Debugging message
            except FileNotFoundError:
                print(f"Sprite not found: {sprite_path}")  # Debugging message
                self.sprite_label.config(image="")  # Hide sprite if not found
        else:
            self.sprite_label.config(image="")  # Hide sprite if no character/expression
    
    def next_dialog(self):
        if self.current_index >= len(self.dialog_data):
            self.dialog_label.config(text="End of dialog.")
            self.next_button.config(state=tk.DISABLED)
            return
        
        line = self.dialog_data[self.current_index]
        chara_name = line.get("chara_name", "")
        dialog = line.get("dialog", "")
        expression = line.get("expression", None)
        sound = line.get("sound", None)
        input_key = line.get("input", None)
        
        # If dialog is a number, treat it as a question reference
        if str(dialog).isdigit():
            question_data = self.questions.get(str(dialog), {})
            dialog_text = question_data.get("question", "Unknown question")
            self.correct_answer = question_data.get("solution", "")
        else:
            dialog_text = dialog
            self.correct_answer = None  # No answer needed
        
        self.dialog_label.config(text=f"{chara_name}: {dialog_text}")
        
        # Load sprite (if available)
        self.load_sprite(chara_name, expression)
        
        if sound:
            pygame.mixer.Sound(f"assets/audio/{sound}.mp3").play()
        
        # Show input field if it's a question
        if self.correct_answer:
            self.next_button.pack_forget()
            self.input_entry.pack()
            self.enter_button.pack()
        else:
            self.next_button.pack()
            self.input_entry.pack_forget()
            self.enter_button.pack_forget()
        
        self.current_index += 1
        
    def check_input(self):
        user_answer = self.input_entry.get().strip()
        
        if check_answer(user_answer, self.correct_answer):
            self.level1_score += 10
            print("Correct! Score:", self.level1_score)
            self.dialog_label.config(text="Correct!", fg="green")
        else:
            print("Incorrect! Try again.")
            self.dialog_label.config(text="Incorrect! Try again.", fg="red")
            return  # Don't proceed to next dialog if wrong
        
        # Clear input and move to next dialog
        self.input_entry.delete(0, tk.END)
        self.next_button.pack()
        self.input_entry.pack_forget()
        self.enter_button.pack_forget()
        self.next_dialog()
        
root = tk.Tk()
dialog_system = DialogSystem(root, "dialog.json", "questions.json")
root.mainloop()
