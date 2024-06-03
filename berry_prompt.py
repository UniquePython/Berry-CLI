import customtkinter as ctk
import tkinter as tk
import os
import ttkthemes
from commands import (
    print_message, list_directory, change_directory, create_folder, create_file,
    delete_files, delete_folders, copy_files, move_files, rename_file,
    list_processes, kill_process, show_help
)

class BerryPrompt(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Berry Prompt")
        self.geometry("1500x700")
        self.configure(bg="white")
        self.option_add('*Font', 'Arial')

        self.style = ttkthemes.ThemedStyle()
        self.style.set_theme("equilux")  

        icon_path = r"c:\Users\chirbhat.ORADEV\Desktop\Python\custom_terminal\Berry-CLI\favicon.ico"
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            print("Warning: favicon.ico not found. Skipping icon setting.")

        self.command_history = []
        self.command_index = -1

        self.create_widgets()

    def create_widgets(self):
        # Create menu bar
        menu_bar = tk.Menu(self)
        self.configure(menu=menu_bar)

        # Add File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        font_menu = tk.Menu(edit_menu, tearoff=0)
        edit_menu.add_cascade(label="Font", menu=font_menu)
        fonts = ["Arial", "Courier New", "Helvetica", "Times New Roman"]
        for font in fonts:
            font_menu.add_command(label=font, command=lambda f=font: self.change_font(f))

        self.output = ctk.CTkTextbox(self, bg_color="black", text_color="white", wrap=tk.WORD, font=('Arial', 15), state="disabled")
        self.output.pack(pady=(10, 5), padx=10, expand=True, fill=tk.BOTH)

        self.entry = ctk.CTkEntry(self, font=('Arial', 15), text_color="black", bg_color="white")
        self.entry = ctk.CTkEntry(self, font=('Arial', 15), text_color="black")
        self.entry.pack(pady=(5, 10), padx=10, expand=False, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.focus_set()

        self.status = ctk.CTkLabel(self, text=f"Current Directory: {os.getcwd()}", anchor="w", bg_color="black", text_color="white")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.output.tag_config("input", foreground="blue")
        self.output.tag_config("output_text", foreground="green")
        self.output.tag_config("error", foreground="red")

        self.entry.bind("<Up>", self.navigate_command_history)
        self.entry.bind("<Down>", self.navigate_command_history)

    def change_font(self, font_name):
        self.output.configure(font=(font_name, 15))
        self.entry.configure(font=(font_name, 15))

    def execute_command(self, event):
        command = self.entry.get().strip()
        if not command:
            return "break"
        current_dir = os.getcwd()

        self.output.configure(state="normal")
        self.output.insert(tk.END, f"({current_dir}) Input: {command}\n", "input")

        try:
            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            command_functions = {
                "print": print_message,
                "list": list_directory,
                "cd": change_directory,
                "new --folder": create_folder,
                "new --file": create_file,
                "delete --file": delete_files,
                "delete --folder": delete_folders,
                "copy": copy_files,
                "move": move_files,
                "rename": rename_file,
                "tasklist": list_processes,
                "taskkill": kill_process,
                "help": show_help,
                "clear": self.clear_output,
                "exit": self.quit,
            }

            if cmd in command_functions:
                command_functions[cmd](self, args)
            else:
                self.output.insert(tk.END, "Output: Command not recognized\n", "error")

            self.command_history.append(command)
            self.command_index = len(self.command_history)

        except Exception as e:
            self.output.insert(tk.END, f"({current_dir}) Output: Error: {str(e)}\n", "error")

        self.output.configure(state="disabled")
        self.output.see("end")
        self.entry.delete(0, tk.END)
        return "break"

    def navigate_command_history(self, event):
        if event.keysym == "Up":
            if self.command_index > 0:
                self.command_index -= 1
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.command_history[self.command_index])
        elif event.keysym == "Down":
            if self.command_index < len(self.command_history) - 1:
                self.command_index += 1
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.command_history[self.command_index])

    def clear_output(self, args=None):
        self.output.configure(state="normal")
        self.output.delete(1.0, tk.END)
        self.output.configure(state="disabled")
