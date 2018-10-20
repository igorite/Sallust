import Constants


class ColorizePythonFunctions:

    def __init__(self, steps):
        self.steps = steps
        self.tag = "function"
        self.text = self.steps.text
        self.update_color()

    def update_color(self):
        purple = "#cc60c8"
        code_characters = [" if ", " else:", " finally ", " while ", " try:", " in ", " for ", " raise "]
        for i in code_characters:
            self.colorize(i, Constants.code_character_color)

        self.colorize("self", Constants.purple)
        self.colorize_from_to("def test", '(', Constants.code_character_color)
        self.colorize_from_to('"""', '"""', Constants.string_character_color, to_code_included=True)
        self.colorize_strings('"', '"', Constants.string_character_color, to_code_included=True)
        self.colorize_strings("'", "'", Constants.string_character_color, to_code_included=True)

    def colorize(self, code, color, nocase=1):
        tag_name = "color_" + code
        self.text.tag_configure(tag_name,
                                foreground=color)

        search_index = "1.0"
        while search_index != "+ 1 char":
            try:
                # search the value starting at 'search index' and returns the index if there is a coincidence
                search_index = self.text.search(code, search_index, "end", nocase=nocase)

                tag_names = self.text.tag_names(search_index)
                if "function" in tag_names:
                    code_length = "+" + str(len(code)) + " char"
                    self.text.tag_add(tag_name, search_index, search_index + code_length)
            except Exception:
                pass

            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"

        self.text.tag_raise(tag_name, self.tag)

    def colorize_from_to(self, from_code, to_code, color,to_code_included=False):
        tag_name = "color_" + from_code
        self.text.tag_configure(tag_name,
                                foreground=color)
        from_code_length = "+" + str(len(from_code)) + " char"
        if to_code_included:
            to_code_length = "+" + str(len(to_code)) + " char"
        else:
            to_code_length = ""
        search_index = "1.0"
        search_index_end = None
        while search_index != "+ 1 char":
            try:
                # search the value starting at 'search index' and returns the index if there is a coincidence
                search_index = self.text.search(from_code, search_index, "end", nocase=1)
                search_index_end = self.text.search(to_code, search_index + from_code_length, "end", nocase=1)
                self.text.tag_add(tag_name, search_index, search_index_end + to_code_length)
                search_index = search_index_end
            except Exception:
                pass
            # set the search_index to the current coincidence plus 1 character

            search_index = search_index + "+ 1 char"

        self.text.tag_raise(tag_name, self.tag)

    def colorize_strings(self, from_code, to_code, color, to_code_included=False):
        tag_name = "color_string"
        self.text.tag_configure(tag_name,
                                foreground=color)
        from_code_length = "+" + str(len(from_code)) + " char"
        if to_code_included:
            to_code_length = "+" + str(len(to_code)) + " char"
        else:
            to_code_length = ""
        search_index = "1.0"
        search_index_end = None
        while search_index != "+ 1 char":
            try:
                # search the value starting at 'search index' and returns the index if there is a coincidence
                search_index = self.text.search(from_code, search_index, "end", nocase=1)
                search_index_end = self.text.search(to_code, search_index + from_code_length, "end", nocase=1)

                tag_names = self.text.tag_names(search_index)
                tag_names_end = self.text.tag_names(search_index_end)
                if "function" in tag_names_end:
                    if "function" in tag_names:
                        self.text.tag_add(tag_name, search_index, search_index_end + to_code_length)

                search_index = search_index_end + "+3 char"
            except Exception:
                pass
            # set the search_index to the current coincidence plus 1 character

            search_index = search_index + "+ 1 char"

        self.text.tag_raise(tag_name, self.tag)
