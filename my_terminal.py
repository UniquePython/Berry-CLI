import tkinter as tk
from tkinter import scrolledtext
import os
import shutil
import subprocess

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


def execute_command(event):
    current_dir = os.getcwd()

    command = entry.get("end-1c linestart", "end-1c lineend")
    output.config(state="normal")
    output.insert(tk.END, f"({current_dir}) Input: ")
    output.insert(tk.END, command, "input")
    output.insert(tk.END, "\n")

    if command.startswith("print "):
        text = command[6:]
        output.insert(tk.END, f"({current_dir}) Output: ", "output_label")
        output.insert(tk.END, text + "\n", "output_text")
    elif command == "list":
        files = os.listdir('.')
        output.insert(tk.END, f"({current_dir}) Output: \n", "output_label")
        for file in files:
            output.insert(tk.END, f"{file}\n", "output_text")
    elif command.startswith("list "):
        try:
            new_dir = command[5:]
            files = os.listdir(new_dir)
            output.insert(tk.END, f"({current_dir}) Output: \n", "output_label")
            for file in files:
                output.insert(tk.END, f"{file}\n", "output_text")
        except Exception:
            output.insert(tk.END, f"({current_dir}) Output: Could not find the specified directory\n", "error")
    elif command.startswith("cd "):
        directory = command[3:].strip()
        try:
            os.chdir(directory)
            current_dir = os.getcwd()
            output.insert(tk.END, f"({current_dir}) Output:Changed directory to: {current_dir}\n", "output_text")
        except FileNotFoundError:
            output.insert(tk.END, f"Directory not found: {directory}\n", "error")
    elif command.startswith("new --folder "):
        folder_name = command[13:].strip()
        try:
            os.mkdir(folder_name)
            output.insert(tk.END, f"({current_dir}) Output: Created folder: {folder_name}\n", "output_text")
        except FileExistsError:
            output.insert(tk.END, f"({current_dir}) Output: Folder already exists: {folder_name}\n", "output_text")
    elif command.startswith("new --file "):
        file_name = command[11:].strip()
        try:
            open(file_name, 'w').close()
            output.insert(tk.END, f"({current_dir}) Output: Created file: {file_name}\n", "output_text")
        except FileExistsError:
            output.insert(tk.END, f"({current_dir}) Output: File already exists: {file_name}\n", "output_text")
    elif command.startswith("delete --file "):
        files_to_delete = command[14:].split()
        for file_to_delete in files_to_delete:
            try:
                os.remove(file_to_delete)
                output.insert(tk.END, f"({current_dir}) Output: Deleted file: {file_to_delete}\n", "output_text")
            except FileNotFoundError:
                output.insert(tk.END, f"({current_dir}) Output: File not found: {file_to_delete}\n", "output_text")
    elif command.startswith("delete --folder "):
        folders_to_delete = command[16:].split()
        for folder_to_delete in folders_to_delete:
            try:
                os.rmdir(folder_to_delete)
                output.insert(tk.END, f"({current_dir}) Output: Deleted folder: {folder_to_delete}\n", "output_text")
            except FileNotFoundError:
                output.insert(tk.END, f"({current_dir}) Output: Folder not found: {folder_to_delete}\n", "output_text")
            except OSError:
                output.insert(tk.END, f"({current_dir}) Output: Directory not empty: {folder_to_delete}\n", "output_text")
    elif command.startswith("copy "):
        try:
            source, destination = command[5:].split()
            shutil.copy(source, destination)
            output.insert(tk.END, f"({current_dir}) Output: Copied file(s)\n", "output_text")
        except ValueError:
            output.insert(tk.END, f"({current_dir}) Output: Invalid syntax for 'copy' command\n", "error")
        except FileNotFoundError as e:
            output.insert(tk.END, f"({current_dir}) Output: {str(e)}\n", "error")
    elif command.startswith("move "):
        try:
            source, destination = command[5:].split()
            shutil.move(source, destination)
            output.insert(tk.END, f"({current_dir}) Output: Moved file(s)\n", "output_text")
        except ValueError:
            output.insert(tk.END, f"({current_dir}) Output: Invalid syntax for 'move' command\n", "error")
        except FileNotFoundError as e:
            output.insert(tk.END, f"({current_dir}) Output: {str(e)}\n", "error")
    elif command.startswith("rename "):
        try:
            old_name, new_name = command[7:].split()
            os.rename(old_name, new_name)
            output.insert(tk.END, f"({current_dir}) Output: Renamed {old_name} to {new_name}\n", "output_text")
        except ValueError:
            output.insert(tk.END, f"({current_dir}) Output: Invalid syntax for 'rename' command\n", "error")
        except FileNotFoundError as e:
            output.insert(tk.END, f"({current_dir}) Output: {str(e)}\n", "error")
    elif command == "tasklist":
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            output.insert(tk.END, f"({current_dir}) Output: \n", "output_label")
            output.insert(tk.END, result.stdout, "output_text")
        except Exception as e:
            output.insert(tk.END, f"({current_dir}) Output: Error executing 'tasklist' command: {e}\n", "error")
    elif command.startswith("taskkill "):
        try:
            subprocess.run(command, shell=True, check=True)
            output.insert(tk.END, f"({current_dir}) Output: Task(s) terminated successfully\n", "output_text")
        except subprocess.CalledProcessError as e:
            output.insert(tk.END, f"({current_dir}) Output: Error executing 'taskkill' command: {e}\n", "error")
    elif command == "clear": 
        output.delete(1.0, tk.END)  
    elif command == "exit":
        root.quit()
    elif command == "help":
        output.insert(tk.END, "List of available commands:\n\n", "output_label")
        for cmd, (description, syntax) in commands.items():
            output.insert(tk.END, f"{cmd}: {description}\nSyntax: {syntax}\n\n", "output_text")
    else:
        output.insert(tk.END, "Output: Command not recognized\n", "error")

    output.config(state="disabled")
    output.see("end")
    entry.delete("end-1c linestart", "end")

    output.tag_config("input", foreground="blue")
    output.tag_config("output_label", foreground="green")
    output.tag_config("output_text", foreground="blue")
    output.tag_config("error", foreground="red")

root = tk.Tk()
root.title("Berry Prompt")
root.state('zoomed')

root.configure(bg="White")
root.option_add('*Font', 'Arial')

output = scrolledtext.ScrolledText(root, bg="white", fg="black", wrap=tk.WORD, font=('Arial', 15), state="disabled")
output.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

entry = tk.Text(root, bg="white", fg="black", insertbackground="black", font=('Arial', 15), height=1)
entry.pack(pady=5, padx=10, expand=False, fill=tk.X)

entry.bind("<Return>", execute_command)
entry.focus_set()

root.mainloop()