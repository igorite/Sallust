import tkinter as tk
import Constants as Constants
import numpy as np


class TestCaseTable(tk.Frame):

    def __init__(self, parent, controller, graphics, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self.controller = controller
        self.graphics = graphics

        self.configure(bg=Constants.light_color)
        self.index_row = 2
        self.index_column = 2

        self.data_table_column = tk.Label(self,
                                          text=" Nº Test ",
                                          font=Constants.text_font(),
                                          fg=Constants.text_color,
                                          bg=Constants.medium_color,
                                          bd=10)

        self.data_table_column_percentage = tk.Label(self,
                                                     text="% Test ",
                                                     font=Constants.text_font(),
                                                     fg=Constants.text_color,
                                                     bg=Constants.medium_color,
                                                     bd=10)

        self.data_table_passed_header = tk.Label(self,
                                                 text="Passed",
                                                 font=Constants.text_font(),
                                                 fg=Constants.text_color,
                                                 bg=Constants.green_color,
                                                 bd=10)

        self.data_table_failed_header = tk.Label(self,
                                                 text="Failed ",
                                                 font=Constants.text_font(),
                                                 fg=Constants.text_color,
                                                 bg=Constants.red_color,
                                                 bd=10)

        self.data_table_passed_result = tk.Label(self,
                                                 text="0",
                                                 font=Constants.text_font(),
                                                 fg=Constants.text_color,
                                                 bg=Constants.ultra_light_color,
                                                 bd=10)

        self.data_table_failed_result = tk.Label(self,
                                                 text="0",
                                                 font=Constants.text_font(),
                                                 fg=Constants.text_color,
                                                 bg=Constants.ultra_light_color,
                                                 bd=10)

        self.data_table_passed_percentage_result = tk.Label(self,
                                                            text="0",
                                                            font=Constants.text_font(),
                                                            fg=Constants.text_color,
                                                            bg=Constants.ultra_light_color,
                                                            bd=10)

        self.data_table_failed_percentage_result = tk.Label(self,
                                                            text="0",
                                                            font=Constants.text_font(),
                                                            fg=Constants.text_color,
                                                            bg=Constants.ultra_light_color,
                                                            bd=10)

        # Grid elements
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(0, minsize=40)
        self.rowconfigure(5, minsize=40)

        self.data_table_column.grid(row=self.index_row,
                                    column=self.index_column + 1,
                                    sticky="nwes",
                                    pady=1, padx=1)

        self.data_table_column_percentage.grid(row=self.index_row,
                                               column=self.index_column + 2,
                                               sticky="nwes",
                                               pady=1, padx=1)

        self.data_table_passed_header.grid(row=self.index_row + 1,
                                           column=self.index_column,
                                           sticky="nwes", pady=1,
                                           padx=1)

        self.data_table_failed_header.grid(row=self.index_row + 2,
                                           column=self.index_column,
                                           sticky="nwes",
                                           pady=1, padx=1)

        self.data_table_passed_result.grid(row=self.index_row + 1,
                                           column=self.index_column + 1,
                                           sticky="nwes",
                                           pady=1, padx=1)

        self.data_table_failed_result.grid(row=self.index_row + 2,
                                           column=self.index_column + 1,
                                           sticky="nwes", pady=1, padx=1)

        self.data_table_passed_percentage_result.grid(row=self.index_row + 1,
                                                      column=self.index_column + 2,
                                                      sticky="nwes",
                                                      pady=1, padx=1)

        self.data_table_failed_percentage_result.grid(row=self.index_row + 2,
                                                      column=self.index_column + 2,
                                                      sticky="nwes",
                                                      pady=1, padx=1)

    def update_table(self):
        self.data_table_passed_result.configure(text=self.controller.test_passed)
        self.data_table_failed_result.configure(text=self.controller.test_failed)

        passed_per = np.round(
            (self.controller.test_passed / (self.controller.test_passed + self.controller.test_failed)) * 100, 1)
        failed_per = np.round(
            (self.controller.test_failed / (self.controller.test_passed + self.controller.test_failed)) * 100, 1)

        self.data_table_passed_percentage_result.configure(text=passed_per)
        self.data_table_failed_percentage_result.configure(text=failed_per)
