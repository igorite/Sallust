from lxml import etree as et


class LoadXML:

    def __init__(self, controller, steps):
        self.controller = controller
        self.steps = steps

    def load_file(self, path):
        try:
            tree = et.parse(path)
        except Exception:
            raise FileNotFoundError
        root = tree.getroot()
        self.controller.get_frame("PageXML").set_xml(et.tostring(root))
        for i in range(len(root)):
            test_case = root[i]
            self.steps.add_test_case(test_case.get("name"))
            for j in range(len(test_case)):
                elem = test_case[j]
                status = elem[0]
                time = elem[1]
                description = elem[2]
                error_message = elem[3]
                if status.text == "passed":
                    self.steps.step_pass(description.text,time.text)
                if status.text == "failed":
                    self.steps.step_fail(description.text, str(error_message.text),time.text)

            self.steps.test_finish()
