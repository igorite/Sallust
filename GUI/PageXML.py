import tkinter as tk
from tkinter.font import Font


class PageXML(tk.Frame):
    """ Load and """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.medium_color)
        text_font = Font(family="Verdana",
                         size=12)
        self.text = tk.Text(self,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            font=text_font,
                            highlightbackground=controller.medium_color,
                            highlightcolor=controller.medium_color,
                            highlightthickness=10,
                            bg=controller.light_color)
        self.text.pack(expand=1, fill="both")
        self.imported_xml = False

    def create_xml(self):
        if self.imported_xml is False:
            self.text.delete("1.0", "end")
            with open(self.controller.current_xml, "r") as f:
                string_xml = f.read()
                self.text.insert("end", string_xml)

    def set_xml(self, string_xml):
        self.imported_xml = True
        self.text.delete("1.0", "end")
        self.text.insert("end", string_xml)
