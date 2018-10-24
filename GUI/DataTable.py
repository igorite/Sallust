import tkinter as tk
import Constants


class DataTable(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=Constants.dark_color)

        self.index_row = 1
        self.index_column = 1
        self.rowconfigure(0, minsize=40)

        for i in range(6):
            self.columnconfigure(i, weight=1)

    def update_all(self):
        self.create_title_row()
        self.create_row()

    def create_title_row(self):
        label_passed_steps = tk.Label(self,
                                      text="Passed Steps",
                                      font=Constants.text_font(),
                                      fg=Constants.text_color,
                                      bg=Constants.medium_color,
                                      bd=10)

        label_failed_steps = tk.Label(self,
                                      text="Failed steps",
                                      font=Constants.text_font(),
                                      fg=Constants.text_color,
                                      bg=Constants.medium_color,
                                      bd=10)

        label_total_steps = tk.Label(self,
                                     text="Total steps",
                                     font=Constants.text_font(),
                                     fg=Constants.text_color,
                                     bg=Constants.medium_color,
                                     bd=10)

        label_percentage_steps = tk.Label(self,
                                          text="% steps",
                                          font=Constants.text_font(),
                                          fg=Constants.text_color,
                                          bg=Constants.medium_color,
                                          bd=10)

        label_passed_steps.grid(row=self.index_row,
                                column=self.index_column,
                                sticky="nwes",
                                padx=1, pady=1)

        label_failed_steps.grid(row=self.index_row,
                                column=self.index_column + 1,
                                sticky="nwes",
                                padx=1, pady=1)

        label_total_steps.grid(row=self.index_row,
                               column=self.index_column + 2,
                               sticky="nwes",
                               padx=1, pady=1)

        label_percentage_steps.grid(row=self.index_row,
                                    column=self.index_column + 3,
                                    sticky="nwes",
                                    padx=1, pady=1)

    def create_row(self):
        for i in range(5):
            label = tk.Label(self, text="row: " + str(i))
            label.grid(row=self.index_row + i + 1, column=self.index_column)
