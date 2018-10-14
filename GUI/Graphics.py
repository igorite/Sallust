import tkinter as tk

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Graphics(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        font = {'family': 'Verdana',
                'weight': 'bold',
                'size': 8}
        matplotlib.rc('font', **font)
        self.sizes = [0, 0]
        self.canvas = None
        self.figure = Figure(figsize=(3, 2), dpi=150)
        self.figure.set_facecolor(self.controller.light_color)
        self.plot = self.figure.add_subplot(211)
        self.plot_bars = self.figure.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.labels = "Passed", "Failed"
        self.colors = "#2ba401", "#cd1a1a"
        self.canvas.get_tk_widget().configure(bg=self.controller.medium_color, bd=10)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=1)
        self.draw()

    def draw(self):
        passed = [x[0] for x in self.controller.data_tests]
        failed = [y[1] for y in self.controller.data_tests]
        steps = []
        for i in range(len(passed)):
            steps.append(passed[i] + failed[i])
        n = len(steps)
        ind = np.arange(n)
        self.figure.clear()
        # Pie Plot
        self.plot = self.figure.add_subplot(211)
        sizes = [self.controller.test_passed, self.controller.test_failed]
        self.plot.set_title("Results of the TestCase")
        self.plot.pie(sizes, labels=self.labels, shadow=True, colors=self.colors,
                      startangle=90, autopct='%1.1f%%', counterclock=False)
        # Bars Plot

        self.plot_bars.set_title("Test Case")
        self.plot_bars = self.figure.add_subplot(212, ylabel="Steps", xlabel="Test")
        self.plot_bars.bar(ind, steps, 0.2, color="#cd1a1a")
        self.plot_bars.bar(ind, passed, 0.2, color="#2ba401")
        self.plot_bars.set_facecolor(self.controller.light_color)
        self.plot_bars.set_xticks(ind)
        self.plot_bars.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
        self.canvas.draw()
