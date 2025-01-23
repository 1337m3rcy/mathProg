import tkinter as tk
from tkinter import ttk, messagebox
from scipy.optimize import linprog
import numpy as np


class SimplexApp:
    def __init__(self, frame):
        self.frame = frame
        self.init_ui()

    def init_ui(self):
        self.frame_setup = ttk.LabelFrame(self.frame, text="Настройки задачи")
        self.frame_setup.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.frame_setup, text="Количество переменных:").grid(row=0, column=0)
        self.num_vars_entry = ttk.Entry(self.frame_setup, width=5)
        self.num_vars_entry.grid(row=0, column=1)

        ttk.Label(self.frame_setup, text="Количество ограничений:").grid(row=1, column=0)
        self.num_constraints_entry = ttk.Entry(self.frame_setup, width=5)
        self.num_constraints_entry.grid(row=1, column=1)

        ttk.Button(self.frame_setup, text="Применить", command=self.setup_problem).grid(
            row=2, column=0, columnspan=2, pady=5
        )

        self.frame_input = None
        self.frame_result = None

    def setup_problem(self):
        if self.frame_input:
            self.frame_input.destroy()
        if self.frame_result:
            self.frame_result.destroy()

        try:
            self.num_vars = int(self.num_vars_entry.get())
            self.num_constraints = int(self.num_constraints_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректное количество переменных и ограничений!")
            return

        # Создание полей для ввода данных
        self.frame_input = ttk.LabelFrame(self.frame, text="Ввод данных")
        self.frame_input.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(self.frame_input, text="Целевая функция:").grid(row=0, column=0, columnspan=2)

        self.obj_func_entries = []
        for i in range(self.num_vars):
            entry = ttk.Entry(self.frame_input, width=5)
            entry.grid(row=1, column=i)
            self.obj_func_entries.append(entry)

        self.obj_func_type = tk.StringVar(value="min")
        ttk.Radiobutton(self.frame_input, text="Min", variable=self.obj_func_type, value="min").grid(row=1, column=self.num_vars)
        ttk.Radiobutton(self.frame_input, text="Max", variable=self.obj_func_type, value="max").grid(row=1, column=self.num_vars + 1)

        ttk.Label(self.frame_input, text="Ограничения:").grid(row=2, column=0, columnspan=2)

        self.constraints_entries = []
        self.constraints_signs = []
        for i in range(self.num_constraints):
            row_entries = []
            for j in range(self.num_vars):
                entry = ttk.Entry(self.frame_input, width=5)
                entry.grid(row=3 + i, column=j)
                row_entries.append(entry)
            self.constraints_entries.append(row_entries)

            sign = tk.StringVar(value="<=")
            combobox = ttk.Combobox(self.frame_input, values=["<=", ">=", "="], textvariable=sign, width=3)
            combobox.grid(row=3 + i, column=self.num_vars)
            self.constraints_signs.append(sign)

            rhs_entry = ttk.Entry(self.frame_input, width=5)
            rhs_entry.grid(row=3 + i, column=self.num_vars + 1)
            row_entries.append(rhs_entry)

        ttk.Button(self.frame_input, text="Рассчитать", command=self.calculate).grid(
            row=4 + self.num_constraints, column=0, columnspan=self.num_vars + 2, pady=5
        )

    def calculate(self):
        try:
            # Получение данных целевой функции
            c = [float(entry.get()) for entry in self.obj_func_entries]

            # Получение данных ограничений
            A_ub, b_ub, A_eq, b_eq = [], [], [], []
            for i, row_entries in enumerate(self.constraints_entries):
                constraint = [float(entry.get()) for entry in row_entries[:-1]]
                rhs = float(row_entries[-1].get())
                sign = self.constraints_signs[i].get()

                if sign == "<=":
                    A_ub.append(constraint)
                    b_ub.append(rhs)
                elif sign == ">=":
                    A_ub.append([-x for x in constraint])
                    b_ub.append(-rhs)
                elif sign == "=":
                    A_eq.append(constraint)
                    b_eq.append(rhs)

            # Преобразование данных в numpy-формат
            c = np.array(c)
            A_ub = np.array(A_ub) if A_ub else None
            b_ub = np.array(b_ub) if b_ub else None
            A_eq = np.array(A_eq) if A_eq else None
            b_eq = np.array(b_eq) if b_eq else None

            # Инвертирование целевой функции для максимизации
            if self.obj_func_type.get() == "max":
                c = -c

            # Решение задачи
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method="simplex")

            if not result.success:
                raise ValueError(result.message)

            # Вывод результата
            if self.frame_result:
                self.frame_result.destroy()
            self.frame_result = ttk.LabelFrame(self.frame, text="Результат")
            self.frame_result.grid(row=2, column=0, padx=10, pady=10)

            ttk.Label(self.frame_result, text=f"Оптимальное значение: {(-1 if self.obj_func_type.get() == 'max' else 1) * result.fun:.2f}").grid(row=0, column=0)
            ttk.Label(self.frame_result, text=f"Решение: {result.x}").grid(row=1, column=0)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при вычислении: {e}")
