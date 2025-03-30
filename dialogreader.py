import tkinter as tk
from PIL import Image, ImageTk  # PIL is needed for image handling
import pygame
import json
from questionchecker import check_input  # Import the function

class DialogSystem:
    def __init__(self, root, dialog_file, question_file):
        self.root = root
        self.dialog_data = self.load_json(dialog_file)
        self.questions = self.load_json(question_file)
        self.current_index = 0
        self.level1_score = 0
        
        pygame.mixer.init()

        # 🌟 Background Label (Placed behind everything)
        self.background_label = tk.Label(root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Covers entire window
        
        # 🌟 Sprite Label (For character images)
        self.sprite_label = tk.Label(root)
        self.sprite_label.pack()

        # 🌟 Dialog Box
        self.dialog_label = tk.Label(root, text="", wraplength=400, bg="white")
        self.dialog_label.pack()

        # 🌟 Buttons & Input
        self.next_button = tk.Button(root, text="Next", command=self.next_dialog)
        self.next_button.pack()
        
        self.input_entry = tk.Entry(root)
        # Replace `self.check_input` in Button command:
        self.enter_button = tk.Button(root, text="Enter", command=self.check_input_wrapper)

        # Start first dialog
        self.next_dialog()

    # Inside DialogSystem class
    def check_input_wrapper(self):
        """Passes user input to questionchecker.py for validation."""
        user_answer = self.input_entry.get().strip()
        check_input(user_answer, self.correct_answer, self)  # Pass self as the DialogSystem instance


        
        
    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
        
    def load_sprite(self, chara_name, expression):
        """Loads and displays the character sprite."""
        if chara_name and expression:
            sprite_path = f"assets/images/{chara_name}_{expression}.png"
            try:
                image = Image.open(sprite_path).resize((200, 200))  # Resize if needed
                self.sprite_image = ImageTk.PhotoImage(image)
                self.sprite_label.config(image=self.sprite_image)
                print(f"Displaying: {sprite_path}")  # Debugging message
            except FileNotFoundError:
                print(f"❌ Sprite not found: {sprite_path}")
                self.sprite_label.config(image="")  # Hide sprite if not found
        else:
            self.sprite_label.config(image="")  # Hide sprite if no character/expression
    
    def load_background(self, scene_name):
        """Fades into the new background from black."""
        if scene_name:
            bg_path = f"assets/images/{scene_name}.png"
            try:
                self.new_bg = Image.open(bg_path).resize((800, 600)).convert("RGBA")

                # Always fade from solid black
                self.old_bg = Image.new("RGBA", (800, 600), (0, 0, 0, 255))

                self.fade_step = 0  # Reset fade step
                self.fade_background()  # Start the fade effect
                
                print(f"🔄 Fading background to: {bg_path}")
            except FileNotFoundError:
                print(f"❌ Background not found: {bg_path}")

    def fade_background(self):
        """Gradually fades from black to the new background."""
        if self.fade_step >= 10:
            # Finalize background transition
            self.background_image = ImageTk.PhotoImage(self.new_bg)
            self.background_label.config(image=self.background_image)
            return  

        # Create a blended fade effect from black
        blended = Image.blend(self.old_bg, self.new_bg, self.fade_step / 10)

        self.background_fade_image = ImageTk.PhotoImage(blended)
        self.background_label.config(image=self.background_fade_image)

        self.fade_step += 1
        self.root.after(50, self.fade_background)  # Smooth transition effect

    def play_bgm(self, bgm_name):
        """Plays or changes background music."""
        bgm_path = f"assets/audio/{bgm_name}.mp3"
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            print(f"🎶 Playing BGM: {bgm_path}")
        except pygame.error:
            print(f"❌ BGM file not found: {bgm_path}")

 
    def next_dialog(self):
        """Displays the next line of dialog and updates visuals."""
        if self.current_index >= len(self.dialog_data):
            self.dialog_label.config(text="End of dialog.")
            self.next_button.config(state=tk.DISABLED)
            return
        
        line = self.dialog_data[self.current_index]
        chara_name = line.get("chara_name", "")
        dialog = line.get("dialog", "")
        expression = line.get("expression", None)
        sound = line.get("sound", None)
        scene = line.get("scene", None)  # Background change
        bgm = line.get("bgm", None)  # Check if there's a bgm change

        # 🌟 Play background music if specified
        if bgm:
            self.play_bgm(bgm)
            
        # 🌟 Update Background
        if scene:
            self.load_background(scene)
        
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


