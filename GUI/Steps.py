import tkinter as tk
from datetime import datetime
from tkinter.font import Font


def _parse_time(time):
    """Parse the given time to mm:ss
    :type time: (datetime.timedelta)

    :return: (string) the given time  parsed as mm:ss
     """
    string_time = " (%02d:%02d) " % (time.seconds % 3600 / 60.0, time.seconds % 60)
    return string_time


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
        self.search_visited = None
        self.time_start = datetime.now()
        self.error_button_state = False
        self.passed_button_state = False
        self.text_font = Font(family="Verdana", size=12)
        self.header_font = Font(family="Verdana", size=12)
        # Frame creation methods
        self._create_option_bar()
        self._create_text_widget()

    def _create_option_bar(self):
        """Create the option bar of the window with it's elements, which contains the hide buttons, the search bar
        and the navigation of the search bar.
        """
        # Create option Bar
        self.option_bar = tk.Frame(self, bg=self.controller.medium_color)
        self.option_bar.pack(fill=tk.X)

        # Create option bar elements
        self.passed_button = tk.Checkbutton(self.option_bar,
                                            text="Hide passed",
                                            bd=1,
                                            overrelief=tk.GROOVE,
                                            command=lambda: self.hide_passed(),
                                            font=self.text_font,
                                            indicatoron=False,
                                            bg=self.controller.light_color,
                                            fg="White",
                                            selectcolor=self.controller.dark_color)

        self.error_button = tk.Checkbutton(self.option_bar,
                                           text="Hide error message",
                                           bd=1, overrelief=tk.GROOVE,
                                           command=lambda: self.hide_error_message(),
                                           font=self.text_font,
                                           indicatoron=False,
                                           bg=self.controller.light_color,
                                           fg="White",
                                           selectcolor=self.controller.dark_color)

        self.validator = (self.register(self.search), '%P')

        self.search_bar = tk.Entry(self.option_bar,
                                   text="Search",
                                   fg="White",
                                   font=self.text_font,
                                   width=25,
                                   bg=self.controller.dark_color,
                                   validate="key",
                                   validatecommand=self.validator)

        self.search_next_button = tk.Button(self.option_bar,
                                            text=">",
                                            font=self.text_font,
                                            bd=0,
                                            fg="White",
                                            bg=self.controller.light_color,
                                            command=lambda: self.search_next())

        self.search_previous_button = tk.Button(self.option_bar,
                                                text="<",
                                                font=self.text_font,
                                                bd=0,
                                                fg="White",
                                                bg=self.controller.light_color,
                                                command=lambda: self.search_previous())

        self.results_label = tk.Label(self.option_bar,
                                      text="",
                                      bg=self.controller.medium_color,
                                      fg="White")

        # Grid option bar elements
        self.passed_button.grid(row=0, column=0, pady=5, padx=10)
        self.error_button.grid(row=0, column=1, pady=5, padx=10)
        self.search_bar.grid(row=0, column=2)
        self.results_label.grid(row=0, column=3)
        self.search_previous_button.grid(row=0, column=4)
        self.search_next_button.grid(row=0, column=5)
        self.search_previous_button.grid_remove()
        self.search_next_button.grid_remove()

    def _create_text_widget(self):
        """Creates and configure the text widget in which the data will be writed"""
        # Create Text Widget
        self.text = tk.Text(self,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            wrap="word",
                            state="disabled",
                            font=self.text_font,
                            highlightbackground=self.controller.medium_color,
                            highlightcolor=self.controller.medium_color,
                            highlightthickness=10,
                            bg=self.controller.light_color)
        self.text.pack(expand=1, fill="both")
        self.text.tag_bind("header", "<Double-1>", self._toggle_visibility)

        # Create text widget Scrollbar
        scroll = tk.Scrollbar(self.text, command=self.text.yview)
        scroll.pack(expand=1, anchor="e", fill=tk.Y)
        self.text['yscrollcommand'] = scroll.set

        # Create Tags of the text widget
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
                                font=self.header_font,
                                background=self.controller.medium_color,
                                foreground="white",
                                spacing1=10,
                                spacing3=10,
                                borderwidth=0,
                                relief=tk.RAISED)

        self.text.tag_configure("failed_message",
                                lmargin1=0,
                                lmargin2=0,
                                background="#8d3434",
                                relief=tk.GROOVE,
                                borderwidth=1)

        self.text.tag_configure("hidden",
                                elide=True)

        self.text.tag_configure("selected",
                                background="Blue")

        self.text.tag_configure("passed")

        self.text.tag_configure("failed")

        self.text.tag_configure("failed_message",
                                lmargin1=0,
                                lmargin2=0,
                                background="#8d3434",
                                relief=tk.GROOVE,
                                borderwidth=1)
        self.text.tag_configure("header_hover",
                                background="#c10a0a")

        self.text.tag_configure("passed_header",
                                background="#65c73e")
        self.text.tag_configure("failed_header",
                                background="#c10a0a")

        self.text.tag_configure("passed_hover",
                                background="#695c87")
        self.text.tag_configure("failed_hover",
                                background="#695c87")

        self.text.bind( "<Motion>", self.probando)
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
    def probando(self, event=None):
        self.text.tag_remove("passed_hover", "1.0", "end")
        self.text.tag_remove("failed_hover", "1.0", "end")
        self.text.tag_remove("header_hover", "1.0", "end")
        index = self.text.index("current")
        self.text.tag_raise("passed_hover","passed")
        self.text.tag_add("passed_hover", str(index)+" linestart", str(index) + " lineend + 1 char")
        print(str(self.text.index("current")))

    def probando_2(self, event=None):
        self.text.tag_remove("passed_hover", "1.0", "end")
        self.text.tag_remove("failed_hover", "1.0", "end")
        self.text.tag_remove("header_hover", "1.0", "end")
        index = self.text.index("current")
        self.text.tag_raise("passed_hover","passed")
        self.text.tag_add("failed_hover", str(index)+" linestart", str(index) + " lineend + 1 char")
        print(str(self.text.index("current")))

    def probando_3(self, event=None):
        self.text.tag_remove("passed_hover", "1.0", "end")
        self.text.tag_remove("failed_hover", "1.0", "end")
        self.text.tag_remove("header_hover", "1.0", "end")
        index = self.text.index("current")
        self.text.tag_raise("passed_hover","passed")
        self.text.tag_add("header_hover", str(index)+" linestart", str(index) + " lineend + 1 char")
        print(str(self.text.index("current")))

    def add_test_case(self, name):
        """Print to the text widget a header and start a new test case

        :type name: (str) the name of the test case
        """
        # Set variables
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

        # Add new test case info
        self.text.image_create(self.test_name_index, image=self.controller.image_run_test, pady=0)
        self.text.configure(state="normal")
        self.text.insert("end", " " + self.test_name_label + "\n", "header")
        self.text.configure(state="disabled")

        # update run tests button
        self.controller.update_run_button()

        # set the new line visible if it isn't
        self.text.see("end")

    def step_pass(self, message, time=None):
        """Add a successfully executed step of a test case. it displays the time on completion of the step since
        the start of the test case and the description of the step

        :type message: (str) the description of the step
        :type time: (str) the elapsed time since the start of the test case until the execution of the step
        """
        # Check if variable time is assigned else assign it
        if time is None:
            # Calculate the elapsed time since the start of the test case
            now = datetime.now() - self.time_start
            time = _parse_time(now)
        else:
            # Format the given time
            time = " (" + time + ") "
        # add step info
        self.text.config(state="normal")

        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=self.controller.image_ok)
        self.text.tag_add("passed", image_index, image_index + "+1 char")
        self.text.insert("end", "%s %s \n" % (time, message), "passed")
        now = datetime.now() - self.time_start
        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=self.controller.image_ok)
        self.text.tag_add("passed", image_index, image_index + "+1 char")
        elapsed_time = self._parse_time(now)
        self.text.insert("end", "%s %s \n" % (elapsed_time, message), "passed")

        self.text.config(state="disabled")
        # if new line is not visible scroll down until it's visible
        self.text.see("end")
        # Increase variables
        self.test_steps += 1
        self.test_steps_passed += 1

    def step_fail(self, message, error_message, time=None):
        """Add a failed executed step of a test case. it displays the time on completion of the step since
        the start of the test case, the description of the step and the error message of the step.

        :type message: (str) the description of the step
        :type error_message: (str) the error message of the step
        :type time: (str) the elapsed time since the start of the test case until the execution of the step
        """
        # set the test case status as failed
    def step_fail(self, message, error_message=None):
        self.test_status = False
        # Check if variable time is assigned else assign it
        if time is None:
            now = datetime.now() - self.time_start
            time = _parse_time(now)
        else:
            time = " (" + time + ") "
        # add step info

        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=self.controller.image_fail)
        self.text.tag_add("failed", image_index, image_index + "+1 char")
        self.text.insert("end", "%s  %s \n" % (time, message), "failed")
        # if there is no error message print consequently
        if error_message is "":
            error_message = "¯\_(ツ)_/¯"
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
        # if new line is not visible scroll down until it's visible
        self.text.see("end")
        # Increase variables
        self.test_steps_failed += 1
        self.test_steps += 1

    def test_finish(self):
        """Finish a test case. If any of the test case steps had failed then tags the test case as failed. Otherwise
        tag the test case as passed."""
        if self.test_status:
            # Change the header of the test case
            self.text.configure(state="normal")
            self.text.delete(str(self.test_name_index), str(self.test_name_index) + "+1 chars")
            self.text.insert(self.test_name_index, " ", "header")
            self.text.image_create(str(self.test_name_index), image=self.controller.image_ok_test,
                                   pady=0)
            self.text.tag_add("passed", str(self.test_name_index), str(self.test_name_index) + " lineend + 1 char")
            self.text.tag_add("passed", str(self.test_name_index),str(self.test_name_index) + " lineend + 1 char")
            self.text.configure(state="disabled")
            # increase the variable
            self.controller.test_passed += 1
        else:
            # Change the header of the test case
            self.text.configure(state="normal")
            self.text.delete(str(self.test_name_index), str(self.test_name_index) + "+1 chars")
            self.text.insert(str(self.test_name_index), " ", "header")
            self.text.image_create(self.test_name_index, image=self.controller.image_fail_test,
                                   pady=0)
            self.text.configure(state="disabled")
            # increase the variable
            self.controller.test_failed += 1

        # store the test case results
        self.controller.data_tests.append([self.test_steps_passed, self.test_steps_failed])
        # reset the steps variables
        self.test_steps_passed = 0
        self.test_steps_failed = 0

    #
    # UTILITY FUNCTIONS
    #

    def search(self, search_value):
        """Search in the text widget if there are any coincidences to the given value. If they are then select
        the coincidences.

        :type search_value: (str) the value to be searched"""
        # init variables
        self.search_indexes = []
        search_index = "1.0"
        # remove all previous searched coincidence
        self.text.tag_remove("selected", "1.0", "end")
        # raise selected tag in order to be shown
        self.text.tag_raise("selected", "failed_message")
        # if none value is searched don't search
        if search_value == "":
            self.results_label.configure(text=" No results")
            # hide navigation search bar buttons
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            return True
        # while the search hasn't get to the end of the text, search for the value and store the coincidences index
        while search_index != "+ 1 char":
            try:
                # search the value starting at 'search index' and returns the index if there is a coincidence
                search_index = self.text.search(search_value, search_index, "end", nocase=1)
                if search_index != "":
                    # if the index is not empty store it
                    self.search_indexes.append(search_index)
            except Exception:
                pass
            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"
        # tag the coincidences of the search as selected
        for elem in self.search_indexes:
            try:
                self.text.tag_add("selected", str(elem), str(elem)+" +"+str(len(search_value)) + "char")
            except Exception:
                pass
        # show the navigation bar if necessary
        self.show_navigation_search_bar()
        return True

    def show_navigation_search_bar(self):
        """If there is any coincidence in a search then show the navigation of the search bar"""
        # make the first coincidences as the current
        self.search_visited = 1
        # if there is any coincidence show the results and show the navigation search bar buttons
        if len(self.search_indexes) > 0:
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))
            self.text.see(self.search_indexes[0])
            self.search_next_button.grid()
            self.search_previous_button.grid()
        # else hide the navigation search bar buttons if they were shown
        else:
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            self.results_label.configure(text=" No results")

    def search_next(self):
        """Scroll to the next searched coincidence of the text widget"""
        next_index = self.search_visited
        # check that the next index is inside the list
        if next_index < len(self.search_indexes):
            self.text.see(self.search_indexes[next_index])
            self.search_visited += 1
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))

    def search_previous(self):
        """Scroll to the previous searched coincidence of the text widget"""
        previous_index = self.search_visited - 2
        # check that the previous_index is in range
        if previous_index >= 0:
            # scroll to the previous index
            self.text.see(self.search_indexes[previous_index])
            self.search_visited -= 1
            # change the text to display the right index
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))

    def hide_error_message(self):
        """Hide all the error messages of the text widget if they are visible.
        If they are not visible then set all error messages visible
         """
        if self.error_button_state is False:
            self.error_button_state = True
            self.text.tag_configure("failed_message", elide=True)
        else:
            self.error_button_state = False
            self.text.tag_configure("failed_message", elide=False)

    def hide_passed(self):
        """Hide all the passed steps of the text widget if they are visible.
         If they are not visible then set all the passed steps visible
         """
        if self.passed_button_state is False:
            self.passed_button_state = True
            self.text.tag_configure("passed", elide=True)
        else:
            self.passed_button_state = False
            self.text.tag_configure("passed", elide=False)

    def _toggle_visibility(self, event=None):
        """ hide or show the steps of the 'selected' test case """

        # Lower the tag stack of passed and failed message
        self.text.tag_lower("passed", "hidden")
        self.text.tag_lower("failed_message", "hidden")
        # get the block start and end of the 'elected' test case
    def _toggle_visibility(self, event=None):
        self.text.tag_lower("passed", "hidden")
        self.text.tag_lower("failed_message", "hidden")
        block_start, block_end = self._get_block("insert")
        # get if the block is hidden or not
        next_hidden = self.text.tag_nextrange("hidden", block_start, block_end)
        if next_hidden:
            # make the block visible again
            self.text.tag_remove("hidden", block_start, block_end + "- 1 char")
            self.text.tag_raise("passed", "hidden")
            self.text.tag_raise("failed_message", "hidden")
        else:
            # hide the block
            self.text.tag_add("hidden", block_start, block_end + "- 1 char")
            self.text.tag_lower("failed_message", "hidden")
    def _get_block(self, index):
        """return indices after header, to next header or EOF

        :type index: (str) the index of start of the block

        :returns: (str) the index of start of the block
                  (str) the index of end of the block
        """
        start = self.text.index("%s lineend+1c" % index)
        next_header = self.text.tag_nextrange("header", start)
        if next_header:
            end = next_header[0]
        else:
            end = self.text.index("end")
        return start, end
