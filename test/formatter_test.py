from unittest import TestCase


class FormatterTest(TestCase):
    """
    FormatterTest is a class for the unit test of the Loader class   
    """
    def testing_class_catching(self):
        self.assertLogs('Catching LoaderTest on the pytest')