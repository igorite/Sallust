# THIRD PARTY
import gc
import importlib
import queue
import sys
from PIL import Image, ImageTk
# BUILT IN
import tkinter as tk
from tkinter import font as tk_font

# PACKAGE IMPORTS
from GUI import PageXML, Graphics, PopUpWindow, Steps
from Tools import ExecuteMethods
import Constants


class Window(tk.Tk):

    running = True
    # COLORS

    data_tests = []

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconify()
        self.test_passed = 0
        self.test_failed = 0
        self.test_not_run = 1
        self.frames = []
        self.process = None
        self.running = True
        self.thread_running = False
        self.thread = None
        self.run_module = None
        self.run_module_path = ""
        self.total_test_case = 0
        self.current_test_number = 0
        self.current_xml = None
        # BUTTONS
        self.button_steps = None
        self.button_graphics = None
        self.button_xml = None
        self.button_run = None
        self.queue = queue.Queue()
        # INIT METHODS
        self.load_images()
        self._create_window()
        self._create_menu()
        self._create_container()
        self.button_run.configure(state="normal")
        self.deiconify()
        self.geometry("710x%d+%d+0" % (Constants.screen_height*0.95, self.winfo_screenwidth() - 720))

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "Steps":
            self.button_steps.configure(bg=Constants.selected_button_color)
            self.button_graphics.configure(bg=Constants.button_color)
            self.button_xml.configure(bg=Constants.button_color)
        if page_name == "Graphics":
            self.button_steps.configure(bg=Constants.button_color)
            self.button_graphics.configure(bg=Constants.selected_button_color)
            self.button_xml.configure(bg=Constants.button_color)
        if page_name == "PageXML":
            self.button_steps.configure(bg=Constants.button_color)
            self.button_graphics.configure(bg=Constants.button_color)
            self.button_xml.configure(bg=Constants.selected_button_color)

    def clear_all(self):
        self.data_tests = []
        self.test_passed = 0
        self.test_failed = 0
        self.test_not_run = 1
        self.get_frame("Steps").clear_text()

    def update_all(self):
        self.get_frame("PageXML").create_xml()
        self.get_frame("Graphics").update_graphics()
        print(self.data_tests)

    def load_steps(self):
        self.show_frame("Steps")

    def load_graphics(self):
        self.show_frame("Graphics")
        self.get_frame("Graphics").update_graphics()

    def load_xml(self):
        self.show_frame("PageXML")
        self.get_frame("PageXML").create_xml()

    def _move_window(self, event=None):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def _create_container(self):
        self.title_font = tk_font.Font(family='Helvetica',
                                       size=18,
                                       weight="bold",
                                       slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.focus_get()

        self.frames = {}
        for F in (Steps.Steps, Graphics.Graphics, PageXML.PageXML):

            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Steps")

    def _create_window(self):
        self.title(Constants.window_title)
        self.wm_iconbitmap("GUI/img/icon.ico")
        # self.attributes('-topmost', True)
        self.screen_height = self.winfo_screenheight() * 0.96
        self.geometry("700x%d+%d+0" % (Constants.screen_height, self.winfo_screenwidth()-710))
        self.config(bg=Constants.dark_color)
        self.focus_get()

        toolbar = tk.Frame(self, bg=Constants.light_color)

        toolbar.pack(fill="both")
        toolbar.bind('<B1-Motion>', self._move_window)
        self.icon = tk.Label(toolbar,
                             image=Constants.image_icon,
                             bg=Constants.light_color).grid(row=0, column=1, pady=10)

        toolbar.grid_columnconfigure(0, weight=1000)
        toolbar.grid_columnconfigure(1, weight=1)
        toolbar.grid_columnconfigure(4, weight=200)
        toolbar.grid_columnconfigure(5, weight=1000)

    def _create_menu(self):
        menu = tk.Frame(self, bg=Constants.light_color)
        menu.pack(fill="both")
        self.button_steps = tk.Button(menu,
                                      text="Steps",
                                      image=Constants.steps_icon,
                                      compound="left",
                                      height=30,
                                      font=Constants.text_font(),
                                      fg="White",
                                      bd=0,
                                      bg=Constants.button_color,
                                      command=lambda: self.load_steps())

        self.button_graphics = tk.Button(menu,
                                         text="Graphics",
                                         image=Constants.graphs_icon,
                                         compound="left",
                                         height=30,
                                         font=Constants.text_font(),
                                         fg="White",
                                         bd=0,
                                         bg=Constants.button_color,
                                         command=lambda: self.load_graphics())

        self.button_xml = tk.Button(menu,
                                    text="XML",
                                    image=Constants.image_xml,
                                    compound="left",
                                    height=30,
                                    font=Constants.text_font,
                                    fg="White",
                                    bd=0,
                                    bg=Constants.button_color,
                                    command=lambda: self.load_xml())

        self.button_run = tk.Button(menu,
                                    state="disabled",
                                    text="Run Test",
                                    image=Constants.image_run,
                                    compound="left",
                                    height=30,
                                    font=Constants.text_font(),
                                    fg="White",
                                    bd=0,
                                    bg=Constants.green_color,
                                    command=lambda: self.run_test_button())

        self.button_load_xml = tk.Button(menu,
                                         text="Load",
                                         image=Constants.image_load,
                                         compound="left",
                                         height=30,
                                         font=Constants.text_font(),
                                         fg="White",
                                         bd=0,
                                         bg=Constants.button_color,
                                         command=lambda: self.load_xml_button())
        menu.grid_propagate(1)

        self.button_steps.grid(row=0, column=2, padx=2)
        self.button_run.grid(row=0, column=1, padx=2)
        self.button_load_xml.grid(row=0, column=0, padx=2)
        self.button_run.bind("<Enter>", self.on_enter)
        self.button_run.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        if self.thread_running is False:
            self.button_run['background'] = "#0b5cb5"

    def on_leave(self, event=None):
        if self.thread_running is False:
            self.button_run['background'] = "#1eab1e"

    def update_run_button(self):
        if self.total_test_case > len(self.data_tests):
            self.current_test_number = self.total_test_case
        else:
            self.current_test_number = len(self.data_tests) + 1
        status = "(" + str(len(self.data_tests) + 1) + "/" + str(self.current_test_number) + ")"
        self.title(Constants.window_title + " " + status)
        self.button_run.configure(text=status + " Tests")

    def load_xml_button(self):
        PopUpWindow.PopUpLoadXML(self, self.get_frame("Steps"))

    def run_test_button(self):
        pop_up = PopUpWindow.LoadModuleWindow(self)
        pop_up.set_file_path(str(self.run_module_path))

    def show_buttons(self):
        self.button_graphics.grid(row=0, column=3, padx=2)
        self.button_xml.grid(row=0, column=4, padx=2)

    def run_test(self):
        self.clear_all()
        if self.thread_running is False:
            self.thread_running = True
            self.get_frame("Steps").text.delete("1.0", "end")
            self.button_run.configure(text="Running Tests", image=Constants.image_running, bg=Constants.blue_color)
            self.thread = ExecuteMethods.Process(self.get_frame("Steps"), self.queue, self.run_module)
            self.thread.start()
            self.after(0, self.update_run)
        else:
            del self.thread
            gc.collect()
            self.thread_running = False
            self.button_run.configure(state="normal", text="Run Tests", bg=Constants.blue_color)

    @staticmethod
    def load_images():
        """Search and load the images needed for the GUI"""
        Constants.image_fail = ImageTk.PhotoImage(Image.open("GUI/img/fail.png"))
        Constants.image_ok = ImageTk.PhotoImage(Image.open("GUI/img/ok.png"))
        Constants.image_skip = ImageTk.PhotoImage(Image.open("GUI/img/skip.png"))
        Constants.image_ok_test = ImageTk.PhotoImage(Image.open("GUI/img/ok_test.png"))
        Constants.image_fail_test = ImageTk.PhotoImage(Image.open("GUI/img/fail_test.png"))
        Constants.image_run_test = ImageTk.PhotoImage(Image.open("GUI/img/run_test.png"))
        Constants.image_icon = ImageTk.PhotoImage(Image.open("GUI/img/Apyno_logo_small.png"))
        Constants.steps_icon = ImageTk.PhotoImage(Image.open("GUI/img/steps_icon.png"))
        Constants.graphs_icon = ImageTk.PhotoImage(Image.open("GUI/img/graphs_icon.png"))
        Constants.image_run = ImageTk.PhotoImage(Image.open("GUI/img/play_icon.png"))
        Constants.image_running = ImageTk.PhotoImage(Image.open("GUI/img/running.png"))
        Constants.image_xml = ImageTk.PhotoImage(Image.open("GUI/img/xml_icon.png"))
        Constants.image_load = ImageTk.PhotoImage(Image.open("GUI/img/load.png"))
        Constants.image_collapse = ImageTk.PhotoImage(Image.open("GUI/img/collapse_icon.png"))

    def get_frame(self, frame_name):
        return self.frames[frame_name]

    def update_run(self):
        self.update()
        self.update_idletasks()
        steps = self.get_frame("Steps")
        try:
            msg = self.queue.get()
            if msg[0] == "n_test_case":
                self.total_test_case = msg[1]
                self.update_run_button()
            if msg[0] == "finish_thread":
                Window.test_not_run = 0
                self.button_run.configure(state="normal", text="Run Tests", bg=Constants.green_color)
                self.thread_running = False
                self.show_buttons()
                self.update_all()
                pass
            else:
                self.after(0, self.update_run)
            if msg[0] == "start":
                steps.add_test_case(msg[1])
            if msg[0] == "end":
                steps.test_finish()
            if msg[0] == "pass":
                steps.step_pass(msg[1])
            if msg[0] == "fail":
                steps.step_fail(msg[1], msg[2])
            if msg[0] == "xml_name":
                self.current_xml = msg[1]

        except queue.Empty:
            self.after(0, self.update_run)
        finally:
            if self.running is False:
                self.destroy()
                sys.exit(0)

    def set_module(self, path):
        spec = importlib.util.spec_from_file_location("testrun.case", path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        sys.modules["testrun.case"] = imported_module
        self.run_module = imported_module
        self.run_module_path = path
        self.run_test()


if __name__ == "__main__":
    app = Window()
    app.mainloop()
