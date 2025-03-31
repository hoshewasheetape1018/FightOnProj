class ObjectivesManager:
    def __init__(self, objectives_label):
        """Initialize with a label for displaying objectives."""
        self.objectives_label = objectives_label
        self.objectives_data = {}  # Stores objectives for each level
        self.current_objectives = []  # Active objectives list
        self.current_index = 0  # Track which objective is active

    def set_level_objectives(self, level_name, objectives):
        """Store objectives for a specific level."""
        self.objectives_data[level_name] = objectives

    def load_objectives_for_level(self, level_name):
        """Load the objectives for a given level and reset progress."""
        self.current_objectives = self.objectives_data.get(level_name, [])
        self.current_index = 0
        self.update_objectives_display()

    def update_objectives(self):
        """Show the next objective in the list, if available."""
        if self.current_index < len(self.current_objectives):
            self.current_index += 1  # Move to the next objective
            self.update_objectives_display()

    def update_objectives_display(self):
        """Update the objectives label with the current objectives."""
        displayed_objectives = self.current_objectives[:self.current_index]
        self.objectives_label.config(text="\n".join(f"- {obj}" for obj in displayed_objectives))
