import tkinter as tk
from tkinter import BooleanVar, filedialog
from threading import Thread
import time  # For simulating backend processing

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Dynamic Frame Interaction with Multithreading")
        self.geometry("700x400")
        self.minsize(700, 400)
        self.maxsize(700, 400)
        self.config(bg="#F5F5F5")  # Light mode by default

        # Dark mode variable
        self.dark_mode = BooleanVar(value=False)

        # Create and configure frames
        self.create_menu()
        self.create_frames()

        # Initialize the home screen
        self.show_home()

    def create_menu(self):
        # Add menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Add Home option to menu bar
        self.menu_bar.add_command(label="Home", command=self.show_home)

        # Add Help option to menu bar
        self.menu_bar.add_command(label="Help", command=self.show_help)

    def create_frames(self):
        # Frame 1
        self.frame1 = tk.Frame(self, bg="#D6E4F0", relief="groove", borderwidth=2, width=150)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        # Frame 2
        self.frame2 = tk.Frame(self, bg="#FFFFFF", relief="groove", borderwidth=2)
        self.frame2.grid(row=0, column=1, sticky="nsew")

        # Configure layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Add buttons to Frame 1
        for i in range(1, 5):
            tk.Button(
                self.frame1,
                text=f"Button {i} (Frame 1)",
                bg="#B3D4EA",
                fg="#000000",
                activebackground="#A9C4D5",
                activeforeground="#000000",
                command=lambda i=i: self.update_frame2(i)
            ).pack(pady=5)

        # Add Dark Mode Toggle to Frame 1
        dark_mode_check = tk.Checkbutton(
            self.frame1,
            text="Dark Mode",
            variable=self.dark_mode,
            command=self.toggle_dark_mode,
            bg="#B3D4EA",
            fg="#000000",
            activebackground="#A9C4D5",
            activeforeground="#000000",
            selectcolor="#FFFFFF"
        )
        dark_mode_check.pack(side="bottom", pady=10)

    def toggle_dark_mode(self):
        # Define colors for dark and light modes
        bg_color = "#121212" if self.dark_mode.get() else "#F5F5F5"
        frame1_color = "#1E1E1E" if self.dark_mode.get() else "#D6E4F0"
        frame2_color = "#1E1E1E" if self.dark_mode.get() else "#FFFFFF"
        widget_fg = "#E0E0E0" if self.dark_mode.get() else "#000000"
        active_bg = "#616161" if self.dark_mode.get() else "#A9C4D5"
        button_bg = "#607D8B" if self.dark_mode.get() else "#B3D4EA"
        button_active_bg = "#4CAF50" if self.dark_mode.get() else "#A9C4D5"
        
        # Apply the selected theme (dark or light)
        self.config(bg=bg_color)
        self.frame1.config(bg=frame1_color)
        self.frame2.config(bg=frame2_color)

        # Update widgets in frame1
        for widget in self.frame1.winfo_children():
            widget.config(bg=frame1_color, fg=widget_fg, activebackground=active_bg)

        # Update widgets in frame2
        for widget in self.frame2.winfo_children():
            widget.config(bg=frame2_color, fg=widget_fg, activebackground=active_bg)

        # Update buttons' color in both frames
        for button in self.frame1.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg=button_bg, activebackground=button_active_bg)

        for button in self.frame2.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg=button_bg, activebackground=button_active_bg)

    def show_home(self):
        self.clear_frame2()
        fg_color = "#E0E0E0" if self.dark_mode.get() else "#000000"
        bg_color = self.frame2.cget("bg")

        tk.Label(self.frame2, text="Welcome to the Home Screen!", bg=bg_color, fg=fg_color, font=("Arial", 14)).pack(pady=10)

    def show_help(self):
        self.clear_frame2()
        fg_color = "#E0E0E0" if self.dark_mode.get() else "#000000"
        bg_color = self.frame2.cget("bg")

        help_text = """
        Help Section:
        - Button 1: Upload files and submit them.
        - Button 2: Change settings such as password and profile.
        - Button 3: View reports or export data.
        - Button 4: Access help or contact support.

        For further assistance, email support@example.com.
        """
        tk.Label(self.frame2, text=help_text, bg=bg_color, fg=fg_color, justify="left", wraplength=400).pack(pady=10)

    def update_frame2(self, button_id):
        self.clear_frame2()
        fg_color = "#E0E0E0" if self.dark_mode.get() else "#000000"
        bg_color = self.frame2.cget("bg")

        if button_id == 1:
            tk.Label(self.frame2, text="Upload Menu (Button 1)", bg=bg_color, fg=fg_color).pack(pady=10)

            file_label = tk.Label(self.frame2, text="No file selected", bg=bg_color, fg=fg_color)
            file_label.pack(pady=5)

            def browse_file():
                file_path = filedialog.askopenfilename()
                if file_path:
                    file_label.config(text=f"File: {file_path}")

            def submit_file():
                self.clear_frame2_messages()
                if "File:" in file_label.cget("text"):
                    tk.Label(self.frame2, text="File submitted successfully!", bg=bg_color, fg=fg_color).pack(pady=5)
                else:
                    tk.Label(self.frame2, text="Please select a file before submitting.", bg=bg_color, fg="#FF0000").pack(pady=5)

            tk.Button(self.frame2, text="Browse", bg="#607D8B", fg="#FFFFFF", command=browse_file).pack(pady=5)
            tk.Button(self.frame2, text="Submit", bg="#4CAF50", fg="#FFFFFF", command=lambda: Thread(target=submit_file).start()).pack(pady=5)

        elif button_id == 2:
            tk.Label(self.frame2, text="Settings Menu (Button 2)", bg=bg_color, fg=fg_color).pack(pady=10)
            tk.Button(self.frame2, text="Change Password", bg="#FF9800", fg="#FFFFFF").pack(pady=5)
            tk.Button(self.frame2, text="Update Profile", bg="#3F51B5", fg="#FFFFFF").pack(pady=5)

        elif button_id == 3:
            tk.Label(self.frame2, text="Reports Menu (Button 3)", bg=bg_color, fg=fg_color).pack(pady=10)
            tk.Button(self.frame2, text="View Reports", bg="#2196F3", fg="#FFFFFF").pack(pady=5)
            tk.Button(self.frame2, text="Export Data", bg="#673AB7", fg="#FFFFFF").pack(pady=5)

        elif button_id == 4:
            tk.Label(self.frame2, text="Help Menu (Button 4)", bg=bg_color, fg=fg_color).pack(pady=10)
            tk.Label(self.frame2, text="For assistance, contact support@example.com", bg=bg_color, fg=fg_color).pack(pady=10)

    def clear_frame2(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

    def clear_frame2_messages(self):
        for widget in self.frame2.winfo_children(): 
            if isinstance(widget, tk.Label) and "Success" in widget.cget("text"):
                widget.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
