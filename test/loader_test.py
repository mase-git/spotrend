from unittest import TestCase


class LoaderTest(TestCase):
    
    def testing_class_catching(self):
        self.assertLogs('Catching LoaderTest on the pytest')