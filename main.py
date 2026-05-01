import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.tasks = []
        self.history = []
        self.load_data()

        # Предопределённые задачи
        self.predefined_tasks = [
            {"task": "Прочитать статью", "category": "учёба"},
            {"task": "Сделать зарядку", "category": "спорт"},
            {"task": "Написать отчёт", "category": "работа"},
            {"task": "Посмотреть лекцию", "category": "учёба"},
            {"task": "Прогуляться 30 минут", "category": "спорт"},
            {"task": "Разобрать почту", "category": "работа"}
        ]
        self.tasks.extend(self.predefined_tasks)

        # --- Интерфейс ---
        # Поля ввода
        tk.Label(root, text="Новая задача").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value="учёба")
        self.category_menu = ttk.Combobox(root, textvariable=self.category_var,
                                          values=["учёба", "спорт", "работа"])
        self.category_menu.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(root, text="Добавить задачу", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Сгенерировать задачу", command=self.generate_task).grid(row=3, column=0, columnspan=2, pady=5)

        # Фильтр по категории
        tk.Label(root, text="Фильтр по категории").grid(row=4, column=0, padx=5)
        self.filter_var = tk.StringVar(value="все")
        ttk.Combobox(root, textvariable=self.filter_var,
                     values=["все", "учёба", "спорт", "работа"]).grid(row=4, column=1, padx=5)
        tk.Button(root, text="Применить фильтр", command=self.filter_history).grid(row=4, column=2, padx=5)

        # История задач
        self.history_listbox = tk.Listbox(root, width=50, height=12)
        self.history_listbox.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Заполнение истории
        self.update_history_display()

    def add_task(self):
        task = self.task_entry.get().strip()
        category = self.category_var.get()

        if not task:
            messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
            return

        self.tasks.append({"task": task, "category": category})
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{task}' добавлена в список.")

    def generate_task(self):
         if not self.tasks:
             messagebox.showwarning("Внимание", "Список задач пуст. Добавьте задачи!")
             return

         selected = random.choice(self.tasks)
         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         self.history.append({"task": selected["task"], "category": selected["category"], "timestamp": timestamp})
         self.update_history_display()
         self.save_data()
         messagebox.showinfo("Ваша задача", f"Задача: {selected['task']}\nКатегория: {selected['category']}")

    def update_history_display(self):
         self.history_listbox.delete(0, tk.END)
         for entry in self.history:
             self.history_listbox.insert(tk.END,
                                         f"[{entry['timestamp']}] {entry['task']} ({entry['category']})")

    def filter_history(self):
         cat = self.filter_var.get()
         self.history_listbox.delete(0, tk.END)
         for entry in self.history:
             if cat == "все" or entry["category"] == cat:
                 self.history_listbox.insert(tk.END,
                                            f"[{entry['timestamp']}] {entry['task']} ({entry['category']})")

    def save_data(self):
         with open("tasks.json", "w", encoding="utf-8") as f:
             json.dump({"tasks": self.tasks, "history": self.history}, f, ensure_ascii=False, indent=4)

    def load_data(self):
         if os.path.exists("tasks.json"):
             with open("tasks.json", "r", encoding="utf-8") as f:
                 data = json.load(f)
                 self.tasks = data.get("tasks", [])
                 self.history = data.get("history", [])

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()