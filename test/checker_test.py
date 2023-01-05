from unittest import TestCase


class CheckerTest(TestCase):
    """
    CheckerTest is a class for the unit test of the Checker class,
    running pytest, you can check the validity of functions with coverage.
    """
    def testing_class_catching(self):
        self.assertLogs('Catching CheckerTest on the pytest')