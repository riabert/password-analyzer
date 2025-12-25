import tkinter as tk
from tkinter import ttk
import re
import os

def check_password():
    password = entry.get()
    score = 0

    if len(password) >= 8:
        score += 25
    if re.search(r"\d", password):
        score += 25
    if re.search(r"[A-Z]", password):
        score += 25
    if re.search(r"[!@#$%^&*()_+=\-{}[\]:;\"'<>,.?/]", password):
        score += 25

    progress['value'] = score

    if score == 0:
        result.config(text="", fg=color["fg"])
    elif score < 50:
        result.config(text="Weak Password", fg="red")
    elif score < 100:
        result.config(text="Medium Password", fg="orange")
    else:
        result.config(text="Strong Password", fg="green")

def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def clear_fields():
    entry.delete(0, tk.END)
    result.config(text="")
    progress['value'] = 0

def apply_theme(theme):
    global color
    if theme == "dark":
        color = {
            "bg": "#1e1e1e",
            "fg": "white",
            "entry_bg": "#2d2d2d",
            "bar": "#00ff88",
            "active_bg": "#3c3c3c" # New color for active backgrounds
        }
        root.configure(bg=color["bg"])
        style.configure("TProgressbar", background=color["bar"], troughcolor="#333", bordercolor=color["bg"])
    else:
        color = {
            "bg": "SystemButtonFace",
            "fg": "black",
            "entry_bg": "white",
            "bar": "green",
            "active_bg": "SystemButtonFace" # Default for light theme
        }
        root.configure(bg=color["bg"])
        style.configure("TProgressbar", background=color["bar"])

    # Apply to all tk widgets
    label.config(bg=color["bg"], fg=color["fg"])
    entry.config(bg=color["entry_bg"], fg=color["fg"], insertbackground=color["fg"])
    show_check.config(bg=color["bg"], fg=color["fg"], activebackground=color["bg"], selectcolor=color["entry_bg"]) # selectcolor for checked state
    checklist.config(bg=color["bg"], fg="gray")
    result.config(bg=color["bg"])
    clear_btn.config(bg=color["bg"], fg=color["fg"], activebackground=color["active_bg"], activeforeground=color["fg"])

    # --- CRITICAL FIX FOR ttk.OptionMenu STYLING ---
    style.configure("TMenubutton",
                    background=color["entry_bg"],
                    foreground=color["fg"],
                    font=("Arial", 12) # Optional: Consistent font for the OptionMenu
                   )
    style.map("TMenubutton",
              background=[('active', color["active_bg"])],
              foreground=[('active', color["fg"])]
             )
    # --- END FIX ---

def switch_theme(*args):
    selected_theme = theme_var.get()
    apply_theme(selected_theme)

# --- GUI Setup ---
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("420x430")

# --- Robust Icon Handling ---
try:
    script_dir = os.path.dirname(__file__)
    icon_path = os.path.join(script_dir, "password_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print(f"Warning: Icon file not found at {icon_path}. Application will run without a custom icon.")
except tk.TclError as e:
    print(f"Error setting icon: {e}. Ensure 'password_icon.ico' is a valid .ico file.")
except Exception as e:
    print(f"An unexpected error occurred while setting the icon: {e}")
# --- End Robust Icon Handling ---

color = {}
style = ttk.Style()
style.theme_use("clam")

# Theme selector
theme_var = tk.StringVar(value="light")
theme_menu = ttk.OptionMenu(root, theme_var, "light", "light", "dark", command=switch_theme)
theme_menu.pack(pady=5)

# Main label
label = tk.Label(root, text="Enter your password:", font=("Arial", 12))
label.pack(pady=10)

# Entry field
entry = tk.Entry(root, width=30, show="*", font=("Arial", 12))
entry.pack(pady=5)
entry.bind("<KeyRelease>", lambda event: check_password())

# Show password checkbox
show_var = tk.BooleanVar()
show_check = tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password)
show_check.pack()

# Checklist
checklist = tk.Label(root, text="- At least 8 characters\n- 1 number\n- 1 uppercase letter\n- 1 special symbol", font=("Arial", 10), justify="left")
checklist.pack(pady=5)

# Clear button
clear_btn = tk.Button(root, text="Clear", command=clear_fields, font=("Arial", 11))
clear_btn.pack(pady=5)

# Progress bar
progress = ttk.Progressbar(root, length=250, maximum=100)
progress.pack(pady=10)

# Result label
result = tk.Label(root, text="", font=("Arial", 14))
result.pack(pady=20)

# Apply default (light) theme
apply_theme("light")

root.mainloop()

