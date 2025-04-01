import tkinter as tk

def get_score(self):
    """Get the total score based on the current level."""
    if self.current_level == 1:
        return self.level1_score
    elif self.current_level == 2:
        return self.level2_score
    elif self.current_level == 3:
        return self.level3_score

def check_answer(player_input, expected_solution):
    """Checks the player's input dynamically."""
    expected_solution = expected_solution.strip()
    player_input = player_input.strip()

    print(f"DEBUG: Checking input: '{player_input}' against expected: '{expected_solution}'")

    # If expected solution is a print statement
    if expected_solution.startswith("print("):
        result = check_print_statement(player_input)
        print(f"DEBUG: Print statement check: {result}")
        return result

    # If expected solution is an if-statement or loop, check structure
    if expected_solution.startswith(("if", "for", "while")):
        result = check_indentation(player_input)
        print(f"DEBUG: Indentation check: {result}")
        return result

    # If expected solution is a math expression, evaluate it
    try:
        result = eval(player_input) == eval(expected_solution)
        print(f"DEBUG: Math evaluation result: {result}")
        return result
    except Exception as e:
        print(f"ERROR: Evaluation failed: {e}")
        return False

def check_print_statement(code):
    """Checks if the player's input is a valid print statement with a string."""
    code = code.strip()
    if code.startswith("print(") and code.endswith(")"):
        content = code[6:-1].strip()  # Extract content inside print()
        if content.startswith("\"") and content.endswith("\""):
            return True  # Ensure it is a string inside print
    return False

def check_indentation(code):
    """Checks if the player used proper indentation for if/loops."""
    lines = code.split("\n")
    if len(lines) < 2:
        return False  # If there's no indented line, it's wrong
    return lines[1].startswith(" ") or lines[1].startswith("\t")  # Check for leading spaces or tabs
def check_input(player_input, correct_answer, dialog_system):
    """Checks the player's answer and updates the score."""
    if check_answer(player_input, correct_answer):
        # Update score based on the current level
        current_level = dialog_system.current_level
        if current_level == 1:
            dialog_system.level1_score += 10
        elif current_level == 2:
            dialog_system.level2_score += 10
        elif current_level == 3:
            dialog_system.level3_score += 10
        

        dialog_system.text_box.delete("1.0", tk.END)  # Clear the text box
        dialog_system.next_dialog()  # Proceed to next dialog
