import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management Application")
        self.root.geometry("500x500")

        # Initialize task list
        self.tasks = []

        # Create UI components
        self.create_widgets()

        # Load tasks from file
        self.load_tasks()

    def create_widgets(self):
        # Task Entry Frame
        task_frame = tk.Frame(self.root)
        task_frame.pack(pady=10)

        tk.Label(task_frame, text="Task: ").grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(task_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(task_frame, text="Priority (1-5): ").grid(row=1, column=0, padx=5)
        self.priority_entry = tk.Entry(task_frame, width=5)
        self.priority_entry.grid(row=1, column=1, padx=5, sticky='w')

        tk.Label(task_frame, text="Due Date (YYYY-MM-DD): ").grid(row=2, column=0, padx=5)
        self.due_date_entry = tk.Entry(task_frame, width=15)
        self.due_date_entry.grid(row=2, column=1, padx=5, sticky='w')

        add_button = tk.Button(task_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=3, column=1, pady=5, sticky='e')

        # Task List Frame
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, height=15)
        self.task_listbox.pack(pady=10)

        # Task Control Frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        mark_complete_button = tk.Button(control_frame, text="Mark Complete", command=self.mark_task_complete)
        mark_complete_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(control_frame, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=0, column=1, padx=5)

        # Priority Filter Frame
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Priority: ").grid(row=0, column=0, padx=5)
        self.priority_filter = tk.StringVar(value="All")
        priority_options = ["All", "1", "2", "3", "4", "5"]
        self.priority_dropdown = tk.OptionMenu(filter_frame, self.priority_filter, *priority_options, command=self.filter_tasks)
        self.priority_dropdown.grid(row=0, column=1, padx=5)

        # Save tasks when closing the app
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        try:
            priority = int(priority)
            if priority < 1 or priority > 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Priority must be an integer between 1 and 5")
            return

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD.")
            return

        self.tasks.append({"task": task, "priority": priority, "due_date": due_date, "completed": False})
        self.update_task_listbox()

        # Clear input fields
        self.task_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in sorted(self.tasks, key=lambda x: (x["completed"], x["priority"], x["due_date"])):
            status = "✓" if task["completed"] else "✗"
            display_text = f"{status} {task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
            self.task_listbox.insert(tk.END, display_text)

    def mark_task_complete(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["completed"] = True
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as complete")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Select a task to delete")

    def filter_tasks(self, *args):
        selected_priority = self.priority_filter.get()
        self.task_listbox.delete(0, tk.END)
        
        for task in sorted(self.tasks, key=lambda x: (x["completed"], x["priority"], x["due_date"])):
            if selected_priority == "All" or task["priority"] == int(selected_priority):
                status = "✓" if task["completed"] else "✗"
                display_text = f"{status} {task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
                self.task_listbox.insert(tk.END, display_text)

    def save_and_exit(self):
        self.save_tasks()
        self.root.destroy()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                task_str = f"{task['task']}|{task['priority']}|{task['due_date']}|{task['completed']}\n"
                file.write(task_str)

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    task, priority, due_date, completed = line.strip().split("|")
                    self.tasks.append({
                        "task": task,
                        "priority": int(priority),
                        "due_date": datetime.strptime(due_date, "%Y-%m-%d").date(),
                        "completed": completed == "True"
                    })
            self.update_task_listbox()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
