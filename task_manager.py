import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

DATA_FILE = "tasks.json"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager with Deadline Tracker")
        self.root.geometry("700x400")
        self.tasks = []

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Deadline (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.deadline_entry = tk.Entry(input_frame, width=15)
        self.deadline_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=4, padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Task", "Deadline", "Status"), show="headings", height=10)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")
        self.tree.column("Task", width=250)
        self.tree.column("Deadline", width=120)
        self.tree.column("Status", width=100)
        self.tree.pack()

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Delete Selected", command=self.delete_task).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Save Tasks", command=self.save_tasks).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Refresh Status", command=self.refresh_status).pack(side=tk.LEFT, padx=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not task or not deadline:
            messagebox.showwarning("Input Error", "Please enter both task and deadline.")
            return

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Date Format Error", "Please use YYYY-MM-DD format for deadline.")
            return

        status = "Overdue" if deadline_date < datetime.now().date() else "Upcoming"
        self.tasks.append({"task": task, "deadline": deadline, "status": status})
        self.refresh_tree()
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for t in self.tasks:
            self.tree.insert("", "end", values=(t["task"], t["deadline"], t["status"]))

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
        index = self.tree.index(selected[0])
        del self.tasks[index]
        self.refresh_tree()

    def save_tasks(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Saved", "Tasks saved successfully.")

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.tasks = json.load(f)
            self.refresh_status()

    def refresh_status(self):
        today = datetime.now().date()
        for task in self.tasks:
            try:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                task["status"] = "Overdue" if deadline < today else "Upcoming"
            except ValueError:
                task["status"] = "Invalid"
        self.refresh_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
