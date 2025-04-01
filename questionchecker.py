import tkinter as tk

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
    """
    Checks the player's answer, updates the score, and advances dialogue if correct.
    """
    if check_answer(player_input, correct_answer):
        dialog_system.level1_score += 10
        print("✅ Correct! Score:", dialog_system.level1_score)
        dialog_system.text_box.delete("1.0", tk.END)  # For Text widgets
        dialog_system.next_dialog()  # Move to next dialogue
    else:
        print("❌ Incorrect! Try again.")
        dialog_system.dialog_label.config(text="Incorrect! Try again.")
