import tkinter as tk
from PIL import Image, ImageTk
import pygame
import json
from questionchecker import check_input
import pyglet
from pointandclick import PointAndClick
import os

# Load custom font
pyglet.font.add_file('assets/fonts/Silver.ttf')
leveldone = False  # You can store this in gui.py or another shared module

class DialogSystem:
    def __init__(self, root, level, on_complete=None):
        self.root = root
        self.level = level  # Dynamically set level
        self.current_level = level  # Add this line to initialize current_level
        self.on_complete = on_complete
        self.player_name = os.getlogin()  # Get the PC's username
        self.dialog_data = self.load_json(f"level{level}_dialog.json")  # Load level-specific dialog JSON
        self.questions = self.load_json("questions.json")
        self.current_index = 0
        self.leveldone = False 
        self.level1_score = 0
        self.level2_score = 0
        self.level3_score = 0

        #Go to a part of the level. This is for debugging!!
        self.root.bind("1", lambda event: self.end_level())

        self.correct_answer = None
        self.bgm_playing = False  # Track whether the background music is playing
        pygame.mixer.init()
        self.objectives_list = []

        # UI Setup
        self.setup_ui()

        # Initialize PointAndClick system
        self.point_and_click = PointAndClick(self.canvas, self)

        # Start the dialog system
        self.next_dialog()

    def setup_ui(self):
        """Set up the UI components."""
        # Canvas for game background and sprites
        self.canvas_frame = tk.Frame(self.root, background="#E2CFEA")
        self.canvas_frame.place(relx=0.499, rely=0.5, anchor="center", width=678, height=460, x=-120, y=-50)
        self.canvas = tk.Canvas(self.canvas_frame, width=670, height=450, bd=-1, highlightthickness=0)
        self.canvas.pack()

        self.bg_image = None
        self.sprite_image = None

        # Dialog container frame
        self.dialog_frame = tk.Frame(self.root, bg="#25325E", highlightthickness=0)
        self.dialog_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=90, y=237)

        self.dialog_frame.columnconfigure(0, weight=3)
        self.dialog_frame.columnconfigure(1, weight=1)

        self.chara_name_label = tk.Label(self.dialog_frame, text="", font=('Silver', 20, 'bold'), bg="#25325E", fg="#E2CFEA", anchor="w")
        self.chara_name_label.grid(row=0, column=0, columnspan=2, sticky="we", padx=10, pady=(5, 0))

        self.dialog_label = tk.Label(self.dialog_frame, text="", wraplength=500, bg="#25325E", fg="#E2CFEA", font=('Silver', 15, 'bold'), anchor="w", justify="left")
        self.dialog_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.next_button = tk.Button(self.dialog_frame, text="Next", command=self.next_dialog, font=('Silver', 20, 'bold'), bg="white", fg="black", bd=0, relief="ridge", width=10)
        self.next_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        # Input Frame (hidden by default)
        self.input_frame = tk.Frame(self.root, bg="#082626", highlightthickness=0)
        self.text_box = tk.Text(self.input_frame, width=10, height=2, wrap="word", font=('Silver', 20, 'bold'), bg="white", fg="#25325E", highlightthickness=0)
        self.enter_button = tk.Button(self.input_frame, text="Enter", command=self.check_input_wrapper, font=('Silver', 20, 'bold'), bg="white", fg="black", bd=0, relief="ridge", width=10)
        self.text_box.pack(side="left", fill="both", expand=True, padx=(1, 10))
        self.enter_button.pack(side="right", padx=(2, 5))

        # Objectives container frame
        self.objectives_frame = tk.Frame(self.root, bg="#25325E", padx=3, pady=10)
        self.objectives_frame.place(relx=0.5, rely=0.5, anchor="center", x= 349, y=-150)
        self.objectives_label = tk.Label(self.objectives_frame, text="", font=('Silver', 15, 'bold'), fg="white", bg="#25325E", justify="left")
        self.objectives_label.pack(anchor="w")
        
        self.update_objectives_display()

    def update_objectives(self, new_objective):
        """Updates the objectives dynamically."""
        if new_objective not in self.objectives_list:
            self.objectives_list.append(new_objective)
            self.update_objectives_display()

    def update_objectives_display(self):
        """Displays the current objectives."""
        self.objectives_label.config(text="\n".join(f"- {obj}" for obj in self.objectives_list))

    def load_json(self, filename):
        """Load a JSON file."""
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def check_input_wrapper(self):
        """Wrapper to check input answers."""
        user_answer = self.text_box.get("1.0", tk.END).strip()
        check_input(user_answer, self.correct_answer, self)

    def jump_to_dialog(self, index):
        """Jump to a specific dialog by index."""
        if index < 0 or index >= len(self.dialog_data):
            print("Invalid dialog index")
            return
        self.current_index = index
        self.next_dialog()

    def next_dialog(self, dialog_index=None):
        """Proceed to the next dialog or jump to a specific index."""
        if dialog_index is not None:
            self.current_index = dialog_index

        if self.current_index >= len(self.dialog_data):
            self.dialog_label.config(text="End of dialog.")
            self.next_button.config(state=tk.DISABLED)
            # Set leveldone to True when dialog is finished
            self.leveldone = True
            
            # Call the completion callback if provided
            if self.on_complete:
                self.on_complete(self)
                        
            print("Calling finish button level, level done == True", self.leveldone)
            return
    

        line = self.dialog_data[self.current_index]
        chara_name = line.get("chara_name", "")
        dialog = line.get("dialog", "")
        expression = line.get("expression", None)
        sound = line.get("sound", None)
        scene = line.get("scene", None)
        bgm = line.get("bgm", None)
        hide = line.get("hide", None)  # Ensure hide is retrieved correctly
        objective = line.get("objective", None)  # Get objective from the current dialog

        if "{player_name}" in dialog:
            dialog = dialog.replace("{player_name}", self.player_name)
            
        if bgm == "none":
            pygame.mixer.music.stop()

        if bgm:
            self.play_bgm(bgm)

        if scene:
            self.load_background(scene)

        if str(dialog).isdigit():
            question_data = self.questions.get(str(dialog), {})
            dialog_text = question_data.get("question", "Unknown question")
            self.correct_answer = question_data.get("solution", "")
            self.show_input_box()
        else:
            dialog_text = dialog
            self.correct_answer = None
            self.hide_input_box()

        self.chara_name_label.config(text=chara_name)
        self.dialog_label.config(text=dialog_text)
        self.load_sprite(chara_name, expression)

        if sound:
            try:
                pygame.mixer.Sound(f"assets/audio/{sound}.mp3").play()
            except pygame.error:
                pass

        # Here we check the hide condition
        if hide and int(hide) == 1:
            self.hide_dialog_box(scene)
        elif hide is not None and int(hide) == 0:  # Ensure the correct hide condition
            self.show_dialog_box()

        # If an objective is present, add it to the list and update the display
        if objective:
            self.update_objectives(objective)

        self.current_index += 1


    def load_sprite(self, chara_name, expression):
        """Load character sprite."""
        if chara_name and expression:
            sprite_path = f"assets/images/{chara_name}_{expression}.png"
            try:
                image = Image.open(sprite_path).resize((670, 450)).convert("RGBA")
                self.sprite_image = ImageTk.PhotoImage(image)
                self.canvas.delete("sprite")
                self.canvas.create_image(340, 240, image=self.sprite_image, tags="sprite")
            except FileNotFoundError:
                self.canvas.delete("sprite")

    def load_background(self, scene_name):
        """Load background image for the scene."""
        if scene_name:
            bg_path = f"assets/images/{scene_name}.png"
            try:
                image = Image.open(bg_path).resize((670, 450)).convert("RGBA")
                self.bg_image = ImageTk.PhotoImage(image)
                self.canvas.delete("background")
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw", tags="background")
            except FileNotFoundError:
                pass

    def play_bgm(self, bgm_name):
        """Play background music."""
        bgm_path = f"assets/audio/{bgm_name}.mp3"
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  # Loop the music
            self.bgm_playing = True  # Music is now playing
        except pygame.error:
            pass

    def show_input_box(self):
        """Display the input box for questions."""
        self.next_button.grid_remove()
        self.input_frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=60, y=325)

    def hide_input_box(self):
        """Hide the input box."""
        self.next_button.grid()
        self.input_frame.place_forget()

    def hide_dialog_box(self, scene):
        """Hide the dialog box and trigger PointAndClick interaction."""
        self.dialog_frame.place_forget()
        self.point_and_click.hide_dialog_box(scene)

    def show_dialog_box(self):
        """Show the current dialog and handle scene transitions."""
        self.dialog_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=90, y=237)
        print("Showing dialog box")



    def get_score(self):
        """Get the current score based on the level."""
        if self.current_level == 1:
            return self.level1_score
        elif self.current_level == 2:
            return self.level2_score
        elif self.current_level == 3:
            return self.level3_score
        
    def end_level(self):
        """End the current level and jump to the end dialog."""
        print("Going to end")
        self.next_dialog(30)  # Jump to the 9th dialog (which is the end)