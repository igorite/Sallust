import tkinter as tk
from tkinter.font import Font


class PageXML(tk.Frame):

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

    def create_XML(self):
        self.text.delete("1.0", "end")
        with open("output.xml", "r") as f:
            strxml = f.read()
            self.text.insert("end", strxml)
