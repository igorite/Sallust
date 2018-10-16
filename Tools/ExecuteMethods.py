import inspect
import threading
from datetime import datetime
from lxml import etree as et
import TestCase


def _get_class_methods(cls):
    """Get a class as an argument and return a list of it's methods that the method name start with the word 'test'.
     The list is sorted by its line position in the module file
     :type cls: (class)

     :return: (list) of 2 dimension elements:   first element is the method name,
                                                second element is line position of the element
     """
    # Initialize a array to store methods
    methods = []
    # Get all the methods of 'cls' (class)
    cls_methods = dir(cls)
    # start a loop to check if a method is a 'test_method'
    for method in cls_methods:
        # check if the method name starts with 'test'
        if method[0:4] == "test":
            # get a reference to the method
            func = getattr(cls, method)
            # get the line position of the method in it's module file
            position = inspect.findsource(func)[1]
            # add the method and its line position to the list 'methods
            methods.append([method, position])
    # sort the methods by the line position
    methods.sort(key=lambda x: x[1])
    return methods


def _add_step_xml(parent, step_order):
    """Add a step sub element with an attribute order to the given parent
    :type parent: (ElementTree)
    :type step_order: (int)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(parent, "step", {"order": str(step_order)})
    return element


def _add_step_time_xml(step, time):
    """Add a time sub element with it's value to the given step
    :type step: (ElementTree)
    :type time: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "time")
    element.text = time


def _add_step_description(step, description):
    """Add a description sub element with it's value to the given step
    :type step: (ElementTree)
    :type description: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "description")
    element.text = description


def _add_step_status(step, status):
    """Add a status sub element with it's value to the given step
    :type step: (ElementTree)
    :type status: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "status")
    element.text = status


def _add_step_error_message(step, error_message):
    """Add a error sub element with it's value to the given step
    :type step: (ElementTree)
    :type error_message: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "error")
    element.text = error_message


def _get_datetime():
    """Get the current date time and parse it to YYYY-MM-DD_hh-mm

    :return: (string) the current time parsed as YYYY-MM-DD_hh-mm"""
    time = str(datetime.now())
    return time[:10] + "_" + time[11:13] + "-" + time[14:16]


def _parse_time(time):
    """Parse the given time to mm:ss
    :type time: (datetime.timedelta)

    :return: (string) the given time  parsed as mm:ss
    """
    string_time = "%02d:%02d" % (time.seconds % 3600 / 60.0, time.seconds % 60)
    return string_time


class Process(threading.Thread):
    """Read and execute the TestCase and and the results in a Queue in order to transfer the data to the main Thread and
    save the data to a XML file"""
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
        self.time_start = datetime.now()
        # create a XML element that will serve as a root
        self.xml = et.Element("test_run")

    def do(self):
        """Execute all functions of this class to perform is task"""
        # clear the list if they aren't empty
        self._run_methods = []
        self._modules_classes = []
        # get the classes of the module that are subclasses of TestCase
        self._process_module_classes(self._module)
        # execute the methods, evaluate its execution and store its result in a Queue
        self.new_execute_methods()
        # Send the signal that the task has finished
        self.queue.put(["finish_thread", 0])
        # delete the object
        del self

    def _process_module_classes(self, module):
        """Get all the the classes that are subclasses of 'TestCase' of a given module
        and store them in a list named'_module_classes'

        :type module: (module) the module which will be run"""
        for name, obj in inspect.getmembers(module):
            # check the object is a class
            if inspect.isclass(obj):
                # check the class is a subclass of 'TestCase'
                if issubclass(obj, TestCase.TestCase):

                    position = inspect.findsource(obj)[1]
                    self._modules_classes.append([obj, position])
        self._modules_classes.sort(key=lambda x: x[1])

    # noinspection PyBroadException
    def new_execute_methods(self):
        n_test_case = len(self._modules_classes)
        self.queue.put(["n_test_case", n_test_case])
        for i in range(len(self._modules_classes)):
            try:
                cls = self._modules_classes[i][0]()
            except Exception:
                continue
            else:
                pass
            self.time_start = datetime.now()
            step_order = 1
            cls_name = cls.get_name()
            if cls_name is None:
                cls_name = "Test " + str(i+1)
            self.queue.put(["start", cls_name])
            parent_xml = self._add_test_xml(cls_name)
            class_methods = _get_class_methods(cls)
            for method in class_methods:
                func = cls.__getattribute__(method[0])
                description = inspect.getdoc(func)
                if description is None:
                    description = "There is no description of this step"
                try:
                    func()
                except Exception as e:
                    now = datetime.now() - self.time_start
                    elapsed_time = _parse_time(now)
                    self.queue.put(["fail", description, str(e)])
                    step = _add_step_xml(parent_xml, step_order)
                    _add_step_status(step, "failed")
                    _add_step_time_xml(step, elapsed_time)
                    _add_step_description(step, description)
                    if str(e) == "":
                        _add_step_error_message(step, "¯\_(ツ)_/¯")
                    else:
                        _add_step_error_message(step, str(e))
                    step_order += 1
                else:
                    now = datetime.now() - self.time_start
                    elapsed_time = _parse_time(now)
                    self.queue.put(["pass", description])
                    step = _add_step_xml(parent_xml, step_order,)
                    _add_step_status(step, "passed")
                    _add_step_time_xml(step, elapsed_time)
                    _add_step_description(step, description)
                    _add_step_error_message(step, "")

                    step_order += 1
            self.queue.put(["end", cls.get_name()])
            self._save_xml()

    def _add_test_xml(self, name):
        """Create a XML sub element of 'test_run' with the tag'testcase' and with the attribute 'name' which contains
        the test case name

        :return: (ElementTree) the element which has been created"""
        parent = et.SubElement(self.xml, "testcase", {"name": name})
        return parent

    def _save_xml(self):
        """Create a string of the XML element 'test_run' with a pretty format (indented and with end lines)
        that later is writen in a XML file

        :return: None"""
        # Converts to string the 'xml' Element to string
        xml_string = et.tostring(self.xml, encoding='UTF-8', xml_declaration=True, pretty_print=True)
        # Replace the end of line with end of line that some programs can understand
        xml_string.replace(b'\n', b'\r\n')
        # Create a string with the name of the file
        xml_name = "test_history/" + _get_datetime() + ".xml"
        # Create and write the XML data to the file
        with open(xml_name, "wb") as f:
            f.write(xml_string)
            f.close()
        # Add the filename to the Queue in order to be read by the main thread
        self.queue.put(["xml_name", xml_name])

    def get_modules_classes(self):
        """:return: the 'modules_classes'"""
        return self._modules_classes

    def get_run_methods(self):
        """:return: the 'run_methods'"""
        return self._run_methods
