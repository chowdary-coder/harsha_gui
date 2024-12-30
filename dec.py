import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def perform_operation(file_path, client):
    # Sample backend functionality based on the selected client
    if client == "Client A":
        messagebox.showinfo("Client A", f"Performing operation for Client A with file {file_path}")
    elif client == "Client B":
        messagebox.showinfo("Client B", f"Performing operation for Client B with file {file_path}")
    elif client == "Client C":
        messagebox.showinfo("Client C", f"Performing operation for Client C with file {file_path}")
    else:
        messagebox.showwarning("Unknown Client", "Unknown client selected!")

def go_to_upload_page():
    # Hide the client selection page
    client_frame.pack_forget()
    # Show the file upload page
    upload_frame.pack(fill='both', expand=True)
    update_window_size()
    # Update the client name in the header on the upload page
    update_client_header(selected_client.get())

def go_home():
    # Go back to the client selection page
    upload_frame.pack_forget()
    client_frame.pack(fill='both', expand=True)
    update_window_size()

def show_help():
    # Show a help message box
    messagebox.showinfo("Help", "This is a simple application for selecting a client and uploading a file.\n\nSteps:\n1. Select a client.\n2. Upload a file.\n3. Perform operation.\n\nEnjoy!")

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)

def submit_file():
    file_path = file_path_var.get()
    client = selected_client.get()
    if file_path:
        perform_operation(file_path, client)
    else:
        messagebox.showwarning("Warning", "Please select a file to upload.")

def update_client_header(client_name):
    # Update the header label with the selected client name
    client_header_label.config(text=f"Client: {client_name}")

def apply_theme(theme):
    if theme == "Light":
        primary_color = "#FFFFFF"
        secondary_color = "#F0F0F0"
        accent_color = "#0078D7"
        text_color = "#000000"
        button_active_bg = "#005BB5"
        button_active_fg = "#FFFFFF"
    else:  # Dark theme
        primary_color = "#2A2A2A"
        secondary_color = "#1E1E1E"
        accent_color = "#FF6F61"
        text_color = "#FFFFFF"
        button_active_bg = "#FF4B47"
        button_active_fg = "#FFFFFF"
    
    style.configure('TFrame', background=primary_color)
    style.configure('TLabel', background=primary_color, foreground=text_color, font=(font_family, font_size))
    style.configure('TButton', background=accent_color, foreground=text_color, font=(font_family, font_size))
    style.map('TButton', background=[('active', button_active_bg)], foreground=[('active', button_active_fg)])
    style.configure('TCombobox', font=(font_family, font_size))
    style.map('TCombobox', fieldbackground=[('readonly', secondary_color)], selectbackground=[('readonly', secondary_color)], selectforeground=[('readonly', text_color)])

    # Configure specific button styles
    style.configure('Browse.TButton', background='#FFA500', foreground='#000000')
    style.map('Browse.TButton', background=[('active', '#FF8C00')], foreground=[('active', '#FFFFFF')])
    
    style.configure('Submit.TButton', background='#32CD32', foreground='#FFFFFF')
    style.map('Submit.TButton', background=[('active', '#228B22')], foreground=[('active', '#FFFFFF')])

    root.update_idletasks()

def change_theme(event):
    selected_theme = theme_var.get()
    apply_theme(selected_theme)

def update_window_size():
    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    root.geometry(f"{width}x{height}")

# Create the main application window
root = tk.Tk()
root.title("Client Selection and File Upload")
root.resizable(False, False)  # Disable window resizing

# Define fonts
font_family = "Helvetica"
font_size = 10  # Decreased font size

# Configure styles
style = ttk.Style()
style.theme_use('clam')

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add 'Home' and 'Help' options to the menu
home_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Home", menu=home_menu)
home_menu.add_command(label="Go to Home", command=go_home)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=show_help)

# Theme selection frame
theme_frame = ttk.Frame(root, padding="10 10 10 10")
theme_frame.pack(fill='x', padx=10, pady=10)

ttk.Label(theme_frame, text="Select Theme:").pack(side=tk.LEFT, padx=5)
theme_var = tk.StringVar(value="Light")
theme_dropdown = ttk.Combobox(theme_frame, textvariable=theme_var, values=["Light", "Dark"], state="readonly")
theme_dropdown.pack(side=tk.LEFT, padx=5)
theme_dropdown.bind("<<ComboboxSelected>>", change_theme)

# Client selection page
client_frame = ttk.Frame(root, padding="20 20 20 20")
client_frame.pack(fill='both', expand=True)

client_label = ttk.Label(client_frame, text="Select a Client:")
client_label.pack(anchor=tk.W, pady=5)

# Dropdown menu for client selection
clients = ["Client A", "Client B", "Client C"]
selected_client = tk.StringVar()
client_dropdown = ttk.Combobox(client_frame, textvariable=selected_client, values=clients, state="readonly")
client_dropdown.pack(fill=tk.X, pady=5)
client_dropdown.current(0)

# Submit button to go to the file upload page
next_button = ttk.Button(client_frame, text="Next", command=go_to_upload_page)
next_button.pack(pady=20)

# File upload page
upload_frame = ttk.Frame(root, padding="20 20 20 20")

# Header label for client name in the upload page (centered)
client_header_label = ttk.Label(upload_frame, text="", font=(font_family, 12, 'bold'), anchor='center')
client_header_label.grid(row=0, column=0, columnspan=2, pady=10)

upload_label = ttk.Label(upload_frame, text="Upload a File:")
upload_label.grid(row=1, column=0, sticky=tk.W, pady=5)

file_path_var = tk.StringVar()

# Set the width of the file path entry (e.g., width = 40)
file_path_entry = ttk.Entry(upload_frame, textvariable=file_path_var, state="readonly", font=(font_family, font_size), width=40)
file_path_entry.grid(row=2, column=0, sticky=tk.W+tk.E, pady=5)

browse_button = ttk.Button(upload_frame, text="Browse", command=upload_file, style='Browse.TButton')
browse_button.grid(row=2, column=1, padx=5, pady=5)

# Submit button to perform the operation
submit_button = ttk.Button(upload_frame, text="Submit", command=submit_file, style='Submit.TButton')
submit_button.grid(row=3, column=0, columnspan=2, pady=20)

# Hide the upload frame initially
upload_frame.pack_forget()

# Apply initial theme
apply_theme("Light")

# Adjust window size to fit the content initially
update_window_size()

# Start the Tkinter event loop
root.mainloop()
