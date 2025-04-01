import tkinter as tk

def get_score(self):
    """Get the total score based on the current level."""
    if self.current_level == 1:
        return self.level1_score
    elif self.current_level == 2:
        return self.level2_score
    elif self.current_level == 3:
        return self.level3_score
    return 0
def check_answer(player_input, expected_solution):
    """Checks the player's input dynamically."""
    expected_solution = expected_solution.strip()
    player_input = player_input.strip()

    print(f"DEBUG: Checking input: {repr(player_input)} against expected: {repr(expected_solution)}")

    # Handle print statements
    if expected_solution.startswith("print("):
        result = check_print_statement(player_input)
        print(f"DEBUG: Print statement check: {result}")
        return result

    # Handle if-statements and loops
    if expected_solution.startswith(("if", "for", "while")):
        result = check_code_structure(player_input, expected_solution)
        print(f"DEBUG: Code structure check: {result}")
        return result

    # Handle variable assignments
    if "=" in expected_solution:
        result = player_input == expected_solution  # Compare exact assignment statement
        print(f"DEBUG: Assignment check: {result}")
        return result

    # Handle mathematical expressions
    try:
        if not any(op in expected_solution for op in ["=", "print(", "if", "for", "while"]):  # Only eval pure expressions
            result = eval(player_input) == eval(expected_solution)
            print(f"DEBUG: Math evaluation result: {result}")
            return result
    except Exception as e:
        print(f"ERROR: Evaluation failed: {e}")
        return False

    return False

def check_print_statement(code):
    """Checks if the player's input is a valid print statement with a string."""
    code = code.strip()
    if code.startswith("print(") and code.endswith(")"):
        content = code[6:-1].strip()  # Extract content inside print()
        if (content.startswith("\"") or content.startswith("\'")) and (content.endswith("\"") or content.endswith("\'")):
            return True  # Ensure it is a string inside print
    return False

def check_code_structure(player_code, expected_code):
    """Checks if the player's code follows a valid structure (if/loops)."""
    player_lines = player_code.split("\n")
    expected_lines = expected_code.split("\n")

    if len(player_lines) < 2:
        return False  # A structured block needs at least two lines

    # Check if the first line matches the expected control statement (ignoring spaces)
    if player_lines[0].strip() != expected_lines[0].strip():
        return False

    # Ensure the second line is properly indented
    return player_lines[1].startswith((" ", "\t"))  # Check for indentation

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
