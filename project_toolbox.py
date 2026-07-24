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

# Function to create XSLT template 
def create_xslt_template(project_path):

    namespace = entry_namespace.get().strip()

    # Validate namespace
    if namespace and not namespace.startswith("urn:com.workday.report/"):
        messagebox.showerror(
            "Namespace Error",
            "Report Namespace must start with:\n\n"
            "urn:com.workday.report/"
        )
        return

    intnumber = entry_int.get().strip()
    csv_function = ""

    if namespace:
        wd_namespace = namespace
        namespace_comment = ""
    else:
        wd_namespace = "REPORT_NAMESPACE"
        namespace_comment = """
    <!-- TODO: Replace REPORT_NAMESPACE with the report namespace -->
        """
    
    if csv_quotes_var.get():
        csv_function = """
    <!-- CSV-safe quoting function -->
    <xsl:function name="local:wrap_quotes" as="xs:string">
        <xsl:param name="v" as="xs:string?"/>
        <xsl:sequence
            select="concat('&quot;',
            replace(normalize-space($v), '&quot;', '&quot;&quot;'),
            '&quot;')" />
    </xsl:function>
    """
    
    xslt_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wd="{wd_namespace}"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:local="urn:local"
    version="2.0">
    {namespace_comment}
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:strip-space elements="*"/>

    <!-- Newline -->
    <xsl:variable name="line_break" select="'&#x0A;'"/>
    {csv_function}
    <xsl:template match="/wd:Report_Data">

        <!-- TODO: Enter CSV Header Values -->
        <xsl:text></xsl:text>
        <xsl:value-of select="$line_break"/>

        <!-- Report Data -->
        <xsl:for-each select="wd:Report_Entry">

            <!-- TODO: Call CSV-safe quoting function for each value:
                <xsl:value-of select="local:wrap_quotes(wd:XML_Alias)"/>
            -->
            <xsl:text>,</xsl:text>
            <xsl:value-of select="$line_break"/>

        </xsl:for-each>

    </xsl:template>

</xsl:stylesheet>
    """

    xslt_file = os.path.join(
        project_path,
        "XSLT",
        f"INT{intnumber}_XSLT.xsl"
    )

    with open(xslt_file, "w", encoding="utf-8") as f:
        f.write(xslt_content)

# Function to create folder structure 
def create_folders():
    int_number = entry_int.get().strip()
    description = entry_desc.get().strip()

    if not int_number or not description: 
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    # Validate namespace if XSLT template is requested
    if create_xslt_var.get():

        namespace = entry_namespace.get().strip()

        if namespace and not namespace.startswith("urn:com.workday.report/"):
            messagebox.showerror(
                "Namespace Error",
                "Report Namespace must start with:\n\n"
                "urn:com.workday.report/"
            )
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

    if create_xslt_var.get():
        create_xslt_template(full_path)        

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

def show_create_API():   
    home_frame.pack_forget()
    view_projects_frame.pack_forget()
    create_project_frame.pack(fill="both", expand=True)

def show_create_pyapp():
    home_frame.pack_forget()
    view_projects_frame.pack_forget()
    create_project_frame.pack_forget()
    create_pyapp_frame.pack(fill="both", expand=True)
# Function used by View INT Projects btn. 
def open_integrations_folder():
    desktop_path = get_desktop_path()
    base_path = desktop_path / "Workday" / "Integrations"

    os.makedirs(base_path, exist_ok=True)

    os.startfile(base_path)

# Main GUI
root = tk.Tk()
root.title("NS Dev Toolbox")
root.geometry("420x420")
root.resizable(False,False)
# Custom Colors 
bg_color = "#ffffff"
btn_color = "#32CD32"
btn_width = 25

root.configure(bg=bg_color)

home_frame = tk.Frame(root,bg=bg_color)
subtitle_frame = tk.Frame(home_frame, bg=bg_color)
create_project_frame = tk.Frame(root, bg=bg_color)
create_pyapp_frame = tk.Frame(root, bg=bg_color)
view_projects_frame = tk.Frame(root, bg=bg_color)
button_frame = tk.Frame(create_project_frame, bg=bg_color)

# Home Screen
home_title = tk.Label(
    home_frame, 
    text="NS Dev Toolbox", 
    font=("Arial", 22, "bold"),
    bg=bg_color,
    fg="black"
)
home_title.pack(pady=(20, 10))
subtitle_frame.pack(fill="x", padx=20, pady=10)

# Subtitle
home_subtitle = tk.Label(
    subtitle_frame,
    text="Centralized toolbox for creating and managing development projects.",
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
    text="Create new API Project",
    command =show_create_API,
    bg=btn_color,
    width=btn_width
)
btn_new_project.pack(pady=10)

# Basic Python App - TKinter GUI
btn_new_pyapp = tk.Button(
    home_frame,
    text="Create Basic Python App",
    command =show_create_pyapp,
    bg=btn_color,
    width=btn_width
)

# Home - View INT Projects button
btn_view_projects = tk.Button(
    home_frame,
    text="View Projects",
    command=open_integrations_folder,
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

# New Project Frame - Create Project button 
btn_create = tk.Button(
    button_frame, 
    text="Create Project", 
    command=create_folders, 
    bg=btn_color, 
    fg="black", 
    width=btn_width
    )

# Add buttons
btn_create.pack(pady=15)
btn_home.pack(pady=5)

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
    bg=bg_color
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