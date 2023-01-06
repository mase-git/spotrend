from unittest import TestCase

class SetupTest(TestCase):
    """
    SetupTest is a class to test the pytest function
    """
    def setup(self):
        #  simple log to trigger pytest function
        self.assertLogs('Test: Setup pytest catched.')