import tkinter as tk
from PIL import Image, ImageTk
import pygame
import json
from questionchecker import check_input 
import pyglet

pyglet.font.add_file('assets/fonts/Silver.ttf')

class DialogSystem:
    def __init__(self, root, dialog_file, question_file):
        self.root = root
        self.dialog_data = self.load_json(dialog_file)
        self.questions = self.load_json(question_file)
        self.current_index = 0
        self.level1_score = 0
        self.correct_answer = None

        pygame.mixer.init()

        # Canvas setup
        self.canvas_frame = tk.Frame(root, background="#E2CFEA")
        self.canvas_frame.place(relx=0.499, rely=0.5, anchor="center", width=678, height=460, x=-120, y=-50)

        self.canvas = tk.Canvas(self.canvas_frame, width=670, height=450, bd=-1, highlightthickness=0)
        self.canvas.pack()

        self.bg_image = None
        self.sprite_image = None

        # Dialog Container Frame
        self.dialog_frame = tk.Frame(root, bg="#25325E", highlightthickness=0)
        self.dialog_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=90, y=237)

        self.dialog_frame.columnconfigure(0, weight=3)
        self.dialog_frame.columnconfigure(1, weight=1)

        self.chara_name_label = tk.Label(self.dialog_frame, text="", font=('Silver', 20, 'bold'), 
                                         bg="#25325E", fg="#E2CFEA", anchor="w")
        self.chara_name_label.grid(row=0, column=0, columnspan=2, sticky="we", padx=10, pady=(5, 0))

        self.dialog_label = tk.Label(self.dialog_frame, text="", wraplength=500, bg="#25325E", 
                                     fg="#E2CFEA", font=('Silver', 15, 'bold'), anchor="w", justify="left")
        self.dialog_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.next_button = tk.Button(self.dialog_frame, text="Next", command=self.next_dialog, 
                                     font=('Silver', 20, 'bold'), bg="white", fg="black", bd=0, relief="ridge", width=10)
        self.next_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        # Input Frame (Hidden by default)
        self.input_frame = tk.Frame(root, bg="#082626", highlightthickness=0)
        self.text_box = tk.Text(self.input_frame, width=10, height=2, wrap="word", font=('Silver', 20, 'bold'),
                                bg="white", fg="#25325E", highlightthickness=0)
        self.enter_button = tk.Button(self.input_frame, text="Enter", command=self.check_input_wrapper,
                                      font=('Silver', 20, 'bold'), bg="white", fg="black", bd=0, relief="ridge", width=10)
        self.text_box.pack(side="left", fill="both", expand=True, padx=(1, 10))
        self.enter_button.pack(side="right", padx=(2, 5))
#---------------------------------------------------------------------------

        # Objectives Container Frame
        self.objectives_frame = tk.Frame(root, bg="#25325E", padx=3, pady=10)
        self.objectives_frame.place(relx=0.5, rely=0.5, anchor="center", x= 349, y=-150)


        # Objectives List Label (Multi-line)
        self.objectives_label = tk.Label(self.objectives_frame, text="", 
                                        font=('Silver', 15, 'bold'), fg="white", bg="#25325E", justify="left")
        self.objectives_label.pack(anchor="w")

        def update_objectives(new_objectives):
            """Updates the objectives dynamically."""
            self.objectives_label.config(text="\n".join(f"- {obj}" for obj in new_objectives))

        # Example usage:
        objectives_list = ["Learn how to print in \nconsole", "Learn variables", "Learn operations"]
        update_objectives(objectives_list)

#---------------------------------------------------------------------------

        self.next_dialog()

    def check_input_wrapper(self):
        user_answer = self.text_box.get("1.0", tk.END).strip()
        check_input(user_answer, self.correct_answer, self)

    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_sprite(self, chara_name, expression):
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
        bgm_path = f"assets/audio/{bgm_name}.mp3"
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

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
        scene = line.get("scene", None)
        bgm = line.get("bgm", None)
        event = line.get("event", None)

        if event and hasattr(self, event):
            getattr(self, event)()

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

        self.current_index += 1

    def show_input_box(self):
        self.next_button.grid_remove()
        self.input_frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=60, y=325)

    def hide_input_box(self):
        self.next_button.grid()
        self.input_frame.place_forget()

