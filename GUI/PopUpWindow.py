import tkinter as tk
from tkinter import filedialog
from Tools.LoadXML import LoadXML
import Constants


class LoadModuleWindow(tk.Toplevel):
    """Creates a window to import test case modules"""
    def __init__(self, window):
        super().__init__(window)
        # Assign the given arguments
        self.controller = window

        # Configure the window
        self.overrideredirect(1)
        self.attributes('-topmost', True)
        self.geometry("400x130+%d+%d" % (self.winfo_screenwidth() * 0.4, self.winfo_screenheight() * 0.4))
        self.configure(bg=Constants.dark_color)
        self.grab_set()

        # Create the variables
        self.top_bar = None
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
        self.path_string = ""

        # Init methods of the window
        self.create_top_bar()
        self.create_main_frame()
        self.set_title("Load test module")

    def create_top_bar(self):
        """ Creates the top bar of the window, which includes the title and the close button"""
        # Create the elements of the top bar
        self.top_bar = tk.Frame(self,
                                bg=Constants.dark_color)

        self.close = tk.Button(self.top_bar,
                               text="X",
                               font=Constants.title_font(),
                               bg=Constants.dark_color,
                               fg=Constants.text_color,
                               bd=0,
                               command=lambda: self.destroy())

        self.label = tk.Label(self.top_bar,
                              text="",
                              font=Constants.title_font(),
                              fg=Constants.text_color,
                              bg=Constants.dark_color)
        # Pack the elements
        self.top_bar.pack(fill=tk.X, anchor="n")
        self.close.pack(side="right")
        self.label.pack()

        # bind drag and drop motion to motion methods
        self.top_bar.bind("<B1 Motion>", self._move_window)
        self.top_bar.bind("<Button 1>", self.click_win)
        self.label.bind("<B1 Motion>", self._move_window)
        self.label.bind("<Button 1>", self.click_win)

    def create_main_frame(self):
        """" Create the main frame of the window and it's elements """
        # Create the main frame
        self.main_frame = tk.Frame(self,
                                   bg=Constants.light_color,
                                   bd=10)

        self.main_frame.pack(expand=1, fill="both", padx=3, pady=3)

        # Create the main frame elements
        self.load_button = tk.Button(self.main_frame,
                                     command=lambda: self.file_manager(),
                                     text="file",
                                     bd=1,
                                     relief=tk.RIDGE,
                                     overrelief=tk.RIDGE,
                                     fg=Constants.text_color,
                                     font=Constants.text_font(),
                                     bg=Constants.button_color,)

        self.entry = tk.Entry(self.main_frame,
                              bg=Constants.medium_color,
                              width="33",
                              font=Constants.title_font(),
                              textvariable=self.path_string,
                              fg=Constants.text_color)

        self.error_label = tk.Label(self.main_frame,
                                    text="",
                                    bg=Constants.light_color,
                                    fg="red")

        self.import_button = tk.Button(self.main_frame,
                                       text="Load and run module",
                                       bd=1,
                                       relief=tk.RIDGE,
                                       overrelief=tk.RIDGE,
                                       font=Constants.text_font(),
                                       bg=Constants.button_color,
                                       fg=Constants.text_color,
                                       command=lambda: self.module_import())

        # Grid elements
        self.entry.grid(row=0, column=0)
        self.load_button.grid(row=0, column=3, padx=5)
        self.error_label.grid(row=1, column=0)
        self.import_button.grid(row=3, column=0)

    def set_title(self, title):
        """Set the title of the top bar of the window

        :type title: (str) the new title of the window
        """
        self.label.configure(text=title)

    def set_file_path(self, path):
        """ Set the entry field to the given path

         :type path: (str) The path to be shown on the entry field
         """
        self.path_string = path
        # Delete the current entry field text
        self.entry.delete(0, "end")
        # Write the given path to the entry field
        self.entry.insert("end", path)
        # Scroll to the end of the entry
        self.entry.xview("end")

    def file_manager(self):
        """ Show the Explorer File Manager and set the file path of the selected file to the entry field"""
        # make the window not visible
        self.state("withdraw")
        # Open the file manager
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("Python files", "*.py"),
                                                              ("all files", "*.*")))
        # make the window visible again
        self.state("normal")
        # set the file path
        self.set_file_path(self.filename)

    def module_import(self):
        """ Try import the module with the file path of the entry field. If imported correctly thw window is closed,
        otherwise the error label show a error on the window"""
        try:
            # get the file path of the entry field
            self.path_string = self.entry.get()
            # import the module
            self.controller.set_module(self.path_string)
            # close the window
            self.destroy()
        except Exception as e:
            # Show a error message
            self.error_label.configure(text="Error while loading module. Try again")

    #
    # Motion methods
    #

    def _move_window(self, event=None):
        """ Move the window to the position of the mouse"""
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def click_win(self, event):
        """set the offset of the mouse when moving the window"""
        self._offset_x = event.x
        self._offset_y = event.y


class PopUpLoadXML(tk.Toplevel):

    def __init__(self, window, steps):
        super().__init__(window)
        # Assign the arguments
        self.controller = window
        self.steps = steps
        # Configure Window
        self.overrideredirect(1)
        self.attributes('-topmost', True)
        self.configure(bg=Constants.dark_color)
        self.geometry("400x130+%d+%d" % (self.winfo_screenwidth() * 0.4, self.winfo_screenheight() * 0.4))
        # Create the variables
        self.top_bar = None
        self.path_string = ""
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

        # Init window methods
        self.create_top_bar()
        self.create_main_frame()
        self.set_title("Load XML file")

    def create_top_bar(self):
        """ Creates the top bar of the window, which includes the title and the close button"""
        # Create the elements of the top bar
        self.top_bar = tk.Frame(self,
                                bg=Constants.dark_color)

        self.close = tk.Button(self.top_bar,
                               text="X",
                               font=Constants.title_font(),
                               bg=Constants.dark_color,
                               fg=Constants.text_color,
                               bd=0,
                               command=lambda: self.destroy())

        self.label = tk.Label(self.top_bar,
                              text="",
                              font=Constants.title_font(),
                              fg=Constants.text_color,
                              bg=Constants.dark_color)

        # Pack the elements
        self.top_bar.pack(fill=tk.X, anchor="n")
        self.close.pack(side="right")
        self.label.pack()

        # bind drag and drop motion to motion methods
        self.top_bar.bind("<B1 Motion>", self._move_window)
        self.top_bar.bind("<Button 1>", self.click_win)
        self.label.bind("<B1 Motion>", self._move_window)
        self.label.bind("<Button 1>", self.click_win)

    def create_main_frame(self):

        # Create the main frame of the window
        self.main_frame = tk.Frame(self, bg=Constants.light_color, bd=10)
        self.main_frame.pack(expand=1, fill="both", padx=3, pady=3)

        # Create the elements of the main frame
        self.load_button = tk.Button(self.main_frame,
                                     command=lambda: self.file_manager(),
                                     text="file",
                                     fg=Constants.text_color,
                                     font=Constants.text_font(),
                                     bg=Constants.button_color,
                                     bd=1,
                                     relief=tk.RIDGE,
                                     overrelief=tk.RIDGE,)

        self.entry = tk.Entry(self.main_frame,
                              bg=Constants.medium_color,
                              width="33",
                              font=Constants.title_font(),
                              textvariable=self.path_string,
                              fg=Constants.text_color)

        self.error_label = tk.Label(self.main_frame,
                                    text="",
                                    bg=Constants.light_color,
                                    fg="red")

        self.import_button = tk.Button(self.main_frame,
                                       text="load module",
                                       font=Constants.text_font(),
                                       bg=Constants.button_color,
                                       fg=Constants.text_color,
                                       bd=1,
                                       relief=tk.RIDGE,
                                       overrelief=tk.RIDGE,
                                       command=lambda: self.xml_import())
        # Grid elements
        self.entry.grid(row=0, column=0)
        self.load_button.grid(row=0, column=3, padx=5)
        self.error_label.grid(row=1, column=0)
        self.import_button.grid(row=3, column=0)

    def set_title(self, title):
        """Set the title of the top bar of the window

        :type title: (str) the new title of the window
        """
        self.label.configure(text=title)

    def set_file_path(self, path):
        """ Set the entry field to the given path

         :type path: (str) The path to be shown on the entry field
         """
        self.path_string = path
        # Delete the current entry field text
        self.entry.delete(0, "end")
        # Write the given path to the entry field
        self.entry.insert("end", path)
        # Scroll to the end of the entry
        self.entry.xview("end")

    def file_manager(self):
        """ Show the Explorer File Manager and set the file path of the selected file to the entry field"""
        # make the window not visible
        self.state("withdraw")
        # Open the file manager
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("XML files", "*.xml"),
                                                              ("all files", "*.*")))
        # make the window visible again
        self.state("normal")
        # set the file path
        self.set_file_path(self.filename)

    def xml_import(self):
        """try to import the XML file of the entry field. If succeed then closes the window. If not, then shows
        a error message"""
        # Instance the LoadXML module
        load = LoadXML(self.controller, self.steps)
        try:
            # Read the XML File
            self.controller.clear_all()
            load.load_file(self.entry.get())
        except FileNotFoundError:
            # Show a message error
            self.error_label.configure(text="Can't load that file. Try again")
        else:
            # Show the hidden buttons of the main window
            self.controller.show_buttons()
            self.controller.update_all()
            # Close the window
            self.destroy()

    #
    # Motion methods
    #

    def _move_window(self, event=None):
        """ Move the window to the position of the mouse"""
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def click_win(self, event):
        """set the offset of the mouse when moving the window"""
        self._offset_x = event.x
        self._offset_y = event.y
