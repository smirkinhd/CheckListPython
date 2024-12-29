import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import os


class CheckboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Чекбокс Заданий")
        self.root.geometry("1024x400")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []
        self.check_vars = []

        self.entry_frame = ttk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        task_label = ttk.Label(self.entry_frame, text="Задание:", font=("Arial", 12))
        task_label.pack(side=tk.LEFT, padx=5)

        self.task_entry = ttk.Entry(self.entry_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        description_label = ttk.Label(self.entry_frame, text="Описание:", font=("Arial", 12))
        description_label.pack(side=tk.LEFT, padx=5)

        self.description_entry = ttk.Entry(self.entry_frame, width=30)
        self.description_entry.pack(side=tk.LEFT, padx=5)

        self.add_task_button = ttk.Button(self.entry_frame, text="Добавить задание", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT)

        self.delete_task_button = ttk.Button(self.entry_frame, text="Удалить выбранные", command=self.delete_selected_tasks)
        self.delete_task_button.pack(side=tk.LEFT)

        self.tasks_frame = ttk.Frame(self.root)
        self.tasks_frame.pack(pady=10)

        tasks_label = ttk.Label(self.tasks_frame, text="Список заданий:", font=("Arial", 14))
        tasks_label.pack(anchor=tk.W)

        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get()
        description_text = self.description_entry.get()

        if task_text:
            task_info = f"{task_text} - {description_text}" if description_text else task_text
            self.tasks.append(task_info)
            var = tk.BooleanVar()
            self.check_vars.append(var)

            checkbox = ttk.Checkbutton(self.tasks_frame, text=task_info, variable=var, command=self.update_task)
            checkbox.pack(anchor=tk.W)

            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

            self.save_tasks()
        else:
            messagebox.showwarning("Предупреждение", "Введите текст задания.")

    def delete_selected_tasks(self):
        for i in reversed(range(len(self.tasks))):
            if self.check_vars[i].get():
                del self.tasks[i]
                del self.check_vars[i]
                for widget in self.tasks_frame.winfo_children():
                    widget.destroy()
                self.create_checkboxes()

        self.save_tasks()

    def create_checkboxes(self):
        for task_info, var in zip(self.tasks, self.check_vars):
            checkbox = ttk.Checkbutton(self.tasks_frame, text=task_info, variable=var, command=self.update_task)
            checkbox.pack(anchor=tk.W)

    def update_task(self):
        completed_tasks = [task for task, var in zip(self.tasks, self.check_vars) if var.get()]
        print("Выполненные задания:", completed_tasks)

    def save_tasks(self):
        with open('tasks.pkl', 'wb') as f:
            data = [(task, var.get()) for task, var in zip(self.tasks, self.check_vars)]
            pickle.dump(data, f)

    def load_tasks(self):
        if os.path.exists('tasks.pkl'):
            with open('tasks.pkl', 'rb') as f:
                data = pickle.load(f)
                for task_info, completed in data:
                    self.tasks.append(task_info)
                    var = tk.BooleanVar(value=completed)
                    self.check_vars.append(var)

                    checkbox = ttk.Checkbutton(self.tasks_frame, text=task_info, variable=var,
                                                   command=self.update_task)
                    checkbox.pack(anchor=tk.W)

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckboxApp(root)
    root.mainloop()
