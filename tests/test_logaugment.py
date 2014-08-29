import logging
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import logaugment


class LogaugmentTestCase(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler(self.stream)
        self.formatter = logging.Formatter("This is the value: %(custom_key)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
    
    def test_augment_with_dictionary(self):
        logaugment.add(self.logger, {'custom_key': 'new-value'})
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the value: new-value\n")
