import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font


class LoadModuleWindow(tk.Toplevel):

    def __init__(self, window):
        super().__init__(window)
        self.controller = window
        self.overrideredirect(1)
        self.attributes('-topmost', True)
        self.top_bar = None
        self.title_font = Font(family="Verdana", size=12)
        self.text_font = Font(family="Verdana", size=12)
        self.main_frame = None
        self.close = None
        self.label = None
        self.load_button = None
        self.filename = None
        self.error_label = None
        self.entry = None
        self.import_button = None
        self._offset_x = 0
        self._offset_y = 0
        self.path_string = tk.StringVar()
        self.grab_set()
        self.menu_bar()
        self.set_title("Load module")

    def menu_bar(self):
        self.geometry("400x130+%d+%d" % (self.winfo_screenwidth()*0.4, self.winfo_screenheight() * 0.4))
        self.configure(bg=self.controller.medium_color)
        self.top_bar = tk.Frame(self, bg=self.controller.medium_color)
        self.main_frame = tk.Frame(self, bg=self.controller.dark_color, bd=10)
        self.close = tk.Button(self.top_bar, text="X", font=self.title_font, bg=self.controller.medium_color,
                               fg=self.controller.text_color, bd=0, command=lambda: self.destroy())
        self.close.pack(side="right")
        self.label = tk.Label(self.top_bar, text="", font=self.title_font, fg=self.controller.text_color,
                              bg=self.controller.medium_color)

        self.load_button = tk.Button(self.main_frame, command=lambda: self.file_manager(), text="file",
                                     fg=self.controller.text_color, font=self.text_font,
                                     bg=self.controller.button_color, bd=0, )
        self.load_button.grid(row=0, column=3,)
        self.entry = tk.Entry(self.main_frame, bg=self.controller.light_color, width="33", font=self.title_font,
                              textvariable=self.path_string, fg=self.controller.text_color)
        self.entry.grid(row=0, column=0)
        self.error_label = tk.Label(self.main_frame, text="", bg=self.controller.dark_color, fg="red")
        self.error_label.grid(row=1, column=0)
        self.import_button = tk.Button(self.main_frame, text="load module", font=self.text_font,
                                       bg=self.controller.button_color, fg=self.controller.text_color, bd=0,
                                       command=lambda: self.module_import())
        self.import_button.grid(row=3, column=0)
        self.label.pack()
        self.top_bar.pack(fill=tk.X, anchor="n")
        self.top_bar.bind("<B1 Motion>", self._move_window)
        self.top_bar.bind("<Button 1>", self.clickwin)
        self.label.bind("<B1 Motion>", self._move_window)
        self.label.bind("<Button 1>", self.clickwin)
        self.main_frame.pack(expand=1, fill="both", padx=3, pady=3)

    def _move_window(self, event=None):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def set_title(self, title):
        self.label.configure(text=title)

    def file_manager(self):
        self.state("withdraw")
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("Python files", "*.py"), ("all files", "*.*")))
        self.state("normal")
        self.entry.delete(0, "end")
        self.path_string = self.filename
        self.entry.insert("end", self.path_string)
        self.entry.xview("end")

    def module_import(self):
        # noinspection PyBroadException
        try:
            self.path_string = self.entry.get()
            self.controller.set_module(self.path_string)
            self.destroy()
        except Exception:
            self.error_label.configure(text="Error while loading module. Try again")
