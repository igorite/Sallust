import tkinter as tk
from datetime import datetime
from tkinter.font import Font


class Steps(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Frame arguments
        self.parent = parent
        self.controller = controller
        # Variables
        self.time_start = None
        self.text = None
        self.test_steps = 0
        self.test_status = True
        self.test_name_label = None
        self.test_passed = 0
        self.test_failed = 0
        self.test_name_index = 1.0
        self.test_steps_passed = 0
        self.test_steps_failed = 0
        self.search_indexes = []
        self.time_start = datetime.now()
        # Frame creation methods
        self._create_window()

    def _create_window(self):
        text_font = Font(family="Verdana",
                         size=12)
        header_font = Font(family="Verdana",
                           size=12)
        self.text = tk.Text(self,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            wrap="word",
                            state="disabled",
                            font=text_font,
                            highlightbackground=self.controller.medium_color,
                            highlightcolor=self.controller.medium_color,
                            highlightthickness=10,
                            bg=self.controller.light_color)

        self.option_bar = tk.Frame(self, bg=self.controller.medium_color)
        self.option_bar.pack(fill=tk.X)
        self.error_button_state = False
        self.passed_button_state = False
        self.passed_button = tk.Checkbutton(self.option_bar, text="Hide passed", bd=1, overrelief=tk.GROOVE,
                                            command=lambda: self.hide_passed(), font=text_font,
                                            indicatoron=False, bg=self.controller.medium_color,
                                            fg="White", selectcolor=self.controller.dark_color)
        self.passed_button.grid(row=0, column=0, pady=5, padx=10)
        self.error_button = tk.Checkbutton(self.option_bar, text="Hide error message", bd =1, overrelief=tk.GROOVE,
                                           command=lambda: self.hide_error_message(), font=text_font,
                                           indicatoron=False, bg=self.controller.medium_color,
                                           fg="White", selectcolor=self.controller.dark_color)
        self.error_button.grid(row=0, column=1, pady=5, padx=10)
        self.text.pack(expand=1,
                       fill="both")
        self.vcmd = (self.register(self.search), '%P')
        self.search_bar = tk.Entry(self.option_bar, fg="White", font=text_font, width=25, bg=self.controller.dark_color,
                                   validate="key", validatecommand=self.vcmd)
        self.search_bar.grid(row=0, column=2)
        self.search_next_button = tk.Button(self.option_bar, text=">", font=text_font, bd=0,fg="White", bg=self.controller.medium_color, command=lambda : self.search_next())
        self.search_next_button.grid(row=0, column=5)
        self.search_previous_button = tk.Button(self.option_bar, text="<",font=text_font, bd=0,fg="White", bg=self.controller.medium_color, command=lambda: self.search_previous())
        self.search_previous_button.grid(row=0, column=4)
        self.search_previous_button.grid_remove()
        self.search_next_button.grid_remove()
        self.results_label = tk.Label(self.option_bar, text="", bg=self.controller.medium_color,fg="White")
        self.results_label.grid(row=0, column=3)



        self.text.tag_configure("header",
                                font=header_font,
                                background=self.controller.dark_color,
                                foreground="white",
                                spacing1=10,
                                spacing3=10,
                                borderwidth=0,
                                relief=tk.RAISED,
                                    )
        self.text.tag_configure("hidden", elide=True)
        self.text.tag_configure("selected", background="Blue")
        self.text.tag_configure("passed",)
        self.text.tag_configure("failed")
        self.text.tag_configure("failed_message", lmargin1=0, lmargin2=0, background="#8d3434",
                                relief=tk.GROOVE, borderwidth=1)

        self.text.tag_bind("header", "<Double-1>", self._toggle_visibility)
        scroll = tk.Scrollbar(self.text, command=self.text.yview)
        scroll.pack(expand=1, anchor="e", fill=tk.Y)
        self.text['yscrollcommand'] = scroll.set

    #
    # WRITE FUNCTIONS
    #

    def search(self,string2):
        self.text.tag_raise("selected", "failed_message")
        self.search_indexes = []
        search_index = "1.0"
        self.text.tag_remove("selected", "1.0", "end")
        search_value = string2
        if search_value == "":
            self.results_label.configure(text="no results")
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            return True
        print(str(string2))
        while search_index != "+ 1 char":
            try:
                search_index = self.text.search(search_value, search_index,"end", nocase=1)
                if search_index != "":
                    self.search_indexes.append(search_index)
            except:
                pass
            search_index = search_index + "+ 1 char"
        print(self.search_indexes)
        for elem in self.search_indexes:
            try:
                self.text.tag_add("selected",str(elem),str(elem)+" +"+str(len(search_value)) + "char")
            except Exception:
                pass
        self.search_visited = 1
        if len(self.search_indexes) > 0:
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited),len(self.search_indexes)))
            self.text.see(self.search_indexes[0])
            self.search_next_button.grid()
            self.search_previous_button.grid()
        else:
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            self.results_label.configure(text="no results")

        return True

    def search_next(self):
        next_index = self.search_visited
        if next_index < len(self.search_indexes):
            self.text.see(self.search_indexes[next_index])
            self.search_visited += 1
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))

    def search_previous(self):
        next_index = self.search_visited - 2
        if next_index >= 0:
            self.text.see(self.search_indexes[next_index])
            self.search_visited -= 1
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))


    def hide_error_message(self):
        if self.error_button_state is False:
            self.error_button_state = True
            self.text.tag_configure("failed_message", elide=True)
        else:
            self.error_button_state = False
            self.text.tag_configure("failed_message", elide=False)

    def hide_passed(self):
        if self.passed_button_state is False:
            self.passed_button_state = True
            self.text.tag_configure("passed", elide=True)
        else:
            self.passed_button_state = False
            self.text.tag_configure("passed", elide=False)

    def test_name(self, name):
        self.test_steps = 0
        self.test_status = True
        self.time_start = datetime.now()
        self.test_name_label = name
        self.test_name_index = self.text.index("end") + "-1 lines"
        self.text.image_create(self.test_name_index, image=self.controller.image_run_test,
                               pady=0)
        self.text.configure(state="normal")
        self.text.insert("end", " " + self.test_name_label + "\n", "header")
        self.text.configure(state="disabled")
        self.text.see("end")

    def step_pass(self, message):
        self.test_steps += 1
        self.test_steps_passed += 1
        self.text.config(state="normal")
        now = datetime.now() - self.time_start
        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=self.controller.image_ok)
        self.text.tag_add("passed", image_index, image_index + "+1 char")
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message), "passed")
        self.text.config(state="disabled")
        self.text.see("end")

    def step_fail(self, message, error_message=None):
        self.test_status = False
        self.test_steps_failed += 1
        self.test_steps = self.test_steps + 1 + self.test_steps_failed
        self.text.config(state="normal")
        now = datetime.now() - self.time_start
        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=self.controller.image_fail)
        self.text.tag_add("failed", image_index, image_index + "+1 char")
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message), "failed")
        if error_message is "":
            error_message = "There is no error message"
        self.text.insert("end", error_message + "\n", "failed_message")
        self.text.config(state="disabled")
        self.text.see("end")

    def test_finish(self):
        if self.test_status:
            self.text.configure(state="normal")
            self.text.delete(str(self.test_name_index), str(self.test_name_index) + "+1 chars")
            self.text.insert(self.test_name_index, " ", "header")
            self.text.image_create(str(self.test_name_index), image=self.controller.image_ok_test,
                                   pady=0)
            self.text.tag_add("passed", str(self.test_name_index),str(self.test_name_index) + " lineend + 1 char")
            self.text.configure(state="disabled")
            self.controller.test_passed += 1
        else:
            self.text.configure(state="normal")
            self.text.delete(str(self.test_name_index), str(self.test_name_index) + "+1 chars")
            self.text.insert(str(self.test_name_index), " ", "header")
            self.text.image_create(self.test_name_index, image=self.controller.image_fail_test,
                                   pady=0)
            self.text.configure(state="disabled")
            self.controller.test_failed += 1

        self.controller.data_tests.append([self.test_steps_passed, self.test_steps_failed])
        self.test_steps_passed = 0
        self.test_steps_failed = 0

    #
    # UTILITY FUNCTIONS
    #
    def _toggle_visibility(self, event=None):
        self.text.tag_lower("passed", "hidden")
        self.text.tag_lower("failed_message", "hidden")
        block_start, block_end = self._get_block("insert")
        next_hidden = self.text.tag_nextrange("hidden", block_start, block_end)
        if next_hidden:
            self.text.tag_remove("hidden", block_start, block_end + "- 1 char")
            self.text.tag_raise("passed", "hidden")
            self.text.tag_raise("failed_message", "hidden")
        else:
            self.text.tag_add("hidden", block_start, block_end + "- 1 char")
            self.text.tag_lower("failed_message", "hidden")
    def _get_block(self, index):
        """return indices after header, to next header or EOF"""
        start = self.text.index("%s lineend+1c" % index)
        next_header = self.text.tag_nextrange("header", start)
        if next_header:
            end = next_header[0]
        else:
            end = self.text.index("end-1c")
        return start, end

    @staticmethod
    def _parse_time(time):
        string_time = " (%02d:%02d) " % (time.seconds % 3600 / 60.0, time.seconds % 60)
        return string_time
