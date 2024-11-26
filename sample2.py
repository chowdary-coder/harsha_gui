import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class MultiClientApp(tk.Tk):
    def __init__(self, clients):
        super().__init__()
        self.title("MRF MF Application")
        self.geometry("470x480")
        self.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook.Tab", background="#93b874", font=("Helvetica", 8, "bold"), foreground="#ffffff")
        style.map("TNotebook.Tab", background=[("selected", "lightgreen")], foreground=[("selected", "blue")])

        # Create a notebook to hold multiple client tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Add a tab for each client
        for client in clients:
            client_frame = ClientFrame(self.notebook, client, self)
            self.notebook.add(client_frame, text=client)

class ClientFrame(ttk.Frame):
    def __init__(self, parent, client_name, app):
        super().__init__(parent)
        self.file_paths = {}
        
        self.client_name = client_name
        self.app = app
        self.pack(expand=True, fill='both')

        # Create menu
        self.create_menu()

        # Create a container to hold the pages
        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill='both')

        # Initialize pages
        self.pages = {}
        self.current_page = None
        

        # Create the client-specific page
        self.add_page(client_name)

    def create_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.pack(side="top", fill="x")

        # Checkbox to use file paths from config.json
        self.use_config_var = tk.BooleanVar()
        use_config_check = ttk.Checkbutton(menu_frame, text="Use Previous Config File Paths",
                                           variable=self.use_config_var, command=self.toggle_file_entry)
        use_config_check.pack(side="left")

    def load_config(self):
        """Load file paths from the config.json if available."""
        if os.path.exists(""):
            with open("Documents/config.json", "r") as f:
                data = json.load(f)
                self.file_paths = data.get("file_paths", {})

    def toggle_file_entry(self):
        """Toggle between manual file selection and using config.json file paths."""
        if self.use_config_var.get():
            # If checkbox is selected, use file paths from the config.json file
            self.load_file_paths_from_config()
        else:
            # Clear entries if checkbox is unselected
            self.clear_entries()

    def clear_entries(self):
        """Clear all file entry fields."""
        for entry in self.upload_entries:
            entry.config(state='normal')
            entry.delete(0, tk.END)

    def load_file_paths_from_config(self):
        """Load file paths from the config and insert them into the entry fields."""
        with open("Documents/config.json", "r") as config_file:
                self.file_paths = json.load(config_file)
                for i, entry in enumerate(self.upload_entries):
                    if i < len(self.file_paths):
                        entry.delete(0, tk.END)
                        entry.insert(0, self.file_paths[str(i)])
                        entry.config(state='readonly')

    

    def add_page(self, client_name):
        page_frame = ttk.Frame(self.container)
        
        # Client-specific labels and upload fields
        label = ttk.Label(page_frame, text=f" {client_name} Calculations", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)

        # Determine how many upload options based on client
        num_uploads = 6 if client_name == " Perpetual " else 6
        self.upload_entries = []
        
        for i in range(num_uploads):
            file_frame = ttk.Frame(page_frame)
            file_frame.pack(pady=4, padx=10, anchor='w')

            file_label = ttk.Label(file_frame, text=f"File {i + 1}:", width=15)
            file_label.pack(side='left')

            file_entry = ttk.Entry(file_frame, width=40)
            file_entry.pack(side='left', padx=5)

            browse_button = ttk.Button(file_frame, text="Browse",  command=lambda e=file_entry, idx=i: self.browse_file(e, idx))
            browse_button.pack(side='left')

            self.upload_entries.append(file_entry)
        

        # Add a submit button with different functionality
        submit_button = ttk.Button(page_frame, text="Submit", command=lambda: self.validation(client_name))
        submit_button.pack(pady=10)


        # Logging area #f4f4f4
        self.log_area = tk.Text(page_frame, height=5, width=58, wrap=tk.WORD,bg='#1a0000', fg='#00ff00', font=("Courier", 10))
        # self.log_area.config(state=tk.DISABLED)
        self.log_area.pack(pady=10)

        # Scrollbar for the log area
        log_scrollbar = ttk.Scrollbar(page_frame, command=self.log_area.yview)
        log_scrollbar.pack(side='right', fill='y')
        self.log_area['yscrollcommand'] = log_scrollbar.set

        self.pages[client_name] = page_frame
        
        if self.current_page is None:
            self.show_page(client_name)


    def browse_file(self, entry, index):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            self.file_paths[index] = file_path
            entry.config(state='readonly')
    

    def save_dict_to_json(self, data, file="Documents/config.json"):
        with open(file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            
    def validate_entries(self):
        for entry in self.upload_entries:
            if not entry.get().strip():  # Check if the entry is empty
                messagebox.showerror("Input Error", "All fields are mandatory!")
                entry.focus()
                return
    
    def validation(self, client_name):
        self.validate_entries()
        self.submit(client_name)


    def submit(self, client_name):
        # Logging the submission
        self.clear_logs()  # Clear old logs before new submission
        log_msg = f"Submitting files for {client_name}...\n"
        self.log(log_msg)
        self.save_dict_to_json(self.file_paths)
        for entry in self.upload_entries:
            entry.config(state='normal')
            entry.delete(0, tk.END)
    
        # Simulate file handling and different functionality per client
        if client_name == " Perpetual ":
            self.handle_perpetual()
        elif client_name == " Client02 ":
            self.handle_client02()
        elif client_name == " Client03 ":
            self.handle_client03()

    def handle_perpetual(self):
        # Perpetual client logic
        self.log(json.dumps(self.file_paths))
        self.log("Perpetual client files submitted successfully.") 

    def handle_client02(self):
        # Client02 logic (e.g., processing only 4 files)
        self.log("Client02 files submitted successfully.")

    def handle_client03(self):
        # Client03 logic (e.g., different file processing behavior)
        self.log("Client03 files submitted successfully.")

    def log(self, message):
        """Append log message to the log area."""
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview(tk.END)  # Auto-scroll to the latest log entry

    def clear_logs(self):
        """Clear the log area."""
        self.log_area.delete(1.0, tk.END)

    def show_page(self, client_name):
        if self.current_page:
            self.pages[self.current_page].pack_forget()

        self.pages[client_name].pack(expand=True, fill='both')
        self.current_page = client_name
if __name__ == "__main__":
    clients = [" Perpetual ", " Client02 ", " Client03 "]
    app = MultiClientApp(clients)
    app.mainloop()
