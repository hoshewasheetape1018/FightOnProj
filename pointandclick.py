import tkinter as tk
from PIL import Image, ImageTk


class PointAndClick:
    def __init__(self, root):
        self.root = root
        self.root.title("Point and Click System")
        
        self.scenes = {
            "hallway": "hallway.png",
            "classroom": "classroom.png",
            "library entrance": "library.png",
            "library": "insidelibrary.png",
            "cat floor": "tom_bg.png",
            "bookshelf": "bookshelves.png",
            "bookshelf 2": "assets/images/bookshelves2.png",
            "librarian desk": "librariandesk.png",
            "secret room": "secretroom.png",
            "security office": "security_office.png"
        }
        
        # Scene hitboxes (x1, y1, x2, y2)
        self.hitboxes = {
            "bookshelf 2": [(100, 200, 300, 400, "Secret Book")],
        }
        
        self.current_scene = "bookshelf 2"  # Set initial scene
        
        
        self.load_scene(self.current_scene)
        
        # Bind events
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Button-1>", self.on_click)
        
    def load_scene(self, scene):
        """Load scene background and draw hitboxes."""
        image_path = self.scenes.get(scene, "default.png")
        self.bg_image = Image.open(image_path).resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        
        # Draw hitboxes
        self.rectangles = []
        if scene in self.hitboxes:
            for (x1, y1, x2, y2, name) in self.hitboxes[scene]:
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2, tags=name)
                self.rectangles.append((rect, name))
        
    def on_hover(self, event):
        """Change cursor when hovering over hitbox."""
        self.canvas.config(cursor="")
        for (rect, name) in self.rectangles:
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.canvas.config(cursor="hand2")
                return
        
    def on_click(self, event):
        """Detect clicks on hitboxes."""
        for (rect, name) in self.rectangles:
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                print(f"Clicked on: {name}")
                return
