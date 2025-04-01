class PointAndClick:
    def __init__(self, canvas, dialog_system):
        self.canvas = canvas
        self.dialog_system = dialog_system  # Store the DialogSystem instance for access
        self.hitboxes = {
            "hallway": [(95, 100, 200, 400, "Classroom")],
            "classroom": [(40, 450, 150, 200, "Hallway"), (200, 100, 380, 200, "Chalkboard")],
        }
        self.current_scene = "hallway"
        self.rectangles = []  # Keep track of created hitboxes
        self.overlay = None  # Overlay layer
        self.text_labels = {}  # Store references to text labels inside hitboxes

        # Bind events to the passed canvas
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Button-1>", self.on_click)

    def hide_dialog_box(self, scene):
        """Hide dialog box and show the corresponding scene's hitboxes."""
        # Clear existing hitboxes and overlay
        for rect, _ in self.rectangles:
            self.canvas.delete(rect)
        self.rectangles.clear()

        if self.overlay:
            self.canvas.delete(self.overlay)  # Remove the existing overlay

        # Create a semi-transparent black overlay
        self.overlay = self.canvas.create_rectangle(0, 0, 800, 600, fill="")

        # Draw red hitboxes for the current scene
        for (x1, y1, x2, y2, name) in self.hitboxes.get(scene, []):
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="", tags=name)
            self.rectangles.append((rect, name))

            # Create a text label inside the hitbox, initially hidden, The math puts it in the center of the hitbox and - 10 subtracts for x as adjustment
            label = self.canvas.create_text((((x1 + x2) / 2)- 10), (y1 + y2) / 2, text=name, fill="white", font=("Silver", 20, 'bold'), state="hidden")
            self.text_labels[name] = label  # Store reference to the label

            # Bind hover events to show/hide the text when the mouse enters or leaves the hitbox
            self.canvas.tag_bind(rect, "<Enter>", lambda event, name=name: self.on_enter(event, name))
            self.canvas.tag_bind(rect, "<Leave>", lambda event, name=name: self.on_leave(event, name))

        # Raise hitboxes to ensure they are on top of the overlay
        for rect, _ in self.rectangles:
            self.canvas.tag_raise(rect)

    def on_hover(self, event):
        """Change cursor when hovering over hitbox."""
        self.canvas.config(cursor="arrow")
        for (rect, name) in self.rectangles:
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.canvas.config(cursor="hand2")
                return  # Only show one cursor at a time

    def on_enter(self, event, name):
        """Display text inside the hitbox when hovering."""
        self.canvas.itemconfig(self.text_labels[name], state="normal")  # Show text

    def on_leave(self, event, name):
        """Hide text inside the hitbox when not hovering."""
        self.canvas.itemconfig(self.text_labels[name], state="hidden")  # Hide text

    def on_click(self, event):
        """Detect clicks on hitboxes and trigger events."""
        for (rect, name) in self.rectangles:
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                print(f"Clicked on: {name}")
                self.trigger_dialog(name)
                return

    def trigger_dialog(self, event_trigger):
        """Trigger the dialog jump based on the event."""
        if event_trigger == "Classroom":
            print("Jumping to the Classroom!")
            self.dialog_system.next_dialog(8)  # Jump to the dialog index for classroom
            self.current_scene = "classroom"  # Change scene to classroom
            self.hide_dialog_box("classroom")  # Redraw the hitboxes for classroom
        elif event_trigger == "Hallway":
            print("Jumping to the Hallway!")
            self.dialog_system.next_dialog(7)  # Jump to the dialog index for hallway
            self.current_scene = "hallway"  # Change scene to hallway
            self.hide_dialog_box("hallway")  # Redraw the hitboxes for hallway
        elif event_trigger == "Chalkboard":
            print("Interacting with the Chalkboard!")
            # Trigger dialog interaction or other logic for chalkboard interaction
            self.dialog_system.next_dialog(9)  # Jump to dialog about interacting with the chalkboard
