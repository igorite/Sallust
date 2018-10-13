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

        self.text.pack(expand=1,
                       fill="both")
        self.text.tag_configure("header",
                                font=header_font,
                                background=self.controller.dark_color,
                                foreground="white",
                                spacing1=10,
                                spacing3=10)
        self.text.tag_configure("hidden", elide=True)
        self.text.tag_bind("header", "<Double-1>", self._toggle_visibility)

        scrollb = tk.Scrollbar(self.text, command=self.text.yview)
        scrollb.pack(expand=1, anchor="e", fill=tk.Y)
        self.text['yscrollcommand'] = scrollb.set
        self.text.index("end")
    #
    # WRITE FUNCTIONS
    #

    def test_name(self, name):
        self.test_steps = 0
        self.test_status = True
        self.time_start = datetime.now()
        self.test_name_label = name
        self.test_name_index = self.text.index("end") + "-1 lines"
        self.text.mark_set(name, "end")
        self.text.configure(state="normal")
        self.text.insert("end", self.test_name_label + "\n", "header")
        self.text.configure(state="disabled")
        self.text.see("end")

    def step_pass(self, message):
        self.test_steps += 1
        self.test_steps_passed += 1
        self.text.config(state="normal")
        now = datetime.now() - self.time_start
        self.text.image_create("end", image=self.controller.image_ok)
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message))
        self.text.config(state="disabled")
        self.text.see("end")

    def step_fail(self, message):
        self.test_status = False
        self.test_steps_failed += 1
        self.test_steps = self.test_steps + 1 + self.test_steps_failed
        self.text.config(state="normal")
        now = datetime.now() - self.time_start
        self.text.image_create("end", image=self.controller.image_fail)
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message))
        self.text.config(state="disabled")
        self.text.see("end")

    def step_skip(self, message):
        self.test_steps += 1
        self.text.config(state="normal")
        now = datetime.now() - self.time_start
        self.text.image_create("end", image=self.controller.image_skip)
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message))
        self.text.config(state="disabled")

    def test_finish(self):
        if self.test_status:
            self.text.configure(state="normal")
            self.text.insert(self.test_name_index, "  ", "header")
            self.text.image_create(self.test_name_index, image=self.controller.image_ok_test,
                                   pady=0)
            self.text.configure(state="disabled")
            self.controller.test_passed += 1
        else:
            self.text.configure(state="normal")
            self.text.insert(self.test_name_index, "  ", "header")
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

    def _toggle_visibility(self, event = None):
        block_start, block_end = self._get_block("insert")
        next_hidden = self.text.tag_nextrange("hidden", block_start, block_end)
        if next_hidden:
            self.text.tag_remove("hidden", block_start, block_end + "- 1 char")
        else:
            self.text.tag_add("hidden", block_start, block_end + "- 1 char")

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
