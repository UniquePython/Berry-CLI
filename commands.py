import os
import shutil
import subprocess

def print_message(app, args):
    message = " ".join(args)
    app.output.insert("end", f"Output: {message}\n", "output_text")

def list_directory(app, args):
    directory = args[0] if args else os.getcwd()
    try:
        files = os.listdir(directory)
        app.output.insert("end", f"({directory}) Output:\n", "output_label")
        for file in files:
            app.output.insert("end", f"{file}\n", "output_text")
    except FileNotFoundError:
        app.output.insert("end", f"({directory}) Output: Directory not found\n", "error")

def change_directory(app, args):
    directory = args[0]
    try:
        os.chdir(directory)
        current_dir = os.getcwd()
        app.status.configure(text=f"Current Directory: {current_dir}")
        app.output.insert("end", f"Output: Changed directory to: {current_dir}\n", "output_text")
    except FileNotFoundError:
        app.output.insert("end", f"Output: Directory not found: {directory}\n", "error")

def create_folder(app, args):
    folder_name = args[0]
    try:
        os.mkdir(folder_name)
        app.output.insert("end", f"Output: Created folder: {folder_name}\n", "output_text")
    except FileExistsError:
        app.output.insert("end", f"Output: Folder already exists: {folder_name}\n", "output_text")
    except FileNotFoundError:
        app.output.insert("end", f"Output: Invalid path: {folder_name}\n", "error")

def create_file(app, args):
    file_name = args[0]
    try:
        open(file_name, 'w').close()
        app.output.insert("end", f"Output: Created file: {file_name}\n", "output_text")
    except FileExistsError:
        app.output.insert("end", f"Output: File already exists: {file_name}\n", "output_text")
    except FileNotFoundError:
        app.output.insert("end", f"Output: Invalid path: {file_name}\n", "error")

def delete_files(app, args):
    for file_name in args:
        try:
            os.remove(file_name)
            app.output.insert("end", f"Output: Deleted file: {file_name}\n", "output_text")
        except FileNotFoundError:
            app.output.insert("end", f"Output: File not found: {file_name}\n", "output_text")

def delete_folders(app, args):
    for folder_name in args:
        try:
            os.rmdir(folder_name)
            app.output.insert("end", f"Output: Deleted folder: {folder_name}\n", "output_text")
        except FileNotFoundError:
            app.output.insert("end", f"Output: Folder not found: {folder_name}\n", "output_text")
        except OSError:
            app.output.insert("end", f"Output: Directory not empty: {folder_name}\n", "output_text")

def copy_files(app, args):
    try:
        if len(args) != 2:
            raise ValueError("Invalid syntax for 'copy' command")
        source, destination = args
        shutil.copy(source, destination)
        app.output.insert("end", f"Output: Copied file(s)\n", "output_text")
    except ValueError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")
    except FileNotFoundError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")

def move_files(app, args):
    try:
        if len(args) != 2:
            raise ValueError("Invalid syntax for 'move' command")
        source, destination = args
        shutil.move(source, destination)
        app.output.insert("end", f"Output: Moved file(s)\n", "output_text")
    except ValueError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")
    except FileNotFoundError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")

def rename_file(app, args):
    try:
        if len(args) != 2:
            raise ValueError("Invalid syntax for 'rename' command")
        old_name, new_name = args
        os.rename(old_name, new_name)
        app.output.insert("end", f"Output: Renamed {old_name} to {new_name}\n", "output_text")
    except ValueError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")
    except FileNotFoundError as e:
        app.output.insert("end", f"Output: {str(e)}\n", "error")

def list_processes(app, args):
    try:
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
        app.output.insert("end", f"Output: \n", "output_label")
        app.output.insert("end", result.stdout, "output_text")
    except Exception as e:
        app.output.insert("end", f"Output: Error executing 'tasklist' command: {e}\n", "error")

def kill_process(app, args):
    process_name = args[0]
    try:
        subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
        app.output.insert("end", f"Output: Task(s) terminated successfully\n", "output_text")
    except subprocess.CalledProcessError as e:
        app.output.insert("end", f"Output: Error executing 'taskkill' command: {e}\n", "error")

def show_help(app, args=None):
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

    app.output.insert("end", "List of available commands:\n\n", "output_label")
    for cmd, (description, syntax) in commands.items():
        app.output.insert("end", f"{cmd}: {description}\nSyntax: {syntax}\n\n", "output_text")

def clear_output(app, args=None):
    app.output.configure(state="normal")
    app.output.delete(1.0, "end")
    app.output.configure(state="disabled")
