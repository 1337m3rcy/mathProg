import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy.optimize import linprog


class TransportationApp:
    def __init__(self, root):
        self.root = root

        # Ввод количества складов и пунктов назначения
        self.frame_setup = ttk.LabelFrame(root, text="Настройки задачи")
        self.frame_setup.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.frame_setup, text="Количество складов:").grid(row=0, column=0)
        self.num_suppliers_entry = ttk.Entry(self.frame_setup, width=5)
        self.num_suppliers_entry.grid(row=0, column=1)

        ttk.Label(self.frame_setup, text="Количество пунктов назначения:").grid(row=1, column=0)
        self.num_destinations_entry = ttk.Entry(self.frame_setup, width=5)
        self.num_destinations_entry.grid(row=1, column=1)

        ttk.Button(self.frame_setup, text="Применить", command=self.setup_problem).grid(row=2, column=0, columnspan=2, pady=5)

        self.frame_input = None
        self.frame_result = None

    def setup_problem(self):
        if self.frame_input:
            self.frame_input.destroy()
        if self.frame_result:
            self.frame_result.destroy()

        try:
            self.num_suppliers = int(self.num_suppliers_entry.get())
            self.num_destinations = int(self.num_destinations_entry.get())
            if self.num_suppliers <= 0 or self.num_destinations <= 0:
                raise ValueError("Количество должно быть положительным!")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректное количество складов и пунктов назначения!")
            return

        self.frame_input = ttk.LabelFrame(self.root, text="Ввод данных")
        self.frame_input.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(self.frame_input, text="Стоимость перевозки:").grid(row=0, column=1, columnspan=self.num_destinations)

        self.cost_entries = []
        for i in range(self.num_suppliers):
            row_entries = []
            for j in range(self.num_destinations):
                entry = ttk.Entry(self.frame_input, width=5)
                entry.grid(row=i + 1, column=j + 1)
                row_entries.append(entry)
            self.cost_entries.append(row_entries)

        ttk.Label(self.frame_input, text="Запасы").grid(row=1, column=self.num_destinations + 1)
        self.supply_entries = []
        for i in range(self.num_suppliers):
            entry = ttk.Entry(self.frame_input, width=5)
            entry.grid(row=i + 1, column=self.num_destinations + 1)
            self.supply_entries.append(entry)

        ttk.Label(self.frame_input, text="Потребности").grid(row=self.num_suppliers + 1, column=1, columnspan=self.num_destinations)
        self.demand_entries = []
        for j in range(self.num_destinations):
            entry = ttk.Entry(self.frame_input, width=5)
            entry.grid(row=self.num_suppliers + 1, column=j + 1)
            self.demand_entries.append(entry)

        ttk.Button(self.frame_input, text="Рассчитать", command=self.solve_transportation).grid(
            row=self.num_suppliers + 2, column=0, columnspan=self.num_destinations + 2, pady=5
        )

    def solve_transportation(self):
        try:
            costs = [[float(entry.get()) for entry in row] for row in self.cost_entries]
            supplies = list(map(float, [entry.get() for entry in self.supply_entries]))
            demands = list(map(float, [entry.get() for entry in self.demand_entries]))

            if any(x < 0 for x in supplies + demands):
                raise ValueError("Запасы и потребности должны быть неотрицательными!")

            costs, supplies, demands = self.balance_problem(costs, supplies, demands)
            result, total_cost = self.solve_with_scipy(costs, supplies, demands)

            if self.frame_result:
                self.frame_result.destroy()
            self.frame_result = ttk.LabelFrame(self.root, text="Результат")
            self.frame_result.grid(row=2, column=0, padx=10, pady=10)

            ttk.Label(self.frame_result, text="Оптимальный план поставок:").grid(row=0, column=1, columnspan=len(result[0]))
            for i in range(len(result)):
                for j in range(len(result[i])):
                    ttk.Label(self.frame_result, text=f"{result[i][j]:.1f}", borderwidth=1, relief="solid", width=10).grid(
                        row=i + 1, column=j + 1
                    )

            ttk.Label(self.frame_result, text=f"Общая стоимость: {total_cost:.1f}").grid(
                row=len(result) + 1, column=0, columnspan=len(result[0]) + 1
            )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def balance_problem(self, costs, supplies, demands):
        supply_sum = sum(supplies)
        demand_sum = sum(demands)

        if supply_sum > demand_sum:
            demands.append(supply_sum - demand_sum)
            for row in costs:
                row.append(0)
        elif demand_sum > supply_sum:
            supplies.append(demand_sum - supply_sum)
            costs.append([0] * len(demands))

        return costs, supplies, demands

    def solve_with_scipy(self, costs, supplies, demands):
        rows, cols = len(supplies), len(demands)
        c = np.array(costs).flatten()

        A_eq = []
        for i in range(rows):
            row = [0] * (rows * cols)
            for j in range(cols):
                row[i * cols + j] = 1
            A_eq.append(row)

        for j in range(cols):
            col = [0] * (rows * cols)
            for i in range(rows):
                col[i * cols + j] = 1
            A_eq.append(col)

        A_eq = np.array(A_eq)
        b_eq = supplies + demands
        bounds = [(0, None)] * (rows * cols)
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

        if not res.success:
            raise ValueError("Задача не имеет решения")

        allocations = np.array(res.x).reshape((rows, cols))
        total_cost = res.fun
        return allocations, total_cost


if __name__ == "__main__":
    root = tk.Tk()
    app = TransportationApp(root)
    root.mainloop()
