import os
import tkinter as tk
from tkinter import ttk
import csv

def add_task():
    task = task_entry.get()
    tasks.append(task)
    update_listbox()

def complete_task():
    task = task_listbox.get(task_listbox.curselection())
    tasks.remove(task)
    completed_tasks.append(task)
    update_listbox()
    update_completed_listbox()

def delete_task():
    if task_listbox.curselection():
        task = task_listbox.get(task_listbox.curselection())
        tasks.remove(task)
    elif completed_task_listbox.curselection():
        task = completed_task_listbox.get(completed_task_listbox.curselection())
        completed_tasks.remove(task)

    update_listbox()
    update_completed_listbox()

def update_listbox():
    clear_listbox()
    for task in tasks: 
        task_listbox.insert("end", task)

    write_file()

def update_completed_listbox():
    clear_completed_listbox()
    for task in completed_tasks:
        completed_task_listbox.insert("end", task)

def clear_listbox():
    task_listbox.delete(0, "end")

def clear_completed_listbox():
    completed_task_listbox.delete(0, "end")

# Write the lists to the CSV file
def write_file():
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tasks"] + tasks)
        writer.writerow(["Completed Tasks"] + completed_tasks)

# Load the tasks back 
def load_file():
    global check_list_loaded
    if not check_list_loaded and os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "Tasks":
                    tasks.clear()
                    tasks.extend(row[1:])
                if row[0] == "Completed Tasks":
                    completed_tasks.clear()
                    completed_tasks.extend(row[1:])
        check_list_loaded = True
        update_listbox()
        update_completed_listbox()

# Constants 

BUTTON_HEIGHT = 2
BUTTON_WIDTH = BUTTON_HEIGHT * 4
FILE_NAME = "toDoList.csv"

# Load the check list

check_list_loaded = False

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Apply a style theme
s = ttk.Style()
s.theme_use('clam')
s.configure('TButton', font=('Arial', 11), foreground='#ffffff', background='#1f1f1f', relief='flat')


# Create the tasks list
tasks = []

# Create the completed tasks list
completed_tasks = []

# Create the task entry widget
task_entry = tk.Entry(root)
task_entry.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

# Create the task listbox
task_listbox = tk.Listbox(root)
task_listbox.grid(row=1, column=0, pady=5, sticky="nsew")

# Create the completed task listbox
completed_task_listbox = tk.Listbox(root)
completed_task_listbox.grid(row=1, column=1, pady=5, sticky="nsew")


# BUTTONS

# Create the add task button
add_button = ttk.Button(root, text="Add Task", command=add_task, width=BUTTON_WIDTH, padding=(10, 10))
add_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

# Create the complete task button
complete_button = ttk.Button(root, text="Complete", command=complete_task, width=BUTTON_WIDTH, padding=(10, 10))
complete_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

# Create the delete task button
delete_button = ttk.Button(root, text="Delete", command=delete_task, width=BUTTON_WIDTH, padding=(10, 10))
delete_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

# Set the row and column weights to expand the widgets when the window is resized
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# Start the main event loop
load_file()
root.mainloop()
