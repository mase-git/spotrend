from unittest import TestCase


class CheckerTest(TestCase):
    """
    CheckerTest is a class for the unit test of the Checker class
    """
    def testing_class_catching(self):
        self.assertLogs('Catching CheckerTest on the pytest')