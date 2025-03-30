import json
import ast
import re

def check_answer(player_input, expected_solution):
    """Checks the player's input dynamically."""
    expected_solution = expected_solution.strip()
    player_input = player_input.strip()

    # If expected solution is a print statement
    if expected_solution.startswith("print("):
        return check_print_statement(player_input)

    # If expected solution is an if-statement or loop, check structure
    if expected_solution.startswith(("if", "for", "while")):
        return check_indentation(player_input)

    # If expected solution is a math expression, evaluate it
    try:
        return eval(player_input) == eval(expected_solution)
    except:
        return False

def check_print_statement(code):
    """Checks if the player's input is a valid print statement with a string."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                # Ensure print has at least one argument that is a string
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    return True
        return False
    except:
        return False

def check_indentation(code):
    """Checks if the player used proper indentation for if/loops."""
    lines = code.split("\n")
    if len(lines) < 2:
        return False  # If there's no indented line, it's wrong
    return re.match(r'^\s+', lines[1]) is not None  # Second line must have indentation

def check_input(player_input, correct_answer, dialog_system):
    """
    Checks the player's answer, updates the score, and advances dialogue if correct.
    """
    if check_answer(player_input, correct_answer):
        dialog_system.level1_score += 10
        print("✅ Correct! Score:", dialog_system.level1_score)
        dialog_system.dialog_label.config(text="Correct!", fg="green")
        dialog_system.input_entry.delete(0, 'end')  # Clear input
        dialog_system.next_dialog()  # Move to next dialogue
    else:
        print("❌ Incorrect! Try again.")
        dialog_system.dialog_label.config(text="Incorrect! Try again.", fg="red")
