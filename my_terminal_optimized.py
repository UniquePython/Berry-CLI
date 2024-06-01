import tkinter as tk
from tkinter import scrolledtext
import os
import shutil
import subprocess

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
    "help": ("Displays information about available commands", "help")
}

class BerryPrompt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Berry Prompt")
        self.state('zoomed')
        self.configure(bg="white")
        self.option_add('*Font', 'Arial')
        
        self.create_widgets()

    def create_widgets(self):
        self.output = scrolledtext.ScrolledText(self, bg="white", fg="black", wrap=tk.WORD, font=('Arial', 15), state="disabled")
        self.output.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        self.entry = tk.Text(self, bg="white", fg="black", insertbackground="black", font=('Arial', 15), height=1)
        self.entry.pack(pady=5, padx=10, expand=False, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.focus_set()

        self.output.tag_config("input", foreground="blue")
        self.output.tag_config("output_text", foreground="green")
        self.output.tag_config("error", foreground="red")

    def execute_command(self, event):
        command = self.entry.get("end-1c linestart", "end-1c lineend").strip()
        current_dir = os.getcwd()

        self.output.config(state="normal")
        self.output.insert(tk.END, f"({current_dir}) Input: {command}\n", "input")

        try:
            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "print":
                self.output.insert(tk.END, f"({current_dir}) Output: {' '.join(args)}\n", "output_text")
            elif cmd == "list":
                self.list_directory(current_dir if not args else args[0])
            elif cmd == "cd":
                self.change_directory(args[0])
            elif cmd == "new --folder":
                self.create_folder(args[0])
            elif cmd == "new --file":
                self.create_file(args[0])
            elif cmd == "delete --file":
                self.delete_files(args)
            elif cmd == "delete --folder":
                self.delete_folders(args)
            elif cmd == "copy":
                self.copy_files(args)
            elif cmd == "move":
                self.move_files(args)
            elif cmd == "rename":
                self.rename_file(args)
            elif cmd == "tasklist":
                self.list_processes()
            elif cmd == "taskkill":
                self.kill_process(args[0])
            elif cmd == "help":
                self.show_help()
            elif cmd == "clear":
                self.clear_output()
            elif cmd == "exit":
                self.quit()
            else:
                self.output.insert(tk.END, "Output: Command not recognized\n", "error")

        except Exception as e:
            self.output.insert(tk.END, f"({current_dir}) Output: Error: {str(e)}\n", "error")

        self.output.config(state="disabled")
        self.output.see("end")
        self.entry.delete("end-1c linestart", "end")
        
    def list_directory(self, directory):
        files = os.listdir(directory)
        self.output.insert(tk.END, f"({directory}) Output: \n", "output_label")
        for file in files:
            self.output.insert(tk.END, f"{file}\n", "output_text")

    def change_directory(self, directory):
        os.chdir(directory)
        current_dir = os.getcwd()
        self.output.insert(tk.END, f"({current_dir}) Output: Changed directory to: {current_dir}\n", "output_text")

    def create_folder(self, folder_name):
        try:
            os.mkdir(folder_name)
            self.output.insert(tk.END, f"Output: Created folder: {folder_name}\n", "output_text")
        except FileExistsError:
            self.output.insert(tk.END, f"Output: Folder already exists: {folder_name}\n", "output_text")

    def create_file(self, file_name):
        try:
            open(file_name, 'w').close()
            self.output.insert(tk.END, f"Output: Created file: {file_name}\n", "output_text")
        except FileExistsError:
            self.output.insert(tk.END, f"Output: File already exists: {file_name}\n", "output_text")

    def delete_files(self, file_names):
        for file_name in file_names:
            try:
                os.remove(file_name)
                self.output.insert(tk.END, f"Output: Deleted file: {file_name}\n", "output_text")
            except FileNotFoundError:
                self.output.insert(tk.END, f"Output: File not found: {file_name}\n", "output_text")

    def delete_folders(self, folder_names):
        for folder_name in folder_names:
            try:
                os.rmdir(folder_name)
                self.output.insert(tk.END, f"Output: Deleted folder: {folder_name}\n", "output_text")
            except FileNotFoundError:
                self.output.insert(tk.END, f"Output: Folder not found: {folder_name}\n", "output_text")
            except OSError:
                self.output.insert(tk.END, f"Output: Directory not empty: {folder_name}\n", "output_text")

    def copy_files(self, args):
        try:
            source, destination = args
            shutil.copy(source, destination)
            self.output.insert(tk.END, f"Output: Copied file(s)\n", "output_text")
        except ValueError:
            self.output.insert(tk.END, f"Output: Invalid syntax for 'copy' command\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def move_files(self, args):
        try:
            source, destination = args
            shutil.move(source, destination)
            self.output.insert(tk.END, f"Output: Moved file(s)\n", "output_text")
        except ValueError:
            self.output.insert(tk.END, f"Output: Invalid syntax for 'move' command\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def rename_file(self, args):
        try:
            old_name, new_name = args
            os.rename(old_name, new_name)
            self.output.insert(tk.END, f"Output: Renamed {old_name} to {new_name}\n", "output_text")
        except ValueError:
            self.output.insert(tk.END, f"Output: Invalid syntax for 'rename' command\n", "error")
        except FileNotFoundError as e:
            self.output.insert(tk.END, f"Output: {str(e)}\n", "error")

    def list_processes(self):
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            self.output.insert(tk.END, f"Output: \n", "output_label")
            self.output.insert(tk.END, result.stdout, "output_text")
        except Exception as e:
            self.output.insert(tk.END, f"Output: Error executing 'tasklist' command: {e}\n", "error")

    def kill_process(self, process_name):
        try:
            subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
            self.output.insert(tk.END, f"Output: Task(s) terminated successfully\n", "output_text")
        except subprocess.CalledProcessError as e:
            self.output.insert(tk.END, f"Output: Error executing 'taskkill' command: {e}\n", "error")

    def show_help(self):
        self.output.insert(tk.END, "List of available commands:\n\n", "output_label")
        for cmd, (description, syntax) in commands.items():
            self.output.insert(tk.END, f"{cmd}: {description}\nSyntax: {syntax}\n\n", "output_text")

    def clear_output(self):
        self.output.delete(1.0, tk.END)

if __name__ == "__main__":
    app = BerryPrompt()
    app.mainloop()

