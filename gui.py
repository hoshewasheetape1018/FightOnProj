'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
=====================================================================
                            GUI by Ocampo
=====================================================================




=============================== Notes ===============================




## Debug
    > Unlocked using Konami Code
        > Konami Code: Up, Up, Down, Down,
        Left, Right, Left, Right, B, A
    > Unlocks all Levels




=====================================================================
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




#----------------------------- Modules -----------------------------#
import tkinter as tk
import pyglet
import sqlite3
from dialogreader import DialogSystem
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import pygame
import questionchecker


# Global leveldone to track if the level is done
global leveldone  
leveldone = False  # Initially set to False


#------------------------  Files / Functions ------------------------#
pyglet.font.add_file('assets/fonts/Silver.ttf')




#------------------------- Basic Window Def -------------------------#
root = tk.Tk()
root.title('FightOn')
root.configure(bg='black')
root.iconbitmap('assets/images/FightOn.ico')

window_width = 1000
window_height = 750
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = 0

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#--------------------------- Collections ---------------------------#
images = {}

#------------------------- Global Variables ------------------------#
global main_canvas, leaderboard_canvas, current_level
level1_score = 0  # Score for level 1
level2_score = 0  # Score for level 2
level3_score = 0  # Score for level 3

#-------------------------- Level Triggers -------------------------#
level_unlocked = [False, False, False]  # Level 1, 2, 3 unlocked
current_level = None

#--------------------------- Konami Code ---------------------------#
konami_code = [
    "Up", "Up", "Down", "Down",
    "Left", "Right", "Left", "Right",
    "b", "a"
]

input_sequence = []

#------------------------- Helper Functions ------------------------#
def create_button(text, command, width=25, height=1, font=('Silver', 20, 'bold'), bg='white'):
    return tk.Button(root, text=text, command=command, height=height, width=width, padx=1, pady=1, font=font, bg=bg)

def create_canvas(bg_image):
    canvas = tk.Canvas(root, width=1000, height=750)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    return canvas


def on_level_complete(dialog_system):
    """Callback function to be called when a level is completed"""
    global current_level
    score = dialog_system.get_score()  # Get the score directly from dialog_system
    
    print("Level completed with score:", score)
    
    # Update level-specific scores
    if current_level == 1:
        global level1_score
        level1_score = score
    elif current_level == 2:
        global level2_score
        level2_score = score
    elif current_level == 3:
        global level3_score
        level3_score = score
    
    # Clean up dialog system resources
    cleanup_dialog_system(dialog_system)
    
    # Show username popup after cleanup
    display_level_complete_screen(score)


def cleanup_dialog_system(dialog_system):
    """Clean up dialog system resources similar to gotomainmenu function"""
    # Clear canvas
    if hasattr(dialog_system, 'canvas'):
        dialog_system.canvas.delete('all')
    
    # Stop background music if it's playing
    if dialog_system.bgm_playing:
        pygame.mixer.music.stop()  # Stop the music
        dialog_system.bgm_playing = False  # Set bgm_playing to False

    # Hide frames instead of destroying them
    if hasattr(dialog_system, 'canvas_frame'):
        dialog_system.canvas_frame.place_forget()
    
    if hasattr(dialog_system, 'dialog_frame'):
        dialog_system.dialog_frame.place_forget()
    
    if hasattr(dialog_system, 'objectives_frame'):
        dialog_system.objectives_frame.place_forget()
    
    if hasattr(dialog_system, 'input_frame'):
        dialog_system.input_frame.place_forget()


#------------------------- Leaderboard Setup -----------------------#
def leaderboarddb_setup():
    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level INTEGER,
                username TEXT,
                score INTEGER
            )
        ''')
        conn.commit()




#--------------------------- Title Screen --------------------------#
def main():
    global main_canvas
    global leveldone  # Ensure you have access to the global variable

    images['main_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/main_bg.jpg"))
    main_canvas = create_canvas(images['main_bg'])
    main_canvas.pack(expand=True)




    main_canvas.create_window(500, 350, anchor="n", window=create_button("Play", levelselect))
    main_canvas.create_window(500, 440, anchor="n", window=create_button("Leaderboard", show_leaderboard))
    main_canvas.create_window(500, 530, anchor="n", window=create_button("Exit", root.quit))


#------------------------- Show Leaderboard ------------------------#
def show_leaderboard():
    global leaderboard_canvas
    if 'leaderboard_canvas' not in globals():
        images['leaderboard_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/leaderboard_bg.jpg"))
        leaderboard_canvas = create_canvas(images['leaderboard_bg'])




    leaderboard_canvas.delete("all")
    leaderboard_canvas.create_image(0, 0, image=images['leaderboard_bg'], anchor="nw")




    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        scores = {level: cursor.execute("SELECT username, score FROM scores WHERE level = ? ORDER BY score DESC LIMIT 5", (level,)).fetchall() for level in range(1, 4)}




    for i, (level, level_scores) in enumerate(scores.items(), start=1):
        leaderboard_canvas.create_text(200 + (i - 1) * 300, 250, text=f"Level {level}", font=('Silver', 45, 'bold'), fill='white')
        for j, (username, score) in enumerate(level_scores):
            leaderboard_canvas.create_text(200 + (i - 1) * 300, 340 + j * 50, text=f"{j + 1}. {username}: {score}", font=('Silver', 20), fill='white')




    leaderboard_canvas.create_window(250, 600, anchor="n", window=create_button("Reset Scores", reset, width=20))
    leaderboard_canvas.create_window(750, 600, anchor="n", window=create_button("Back", back_to_main, width=20))




    main_canvas.pack_forget()
    leaderboard_canvas.pack(expand=True)




#------------------------ Reset Leaderboard --------------------------#
def reset():
    resetpop = tk.Toplevel(root)
    resetpop.title("Reset Scores")
    resetpop.configure(bg='black')
    resetpop.iconbitmap('assets/images/FightOn.ico')
    resetpop.geometry("600x210+{}+0".format((resetpop.winfo_screenwidth() // 2) - 300))




    tk.Label(resetpop, text="Which level do you want to reset?", font=('Silver', 25), bg='black', fg='white').pack(pady=10)




    frame = tk.Frame(resetpop, bg='black')
    frame.pack(pady=5)




    for i in range(1, 4):
        tk.Button(frame, text=f"Level {i}", command=lambda level=i: reset_scores(level), width=10, height=1, font=('Silver', 15, 'bold')).grid(row=0, column=i-1, padx=10)




    tk.Button(frame, text="All", command=lambda: reset_scores('all'), width=10, height=1, font=('Silver', 14, 'bold')).grid(row=1, column=0, columnspan=3, pady=10, padx=10)




def reset_scores(level):
    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        if level == 'all':
            cursor.execute("DELETE FROM scores")
            messagebox.showinfo("Reset Scores", "All scores have been reset.")
        else:
            cursor.execute("DELETE FROM scores WHERE level = ?", (level,))
            messagebox.showinfo("Reset Scores", f"Level {level} scores have been reset.")




    show_leaderboard()




#---------- Back to Main Menu ----------#
def back_to_main():
    leaderboard_canvas.pack_forget()
    main_canvas.pack(expand=True)




#---------- Level Select Screen ----------#
def levelselect():
    global levelselect_canvas
    if 'levelselect_canvas' not in globals():
        images['levelselect_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/levelselect_bg.jpg"))
        levelselect_canvas = create_canvas(images['levelselect_bg'])
        levelselect_canvas.bind("<Key>", check_konami_code)
        levelselect_canvas.focus_set()




    update_lvlselectbtns()
    main_canvas.pack_forget()
    levelselect_canvas.pack(expand=True)




#---------- Check Konami Code ----------#
def check_konami_code(event):
    global input_sequence
    input_sequence.append(event.keysym)
    if len(input_sequence) > len(konami_code):
        input_sequence.pop(0)


    if input_sequence == konami_code:
        debug_features()
        messagebox.showinfo("True Gamer", "Congratulations! You have unlocked all the levels.")




#---------- Unlock Debug Features ----------#
def debug_features():
    global level_unlocked
    level_unlocked[1] = True
    level_unlocked[2] = True
    update_lvlselectbtns()




#---------- Update Level Select Buttons ----------#
def update_lvlselectbtns():
    levelselect_canvas.delete("all")
    levelselect_canvas.create_image(0, 0, image=images['levelselect_bg'], anchor="nw")




    level_buttons = [
        (1, level1, "Level 1", 'white'),  # Level 1 is always unlocked
        (2, level2locked if not level_unlocked[1] else level2unlocked, "Level 2", 'darkgray' if not level_unlocked[1] else 'white'),
        (3, level3locked if not level_unlocked[2] else level3unlocked, "Level 3", 'darkgray' if not level_unlocked[2] else 'white')
    ]




    for i, (level_num, command, text, bg_color) in enumerate(level_buttons):
        levelselect_canvas.create_window(500, 300 + i * 90, anchor="n", window=create_button(text, command, bg=bg_color))




    levelselect_canvas.create_window(500, 570, anchor="n", window=create_button("Back", back, width=15))




#---------- Back to Main ----------#
def back():
    levelselect_canvas.pack_forget()
    main_canvas.pack(expand=True)




#---------- Menu Screen ----------#
def menu():
    print("In Menu")
    global menu_canvas
    images['menu_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/menu_bg.jpg"))
    menu_canvas = create_canvas(images['menu_bg'])
    menu_canvas.pack(expand=True)




    menu_canvas.create_window(500, 275, anchor="n", window=create_button("Resume Level", resume_level))
    menu_canvas.create_window(500, 365, anchor="n", window=create_button("Main Menu", lambda: gotomainmenu(dialog_system)))
    menu_canvas.create_window(500, 455, anchor="n", window=create_button("Exit", root.quit))




    if current_level:
        if current_level == 1:
            level1_canvas.pack_forget()
        elif current_level == 2:
            level2_canvas.pack_forget()
        elif current_level == 3:
            level3_canvas.pack_forget()




#---------- Resume Level ----------#
def resume_level():
    if current_level:
        if current_level == 1:
            level1_canvas.pack(expand=True)
        elif current_level == 2:
            level2_canvas.pack(expand=True)
        elif current_level == 3:
            level3_canvas.pack(expand=True)
    menu_canvas.pack_forget()




#---------- Try Again ----------#
def try_again():
    if current_level:
        if current_level == 1:
            level1_canvas.pack(expand=True)
        elif current_level == 2:
            level2_canvas.pack(expand=True)
        elif current_level == 3:
            level3_canvas.pack(expand=True)
    lvlcomplete_canvas.pack_forget()




#---------- Load Level ----------#
def load_level(level_num, bg_image):
    global current_level
    current_level = level_num




    level_canvas = create_canvas(bg_image)
    level_canvas.pack(expand=True)






    level_canvas.create_window(850, 25, anchor="n", window=create_button("Menu", menu, width=15, height=1, font=('Silver', 15)))



    return level_canvas




#---------- Level Functions ----------#
def level1():
    global level1_canvas, dialog_system
    images['level1_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/level1_bg.jpg"))
    level1_canvas = load_level(1, images['level1_bg'])
    levelselect_canvas.pack_forget()
    dialog_system = DialogSystem(root, level=1, on_complete=on_level_complete)




def unlock_level(level_index):
    global level_unlocked
    level_unlocked[level_index] = True




def level2locked():
    if level_unlocked[1]:
        level2unlocked()
    else:
        messagebox.showwarning("Level 2 Locked", "Finish Level 1 to unlock Level 2!")




def level2unlocked():
    global level2_canvas
    images['level2_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/level2_bg.jpg"))
    level2_canvas = load_level(2, images['level2_bg'])
    levelselect_canvas.pack_forget()
    dialog_system = DialogSystem(root, level=2, on_complete=on_level_complete)




def level3locked():
    if level_unlocked[2]:
        level3unlocked()
    else:
        messagebox.showwarning("Level 3 Locked", "Finish Level 2 to unlock Level 3!")




def level3unlocked():
    global level3_canvas
    images['level3_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/level3_bg.jpg"))
    level3_canvas = load_level(3, images['level3_bg'])
    dialog_system = DialogSystem(root, level=3, on_complete=on_level_complete)




#---------- Show Username Popup ----------#
def show_username_popup(score, current_level):
    # Validate the score before proceeding
    if not isinstance(score, int) or score < 0:
        messagebox.showerror("Invalid Score", "The score is invalid. Please try again.")
        return

    popup = tk.Toplevel(root)
    popup.title("Enter Username")
    popup.configure(bg='black')
    popup.iconbitmap('assets/images/FightOn.ico')
    popup.geometry("400x200+{}+{}".format((popup.winfo_screenwidth() // 2) - 200, (popup.winfo_screenheight() // 2) - 100))

    tk.Label(popup, text=f"Score: {score}", font=('Silver', 20), bg='black', fg='white').pack(pady=10)
    tk.Label(popup, text="Enter your username:", font=('Silver', 15), bg='black', fg='white').pack(pady=10)

    username_entry = tk.Entry(popup, font=('Silver', 15))
    username_entry.pack(pady=10)

    def submit_username():
        username = username_entry.get().strip()  # Strip leading/trailing spaces
        
        # Check if username is empty
        if not username:
            messagebox.showwarning("Invalid Username", "Username cannot be empty. Please enter a valid username.")
            return
        
        # Save score to the database
        try:
            with sqlite3.connect('leaderboard.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO scores (level, username, score) VALUES (?, ?, ?)", (current_level, username, score))
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while saving the score: {e}")
            return

        popup.destroy()  # Close the popup after submitting
        
    submit_button = tk.Button(popup, text="Submit", command=submit_username, font=('Silver', 15, 'bold'))
    submit_button.pack(pady=10)



#--------- LEVEL COMPLETE SCREEN ---------
def display_level_complete_screen(score, dialog_system=None):  # Make dialog_system optional
    """Shows the level complete screen"""
    global lvlcomplete_canvas, current_level

    # Hide the current level canvas instead of specifically level1_canvas
    if current_level == 1 and 'level1_canvas' in globals():
        level1_canvas.pack_forget()
    elif current_level == 2 and 'level2_canvas' in globals():
        level2_canvas.pack_forget()
    elif current_level == 3 and 'level3_canvas' in globals():
        level3_canvas.pack_forget()
        
    images['lvlcomplete_bg'] = ImageTk.PhotoImage(Image.open("assets/images/bg/lvlcomplete_bg.jpg"))
    lvlcomplete_canvas = create_canvas(images['lvlcomplete_bg'])
    lvlcomplete_canvas.pack(expand=True)
    
    # Pass the dialog_system to gotomainmenu
    lvlcomplete_canvas.create_window(500, 465, anchor="n", 
                                     window=create_button("Main Menu", lambda: gotomainmenu(dialog_system)))

    # Check if the next level should be unlocked and show message
    if current_level == 1:
        unlock_level(1)
        messagebox.showinfo("Level Unlocked", "You have now unlocked Level 2.")
    elif current_level == 2:
        unlock_level(2)
        messagebox.showinfo("Level Unlocked", "You have now unlocked Level 3.")

    # Update the level select buttons to reflect the new unlocked status
    update_lvlselectbtns()
    show_username_popup(score, current_level)

#---------- Finish Level ----------#
def finishlevel(score):
    pass





#---------- Go to Main Menu from Ingame ----------#
def gotomainmenu(dialog_system):
    print("Going to Main Menu")
    
    cleanup_dialog_system(dialog_system)
    
    # Check if menu_canvas exists before trying to hide it
    if 'menu_canvas' in globals():
        menu_canvas.pack_forget()
    
    # Check if lvlcomplete_canvas exists and hide it if needed
    if 'lvlcomplete_canvas' in globals():
        lvlcomplete_canvas.pack_forget()
    
    # Go back to the main menu
    main_canvas.pack(expand=True)


#---------- Quit to Main ----------#
def quit2lvlselect():
    print("Going to level select)")
    main_canvas.pack_forget()
    main_canvas.pack(expand=True)



def on_level_complete(dialog_system):
    """Callback function to be called when a level is completed"""
    global current_level
    score = dialog_system.get_score()  # Get the score directly from dialog_system
    
    print("Level completed with score:", score)
    
    # Clean up the active level canvas to hide the current level's background
    if current_level == 1 and 'level1_canvas' in globals():
        level1_canvas.pack_forget()
    elif current_level == 2 and 'level2_canvas' in globals():
        level2_canvas.pack_forget()
    elif current_level == 3 and 'level3_canvas' in globals():
        level3_canvas.pack_forget()

    # Update level-specific scores
    if current_level == 1:
        global level1_score
        level1_score = score
    elif current_level == 2:
        global level2_score
        level2_score = score
    elif current_level == 3:
        global level3_score
        level3_score = score

    # Clean up dialog system resources
    cleanup_dialog_system(dialog_system)

    # Show the level complete screen
    display_level_complete_screen(score, dialog_system)

leaderboarddb_setup()
main()
root.mainloop()