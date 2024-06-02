import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import os
import shutil
import subprocess
import ttkthemes

# Command dictionary
commands = {
    "print": ("Prints a message to the terminal", "print <message>"),
    "list": ("Lists the contents of the current directory", "list"),
    "cd": ("Changes the current directory", "cd <directory_path>"),
    "new --folder": ("Creates a new folder", "new --folder <folder_name>"),
    "new --file": ("Creates a new file", "new --file <file_name_with_extension>"),
    "delete --file": ("Deletes one or more files", "delete --file <file_name1> [file_name2 ...]"),
    "delete --folder": ("Deletes one or more folders", "delete --folder <folder_name1> [folder_name2 ...]"),
    "copy": ("Copies one or more files from one location to another", "copy <source> <destination>"),
    "move": ("Moves one or more files from one location to another", "move <source> <destination>"),
    "rename": ("Renames a file or directory", "rename <old_name> <new_name>"),
    "tasklist": ("Lists all currently running processes", "tasklist"),
    "taskkill": ("Terminates one or more processes", "taskkill <process_name>"),
    "help": ("Displays information about available commands", "help"),
    "clear": ("Clears the output screen", "clear"),
    "exit": ("Exits the application", "exit")
}

class BerryPrompt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Berry Prompt")
        self.state('zoomed')
        self.configure(bg="white")
        self.option_add('*Font', 'Arial')

        self.style = ttkthemes.ThemedStyle()
        self.style.set_theme("equilux")  

        self.iconbitmap("favicon.ico")

        self.command_history = []
        self.command_index = -1

        self.create_widgets()

    def create_widgets(self):
        # Create menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Add File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        self.output = scrolledtext.ScrolledText(self, bg="black", fg="white", wrap=tk.WORD, font=('Arial', 15), state="disabled")
        self.output.pack(pady=(10, 5), padx=10, expand=True, fill=tk.BOTH)

        self.entry = ttk.Entry(self, font=('Arial', 15), background="black", foreground="white")
        self.entry.pack(pady=(5, 10), padx=10, expand=False, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.focus_set()

        self.status = ttk.Label(self, text=f"Current Directory: {os.getcwd()}", anchor="w", background="white",
                                foreground="black")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.output.tag_config("input", foreground="blue")
        self.output.tag_config("output_text", foreground="green")
        self.output.tag_config("error", foreground="red")

        self.entry.bind("<Up>", self.navigate_command_history)
        self.entry.bind("<Down>", self.navigate_command_history)

    def execute_command(self, event):
        command = self.entry.get().strip()
        if not command:
            return "break"
        current_dir = os.getcwd()

        self.output.config(state="normal")
        self.output.insert(tk.END, f"({current_dir}) Input: {command}\n", "input")

        try:
            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            command_functions = {
                "print": self.print_message,
                "list": self.list_directory,
                "cd": self.change_directory,
                "new --folder": self.create_folder,
                "new --file": self.create_file,
                "delete --file": self.delete_files,
                "delete --folder": self.delete_folders,
                "copy": self.copy_files,
                "move": self.move_files,
                "rename": self.rename_file,
                "tasklist": self.list_processes,
                "taskkill": self.kill_process,
                "help": self.show_help,
                "clear": self.clear_output,
                "exit": self.quit,
            }

            if cmd in command_functions:
                command_functions[cmd](args)
            else:
                self.output.insert(tk.END, "Output: Command not recognized\n", "error")

            self.command_history.append(command)
            self.command_index = len(self.command_history)

        except Exception as e:
            self.output.insert(tk.END, f"({current_dir}) Output: Error: {str(e)}\n", "error")

        self.output.config(state="disabled")
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

    def print_message(self, args):
        message = " ".join(args)
        self.output.insert(tk.END, f"Output: {message}\n", "output_text")

    def list_directory(self, args):
        directory = args[0] if args else os.getcwd()
        try:
            files = os.listdir(directory)
            self.output.insert(tk.END, f"({directory}) Output:\n", "output_label")
            for file in files:
                self.output.insert(tk.END, f"{file}\n", "output_text")
        except FileNotFoundError:
            self.output.insert(tk.END, f"({directory}) Output: Directory not found\n", "error")

    def change_directory(self, args):
        directory = args[0]
        try:
            os.chdir(directory)
            current_dir = os.getcwd()
            self.status.config(text=f"Current Directory: {current_dir}")
            self.output.insert(tk.END, f"Output: Changed directory to: {current_dir}\n", "output_text")
        except FileNotFoundError:
            self.output.insert(tk.END, f"Output: Directory not found: {directory}\n", "error")

    def create_folder(self, args):
        folder_name = args[0]
        try:
            os.mkdir(folder_name)
            self.output.insert(tk.END, f"Output: Created folder: {folder_name}\n", "output_text")
        except FileExistsError:
            self.output.insert(tk.END, f"Output: Folder already exists: {folder_name}\n", "output_text")
        except FileNotFoundError:
            self.output.insert(tk.END, f"Output: Invalid path: {folder_name}\n", "error")

    def create_file(self, args):
        file_name = args[0]
        try:
            open(file_name, 'w').close()
            self.output.insert(tk.END, f"Output: Created file: {file_name}\n", "output_text")
        except FileExistsError:
            self.output.insert(tk.END, f"Output: File already exists: {file_name}\n", "output_text")
        except FileNotFoundError:
            self.output.insert(tk.END, f"Output: Invalid path: {file_name}\n", "error")

    def delete_files(self, args):
        for file_name in args:
            try:
                os.remove(file_name)
                self.output.insert(tk.END, f"Output: Deleted file: {file_name}\n", "output_text")
            except FileNotFoundError:
                self.output.insert(tk.END, f"Output: File not found: {file_name}\n", "output_text")

    def delete_folders(self, args):
        for folder_name in args:
            try:
                os.rmdir(folder_name)
                self.output.insert(tk.END, f"Output: Deleted folder: {folder_name}\n", "output_text")
            except FileNotFoundError:
                self.output.insert(tk.END, f"Output: Folder not found: {folder_name}\n", "output_text")
            except OSError:
                self.output.insert(tk.END, f"Output: Directory not empty: {folder_name}\n", "output_text")

    def copy_files(self, args):
        try:
            if len(args) != 2:
                raise ValueError("Invalid syntax for 'copy' command")
            source, destination = args
            shutil.copy(source, destination)
            self.output.insert(tk.END, f"Output: Copied file(s)\n", "output_text")
        except ValueError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def move_files(self, args):
        try:
            if len(args) != 2:
                raise ValueError("Invalid syntax for 'move' command")
            source, destination = args
            shutil.move(source, destination)
            self.output.insert(tk.END, f"Output: Moved file(s)\n", "output_text")
        except ValueError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def rename_file(self, args):
        try:
            if len(args) != 2:
                raise ValueError("Invalid syntax for 'rename' command")
            old_name, new_name = args
            os.rename(old_name, new_name)
            self.output.insert(tk.END, f"Output: Renamed {old_name} to {new_name}\n", "output_text")
        except ValueError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def list_processes(self, args):
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            self.output.insert(tk.END, f"Output: \n", "output_label")
            self.output.insert(tk.END, result.stdout, "output_text")
        except Exception as e:
            self.output.insert(tk.END, f"Output: Error executing 'tasklist' command: {e}\n", "error")

    def kill_process(self, args):
        process_name = args[0]
        try:
            subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
            self.output.insert(tk.END, f"Output: Task(s) terminated successfully\n", "output_text")
        except subprocess.CalledProcessError as e:
            self.output.insert(tk.END, f"Output: Error executing 'taskkill' command: {e}\n", "error")

    def show_help(self, args=None):
        self.output.insert(tk.END, "List of available commands:\n\n", "output_label")
        for cmd, (description, syntax) in commands.items():
            self.output.insert(tk.END, f"{cmd}: {description}\nSyntax: {syntax}\n\n", "output_text")

    def clear_output(self, args=None):
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)
        self.output.config(state="disabled")

if __name__ == "__main__":
    app = BerryPrompt()
    app.mainloop()
