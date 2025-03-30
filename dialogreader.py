import tkinter as tk
from PIL import Image, ImageTk
import pygame
import json
from questionchecker import check_input 

class DialogSystem:
    def __init__(self, root, dialog_file, question_file):
        self.root = root
        self.dialog_data = self.load_json(dialog_file)
        self.questions = self.load_json(question_file)
        self.current_index = 0
        self.level1_score = 0

        pygame.mixer.init()

        # Create Canvas for background and sprite
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="black")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Image references to prevent garbage collection
        self.bg_image = None
        self.sprite_image = None

        # Dialog Container Frame
        self.dialog_frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
        self.dialog_frame.place(relx=0.5, rely=0.9, anchor="center", width=700, height=150)

        # Character Name (Separate Row)
        self.chara_name_label = tk.Label(self.dialog_frame, text="", font=("Arial", 14, "bold"), bg="white", fg="black")
        self.chara_name_label.pack(pady=(10, 0))  # Added padding to separate from edges

        self.dialog_label = tk.Label(self.dialog_frame, text="", wraplength=600, bg="white", fg="black", font=("Arial", 16))
        self.dialog_label.pack(pady=(5, 10), padx=10)

        # Input and Buttons Frame (inside dialog_frame)
        self.input_frame = tk.Frame(self.dialog_frame, bg="white")
        self.input_frame.pack(pady=5)

        # Input Field
        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_entry.pack(side="left", padx=5)

        # Enter Button
        self.enter_button = tk.Button(self.input_frame, text="Enter", command=self.check_input_wrapper)
        self.enter_button.pack(side="left", padx=5)

        # Next Button (Placed Below Dialog)
        self.next_button = tk.Button(self.dialog_frame, text="Next", command=self.next_dialog)
        self.next_button.pack(pady=5)

        # Start first dialog
        self.next_dialog()

    def check_input_wrapper(self):
        """Passes user input to questionchecker.py for validation."""
        user_answer = self.input_entry.get().strip()
        check_input(user_answer, self.correct_answer, self)

    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_sprite(self, chara_name, expression):
        """Loads and displays the character sprite on the canvas."""
        if chara_name and expression:
            sprite_path = f"assets/images/{chara_name}_{expression}.png"
            try:
                image = Image.open(sprite_path).convert("RGBA")
                image = image.resize((1000, 750))  # Resize as needed
                self.sprite_image = ImageTk.PhotoImage(image)  # Keep reference

                # Remove old sprite and add new one
                self.canvas.delete("sprite")  # Remove previous sprite
                self.canvas.create_image(400, 400, image=self.sprite_image, tags="sprite")  # Centered sprite
                print(f"Displaying: {sprite_path}")
            except FileNotFoundError:
                print(f"❌ Sprite not found: {sprite_path}")
                self.canvas.delete("sprite")  # Hide sprite if not found
        else:
            self.canvas.delete("sprite")  # Hide sprite if no character/expression

    def load_background(self, scene_name):
        """Loads and displays the background image on the canvas."""
        if scene_name:
            bg_path = f"assets/images/{scene_name}.png"
            try:
                image = Image.open(bg_path).resize((1000, 750)).convert("RGBA")
                self.bg_image = ImageTk.PhotoImage(image)

                # Remove old background and add new one
                self.canvas.delete("background")  # Remove previous background
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw", tags="background")
                print(f"Background changed to: {bg_path}")
            except FileNotFoundError:
                print(f"❌ Background not found: {bg_path}")

    def play_bgm(self, bgm_name):
        """Plays or changes background music."""
        bgm_path = f"assets/audio/{bgm_name}.mp3"
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
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
        scene = line.get("scene", None)
        bgm = line.get("bgm", None)
        event = line.get("event", None)

        # Execute Event if exists
        if event and hasattr(self, event):
            getattr(self, event)()

        if bgm:
            self.play_bgm(bgm)

        if scene:
            self.load_background(scene)

        # Check if dialog is a number (indicating a question)
        if str(dialog).isdigit():
            question_data = self.questions.get(str(dialog), {})
            dialog_text = question_data.get("question", "Unknown question")
            self.correct_answer = question_data.get("solution", "")
        else:
            dialog_text = dialog
            self.correct_answer = None

        # Update UI elements separately
        self.chara_name_label.config(text=chara_name)  # Name stays separate
        self.dialog_label.config(text=dialog_text)  # Show either question or dialogue

        self.load_sprite(chara_name, expression)

        if sound:
            try:
                pygame.mixer.Sound(f"assets/audio/{sound}.mp3").play()
            except pygame.error:
                print(f"❌ Sound file not found: assets/audio/{sound}.mp3")

        # Input Handling (Show Input Box if Question is Asked)
        if self.correct_answer:
            self.next_button.pack_forget()  # Hide Next Button
            self.input_entry.pack()
            self.enter_button.pack()
        else:
            self.next_button.pack()  # Show Next Button
            self.input_entry.pack_forget()
            self.enter_button.pack_forget()

        self.current_index += 1
