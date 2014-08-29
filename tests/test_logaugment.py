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
        self.formatter = logging.Formatter("This is the %(message)s: %(custom_key)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.logger.filters = []

    def test_augment_with_dictionary(self):
        logaugment.add(self.logger, {'custom_key': 'new-value'})
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: new-value\n")

    def test_augment_with_dictionary_and_extra(self):
        logaugment.add(self.logger, {'custom_key': 'new-value'})
        self.logger.info('message', extra={'custom_key': 'extra-value'})
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: extra-value\n")

    def test_augment_with_callable(self):
        def my_callable(record):
            return {'custom_key': record.filename}

        logaugment.add(self.logger, my_callable)
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: test_logaugment.py\n")
