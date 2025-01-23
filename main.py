import tkinter as tk
from tkinter import ttk
from jordanElimination.jordanElimination import JordanApp
from simplexMethod.simplexMethod import SimplexApp
from transportationTask.transportationTask import TransportationApp


class GradientFrame(tk.Frame):
    def __init__(self, parent, color1, color2, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self.update_gradient)

    def update_gradient(self, event=None):
        """Обновляет градиентный фон."""
        self.canvas.delete("gradient")
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        # Рисуем градиент построчно
        for i in range(height):
            color = self._interpolate_color(self.color1, self.color2, i / height)
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    def _interpolate_color(self, color1, color2, t):
        """Интерполяция между двумя цветами."""
        r1, g1, b1 = self.winfo_rgb(color1)
        r2, g2, b2 = self.winfo_rgb(color2)
        r = int(r1 + (r2 - r1) * t) >> 8
        g = int(g1 + (g2 - g1) * t) >> 8
        b = int(b1 + (b2 - b1) * t) >> 8
        return f"#{r:02x}{g:02x}{b:02x}"


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математические методы")
        self.root.geometry("800x600")

        # Создаем градиентный фон
        self.gradient_frame = GradientFrame(root, "#FFDEE9", "#B5FFFC")
        self.gradient_frame.pack(fill="both", expand=True)

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.gradient_frame.canvas)
        self.notebook.place(relx=0.5, rely=0.5, anchor="center", width=750, height=550)

        self.add_jordan_tab()
        self.add_simplex_tab()
        self.add_transport_tab()

    def add_jordan_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Жорданово исключение")
        JordanApp(frame)

    def add_simplex_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Симплекс-метод")
        SimplexApp(frame)

    def add_transport_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Транспортная задача")
        TransportationApp(frame)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
