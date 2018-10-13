import inspect
import threading

from lxml import etree as ET

import TestCase


class Procesar(threading.Thread):
    """Read and execute the TestCase and and the results in a Queue in order to transfer the data to the main Thread"""

    def __init__(self, steps, queue, module):
        threading.Thread.__init__(self, None, self.do)
        # assign the arguments
        self.queue = queue
        self._test = steps
        self._module = module
        # create empty data
        self._run_methods = []
        self._modules_classes = []
        self.cls = None
        # create a XML element that will serve as a root
        self.xml = ET.Element("test_run")

    def do(self):
        """Execute all functions of this class to perform is task"""
        # clear the list if they aren't empty
        self._run_methods = []
        self._modules_classes = []
        # get the classes of the module that are subclasses of TestCase
        self._proccess_module_classes(self._module)
        # get the methods of the previous classes that it's name start with 'test'
        # self._process_classes_methods(self._modules_classes)
        # sort the methods to keep them in the order they are written in the module
        self._sort_run_methods()
        # execute the methods, evaluate its execution and store its result in a Queue
        # self.execute_methods()
        self.new_execute_methods()
        # delete the Thread
        self.queue.put(["finish_thread", 0])
        del self

    def _proccess_module_classes(self, module):
        """Get all the the classes that are subclasses of 'TestCase' of a given module
        and store them in a list named'_module_classes'

        :argument: module (should be a module)"""
        for name, obj in inspect.getmembers(module):
            # check the object is a class
            if inspect.isclass(obj):
                # check the class is a subclass of 'TestCase'
                if issubclass(obj, TestCase.TestCase):
                    self._modules_classes.append(obj)

    def _process_classes_methods(self, classes_of_module):
        """"Gets all methods of the given classes that it's name start with the words 'test' and store them in a list.
         each element of the list is a list which contains the method class, the method itself and the line position of
         the method in it's module"""
        for cls in classes_of_module:
            # get all the methods of the given class
            cls_methods = dir(cls)
            for method in cls_methods:
                # check if the method name starts with 'test'
                if method[0:4] == "test":
                    func = getattr(cls, method)
                    position = inspect.findsource(func)[1]
                    self._run_methods.append([cls, method, position])

    def _get_class_methods(self, cls):
        methods = []
        cls_methods = dir(cls)
        for method in cls_methods:
            # check if the method name starts with 'test'
            if method[0:4] == "test":
                func = getattr(cls, method)
                position = inspect.findsource(func)[1]
                methods.append([method, position])
        return methods

    def new_execute_methods(self):
        step = 1

        for i in range(len(self._modules_classes)):
            try:
                cls = self._modules_classes[i]()
            except Exception:
                continue
            else:
                pass
            self.queue.put(["start", cls.get_name()])
            parent_XML = self._add_test_XML(cls.get_name())
            class_methods = self._get_class_methods(cls)
            class_methods.sort(key=lambda x: x[1])
            for method in class_methods:
                func = cls.__getattribute__(method[0])
                description = inspect.getdoc(func)
                if description is None:
                    description = "There is no description of this step"
                try:
                    func()
                except Exception as e:
                    self.queue.put(["fail", description + "\n Error:" + str(e)])
                    self._add_step_XML(parent_XML, "fail", step, description)
                    step += 1
                else:
                    self.queue.put(["pass", description])
                    self._add_step_XML(parent_XML, "pass", step, description)
                    step += 1
            self.queue.put(["end", cls.get_name()])

    def _sort_run_methods(self):
        """sort the run methods by its line position on the module"""
        self._run_methods.sort(key=lambda x:  x[2])

    def execute_methods(self):
        test_case = self._run_methods[0][0]().get_name()
        parent_XML = self._add_test_XML(test_case)
        step = 1
        self.cls = self._run_methods[0][0]()
        self.queue.put(["start", test_case])
        for method in self._run_methods:
            method_test_name = method[0]().get_name()
            if method_test_name != test_case:
                self.queue.put(["end", test_case])
                test_case = method_test_name
                self.cls = method[0]()
                self.queue.put(["start", test_case])
                parent_XML = self._add_test_XML(test_case)
                step = 1
            execute = getattr(self.cls, method[1])
            description = inspect.getdoc(execute)
            if description is None:
                description = "There is no description of this step"
            try:
                execute()
            except Exception as e:
                self.queue.put(["fail", description + "\n Error:" + str(e)])
                self._add_step_XML(parent_XML, "fail", step, description)
                step += 1
            else:
                self.queue.put(["pass", description])
                self._add_step_XML(parent_XML, "pass", step, description)
                step += 1
        self.queue.put(["end", test_case])
        self.queue.put(["finish_thread", 0])
        self._save_XML()

    def _add_step_XML(self, parent, status, step, description):
        element = ET.SubElement(parent, "step", {"status": status, "step": str(step)})
        element.text = description

    def _add_test_XML(self, name):
        """Create a XML sub element of 'test_run' with the tag'testcase' and with the attribute 'name' which contains
        the test case name"""
        parent = ET.SubElement(self.xml, "testcase", {"name": name})
        return parent

    def _save_XML(self):
        """Create a string of the XML element 'test_run' with a pretty format (indented and with end lines)
        that later is writen in a XML file"""
        xmlstr = ET.tostring(self.xml, encoding='UTF-8', xml_declaration=True, pretty_print=True)
        xmlstr.replace(b'\n', b'\r\n')
        with open("output.xml", "wb") as f:
            f.write(xmlstr)
            f.close()

    def get_modules_classes(self):
        """return the 'modules_classes'"""
        return self._modules_classes

    def get_run_methods(self):
        """return the 'run_methods'"""
        return self._run_methods
