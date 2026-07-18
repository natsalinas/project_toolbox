import os 
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys 

# Function to get user's Desktop path
def get_desktop_path():
    home = Path.home()

    # Check for One-Drive desktop
    onedrive_paths = list(home.glob("OneDrive*"))

    for od in onedrive_paths:
        desktop = od / "Desktop"
        if desktop.exists():
            return desktop
        
    # fallback to return C:/Users/username/Desktop 
    return home / "Desktop"

# Toggle XSLT options 
def toggle_xslt_options():
    if create_xslt_var.get():
        xslt_frame.pack(pady=10)
    else:
        xslt_frame.pack_forget()

# Function to create folder structure 
def create_folders():
    int_number = entry_int.get().strip()
    description = entry_desc.get().strip()

    if not int_number or not description: 
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    # Determine desktop path for user. 
    desktop_path = get_desktop_path()
    # All integration system files will be in Workday/Integrations directory on the user desktop. 
    base_path = desktop_path / "Workday" / "Integrations"
    # Create base folder if it doesnn't exist
    os.makedirs(base_path, exist_ok=True)

    folder_name = f"INT{int_number} - {description}"
    full_path = os.path.join(base_path, folder_name)

    subfolders = ["XML", "XSLT", "Output_Files"]

    for sub in subfolders:
        os.makedirs(os.path.join(full_path, sub), exist_ok=True)
    
    messagebox.showinfo("Success", f"Created folders for:\n{folder_name}")

    entry_int.delete(0, tk.END)
    entry_desc.delete(0, tk.END)

def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, filename)

# Navigation functions 
def show_home():
    create_project_frame.pack_forget()
    view_projects_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

def show_create_project():   
    home_frame.pack_forget()
    view_projects_frame.pack_forget()
    create_project_frame.pack(fill="both", expand=True)

def show_view_projects():
    home_frame.pack_forget()
    create_project_frame.pack_forget()
    view_projects_frame.pack(fill="both", expand=True)

    refresh_project_list()

def refresh_project_list():
    project_listbox.delete(0, tk.END)

    desktop_path = get_desktop_path()
    base_path = desktop_path / "Workday" / "Integrations"

    if not os.path.exists(base_path):
        return

    for folder in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, folder)

        if os.path.isdir(folder_path):
            project_listbox.insert(
                tk.END,
                f"{folder} | {folder_path}"
            )
def update_function_description():
    if csv_quotes_var.get():

        description = (
            "CSV Safe Quoting\n\n"
            "Wraps values in double quotes and "
            "escapes commas in XML value."
        )

    elif date_format_var.get():

        description = (
            "Date Formatter\n\n"
            "Converts Workday date values into "
            "a standard output format."
        )

    elif null_handling_var.get():

        description = (
            "Null Handling\n\n"
            "Provides default values when "
            "source fields are empty."
        )

    else:

        description = (
            "Select a function to view details."
        )

    lbl_function_description.config(text=description)
    

# Main GUI
root = tk.Tk()
root.title("Project Toolbox")
root.geometry("420x420")
root.resizable(False,False)
# Custom Colors 
bg_color = "#ffffff"
btn_color = "#FFC904"
btn_width = 25

root.configure(bg=bg_color)

home_frame = tk.Frame(root,bg=bg_color)
subtitle_frame = tk.Frame(home_frame, bg=bg_color)
create_project_frame = tk.Frame(root, bg=bg_color)
view_projects_frame = tk.Frame(root, bg=bg_color)
button_frame = tk.Frame(create_project_frame, bg=bg_color)

# Home Screen
home_title = tk.Label(
    home_frame, 
    text="Dev Toolbox", 
    font=("Arial", 22, "bold"),
    bg=bg_color,
    fg="black"
)
home_title.pack(pady=(20, 10))
subtitle_frame.pack(fill="x", padx=20, pady=10)

# Subtitle
home_subtitle = tk.Label(
    subtitle_frame,
    text="Centralized toolbox for creating and managing local Workday Integration projects.",
    font=("Arial", 10),
    bg=bg_color,
    wraplength=350,
    justify="center"

)
home_subtitle.pack()

# UCF Logo
try:
    logo_path = resource_path(os.path.join("img", "ucf_logo_2.png"))
    print("DEBUG - logo path:",logo_path)
    
    img = Image.open(logo_path)
    img = img.resize((120,120))
    logo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(home_frame, image=logo, bg=bg_color)
    logo_label.pack(pady=5)
except Exception as e:
    print(f"Logo load error: {e}")

try:
    icon_path = resource_path(os.path.join("img", "ucf_icon.ico"))
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Icon load error: {e}")

# Buttons 
# Home - New INT Project button
btn_new_project = tk.Button(
    home_frame,
    text="Create new INT Project",
    command =show_create_project,
    bg=btn_color,
    width=btn_width
)
btn_new_project.pack(pady=10)
# Home - View INT Projects button
btn_view_projects = tk.Button(
    home_frame,
    text="View INT Projects",
    command=show_view_projects,
    width=btn_width
)
btn_view_projects.pack(pady=10)
# New Project Frame - Home buttom
btn_home = tk.Button(
    button_frame,
    text="Home",
    command=show_home,
    width=btn_width
)
btn_home.pack(pady=5)

# New Project Frame - Create Project button 
btn_create = tk.Button(
    button_frame, 
    text="Create Project", 
    command=create_folders, 
    bg=btn_color, 
    fg="black", 
    width=btn_width
    )
btn_create.pack(pady=15)

# Integration Number 
label_int = tk.Label(create_project_frame, text="Integration Number:", bg=bg_color)
label_int.pack()
entry_int = tk.Entry(create_project_frame, width=30)
entry_int.pack(pady=5)

# Description 
label_desc = tk.Label(create_project_frame, text="Short Description:", bg=bg_color)
label_desc.pack()
entry_desc = tk.Entry(create_project_frame, width=30)
entry_desc.pack(pady=5)

# Generate XSLT checkbox
create_xslt_var = tk.BooleanVar()

chk_xslt = tk.Checkbutton(
    create_project_frame,
    text="Generate XSLT Template",
    variable=create_xslt_var,
    command=toggle_xslt_options,
    bg=bg_color
)
chk_xslt.pack(pady=10)

# XSLT Options Frame
xslt_frame = tk.LabelFrame(
    create_project_frame,
    text="XSLT Options",
    padx=10,
    pady=10,
    bg=bg_color
)

# XSLT Functions Description Section
lbl_function_title = tk.Label(
    xslt_frame,
    text="Function Description",
    font=("Arial", 10, "bold"),
    bg=bg_color
)

lbl_function_title.pack(anchor="w", pady=(10, 0))

lbl_function_description = tk.Label(
    xslt_frame,
    text="Select a function to view details.",
    bg=bg_color,
    justify="left",
    wraplength=300,
    relief="sunken",
    padx=10,
    pady=10
)

lbl_function_description.pack(fill="x", pady=(5, 0))

# Namespace
label_namespace = tk.Label(
    xslt_frame,
    text="Report Namespace:",
    bg=bg_color
)
label_namespace.pack(anchor="w")

entry_namespace = tk.Entry(
    xslt_frame,
    width=50
)
entry_namespace.pack(fill="x", pady=(0, 10))

# Function Section
label_functions = tk.Label(
    xslt_frame,
    text="Available Functions:",
    font=("Arial", 10, "bold"),
    bg=bg_color
)
label_functions.pack(anchor="w", pady=(5, 5))

csv_quotes_var = tk.BooleanVar()

chk_csv_quotes = tk.Checkbutton(
    xslt_frame,
    text="CSV Safe Quoting",
    variable=csv_quotes_var,
    bg=bg_color,
    font=("Arial", 9, "bold"),
    command=update_function_description
)

chk_csv_quotes.pack(anchor="w")

# Hide frame initially
xslt_frame.pack_forget()

# Pack Home a Create Project Buttons for New Project Frame
button_frame.pack(
    side="bottom",
    fill="x",
    pady=10
)

# Start app
show_home()

# Run app 
root.mainloop()