import tkinter as tk
from tkinter import ttk, messagebox
from sympy import Matrix


class JordanApp:
    def __init__(self, frame):
        self.frame = frame
        self.init_ui()

    def init_ui(self):
        ttk.Label(self.frame, text="Жорданово исключение", font=("Arial", 16)).pack(pady=10)

        self.matrix_frame = ttk.LabelFrame(self.frame, text="Ввод матрицы")
        self.matrix_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.matrix_frame, text="Количество строк:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_entry = ttk.Entry(self.matrix_frame, width=5)
        self.rows_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.matrix_frame, text="Количество столбцов:").grid(row=1, column=0, padx=5, pady=5)
        self.cols_entry = ttk.Entry(self.matrix_frame, width=5)
        self.cols_entry.grid(row=1, column=1, padx=5)

        ttk.Button(self.matrix_frame, text="Установить размер", command=self.setup_matrix).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        self.entries_frame = ttk.Frame(self.matrix_frame)
        self.entries_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_frame = ttk.LabelFrame(self.frame, text="Результат")
        self.result_frame.pack(fill="x", padx=10, pady=10)

    def setup_matrix(self):
        try:
            # Получаем размеры матрицы
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())

            # Очистка старых полей ввода
            for widget in self.entries_frame.winfo_children():
                widget.destroy()

            self.entries = []
            for i in range(self.rows):
                row_entries = []
                for j in range(self.cols):
                    entry = ttk.Entry(self.entries_frame, width=5)
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Кнопка для выполнения Жорданова исключения
            ttk.Button(self.entries_frame, text="Рассчитать", command=self.perform_jordan_elimination).grid(
                row=self.rows, column=0, columnspan=self.cols, pady=10
            )
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные размеры матрицы!")

    def perform_jordan_elimination(self):
        try:
            # Считываем матрицу из полей ввода
            matrix = Matrix(
                [[float(entry.get()) for entry in row] for row in self.entries]
            )

            # Приведение к ступенчатому виду
            reduced_matrix = matrix.rref()[0]

            # Очистка старых результатов
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            # Отображение результата
            for i, row in enumerate(reduced_matrix.tolist()):
                ttk.Label(self.result_frame, text=" | ".join(f"{x:.2f}" for x in row)).pack()
        except ValueError:
            messagebox.showerror("Ошибка", "Заполните все поля матрицы корректными числами!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
