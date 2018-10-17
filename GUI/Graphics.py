import tkinter as tk
import numpy as np

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.widgets import Slider


class Graphics(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Assign the arguments
        self.controller = controller

        # Configure the frame

        self.configure(bg=self.controller.medium_color)

        # Create Variables
        self.canvas = None
        self.canvas_bars_frame = None
        self.scroll_value = 0.0
        self.higher_test = 0
        self.one = None
        self.sizes = [0, 0]
        self.test_length = 0
        self.labels = "Passed", "Failed"
        self.colors = "#2ba401", "#cd1a1a"
        font = {'family': 'Verdana',
                'weight': 'bold',
                'size': 7}

        # Configure matplotlib
        matplotlib.rc('font', **font)
        matplotlib.rcParams['text.color'] = "#FFFFFF"

        # Create the main frames
        self.pie_frame = tk.Frame(self, bg=self.controller.medium_color)
        self.pie_frame.pack(expand=1, fill="both")

        self.bars_frame = tk.Canvas(self, bg=self.controller.light_color, bd=10)
        self.bars_frame.pack(expand=1, fill="both")

        # Create the figures of the plot
        self.figure_pie = Figure(figsize=(1, 1), dpi=110)
        self.figure_bars = Figure(figsize=(2, 1), dpi=110)

        self.figure_pie.set_facecolor(self.controller.light_color)
        self.figure_bars.set_facecolor(self.controller.light_color)

        self.plot = self.figure_pie.add_subplot(111)
        self.plot_bars = self.figure_bars.add_subplot(111)

        # Create the canvas
        self.canvas = FigureCanvasTkAgg(self.figure_pie, self.pie_frame)
        self.canvas_bars = FigureCanvasTkAgg(self.figure_bars, self.bars_frame)

        # Configure the canvas widget
        self.canvas.get_tk_widget().configure(bg=self.controller.medium_color, bd=10)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=1)

        self.canvas_bars.get_tk_widget().configure(bg=self.controller.medium_color, bd=10)
        self.canvas_bars.get_tk_widget().pack()

        # Draw an empty plot
        self.draw()

    def draw(self):

        # Clear the plots
        self.figure_pie.clear()
        self.figure_bars.clear()

        # Get the test data
        passed = [x[0] for x in self.controller.data_tests]
        failed = [y[1] for y in self.controller.data_tests]
        steps = []

        # Get the number of steps of every test case
        for i in range(len(passed)):
            steps.append(passed[i] + failed[i])

        # Set the higher number of steps
        self.higher_test = 0

        # get the highest number of steps of a single test case
        for i in range(len(steps)):
            if steps[i] > self.higher_test:
                self.higher_test = steps[i]

        # get the number of test case
        self.test_length = len(steps)
        # get evenly spaced values between the number of test
        ind = np.arange(self.test_length)

        # Create the Pie Plot
        self.plot = self.figure_pie.add_subplot(111)
        self.plot.set_title("Results of the TestCase")
        sizes = [self.controller.test_passed, self.controller.test_failed]
        self.plot.pie(sizes,
                      labels=self.labels,
                      shadow=True,
                      colors=self.colors,
                      startangle=90,
                      autopct='%1.1f%%',
                      counterclock=False)

        # Create the Bar plot
        self.plot_bars = self.figure_bars.add_subplot(111, ylabel="Steps", xlabel="Test")
        self.plot_bars.set_title("Case by Case")
        self.plot_bars.spines['bottom'].set_color('#ffffff')
        self.plot_bars.spines['top'].set_color('#ffffff')
        self.plot_bars.spines['right'].set_color('#ffffff')
        self.plot_bars.spines['left'].set_color('#ffffff')
        self.plot_bars.yaxis.label.set_color('#ffffff')
        self.plot_bars.xaxis.label.set_color('#ffffff')
        self.plot_bars.axis([-0.5, self.test_length, 0, self.higher_test * 1.3])
        self.plot_bars.bar(ind, steps, 0.2, color="#cd1a1a")
        self.plot_bars.bar(ind, passed, 0.2, color="#2ba401")
        self.plot_bars.set_facecolor(self.controller.light_color)
        self.plot_bars.set_xticks(ind)
        self.plot_bars.set_xticklabels(range(1,self.test_length+1))
        self.plot_bars.tick_params(direction='out', length=6, width=2, grid_alpha=0.5, color="#ffffff", labelcolor="#ffffff")
        self.canvas.draw()
        if self.test_length > 7:
            ax = self.figure_bars.add_axes([0.125, 0.855, 0.775, 0.03])
            self.one = Slider(ax, "Test", 3, self.test_length - 4)
            del self.one.label
            self.one.on_changed(self.update_slider)
            self.update_slider(0.01)

        self.canvas_bars.get_tk_widget().configure(bg=self.controller.medium_color, bd=10)
        self.canvas_bars.get_tk_widget().pack(expand=1,fill="both")
        self.canvas_bars_frame = self.canvas_bars.get_tk_widget()

        self.canvas_bars.draw()

    def update_slider(self, val):
        pos = self.one.val
        self.one.valtext.set_text("")
        self.plot_bars.axis([pos-3.5, pos + 3.5 , 0, self.higher_test * 1.3])
        self.figure_bars.canvas.draw_idle()
