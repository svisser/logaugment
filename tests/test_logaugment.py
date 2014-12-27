import collections
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
        self.formatter = logging.Formatter(
            "This is the %(message)s: %(custom_key)s")
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

    def test_augment_with_mapping(self):
        class MyMapping(collections.Mapping):

            def __init__(self, *args, **kwargs):
                super(MyMapping, self).__init__()
                self._data = {}
                self._data.update(kwargs)

            def __getitem__(self, key):
                return self._data[key]

            def __iter__(self):
                return iter(self._data)

            def __len__(self):
                return len(self._data)

        logaugment.add(self.logger, MyMapping(custom_key='new-value'))
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: new-value\n")

    def test_augment_with_callable(self):
        def my_callable(record):
            return {'custom_key': record.filename}

        logaugment.add(self.logger, my_callable)
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: test_logaugment.py\n")

    def test_augment_with_callable_dictionary(self):
        class MyDictionary(dict):

            def __call__(self, *args, **kwargs):
                return {'custom_key': 'called_value'}

        my_dict = MyDictionary()
        my_dict['custom_key'] = 'stored_value'
        logaugment.add(self.logger, my_dict)
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: called_value\n")

    def test_augment_with_kwargs(self):
        logaugment.add(self.logger, custom_key='new-value')
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: new-value\n")

    def test_most_recent_value_is_used(self):
        logaugment.add(self.logger, custom_key='custom-value-1')
        logaugment.add(self.logger, custom_key='custom-value-2')
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: custom-value-2\n")

    def test_remove_all_logaugment_adds(self):
        logaugment.add(self.logger, custom_key='custom-value-1')
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: custom-value-1\n")
        self.assertEqual(len(self.logger.filters), 1)
        logaugment.reset(self.logger)
        self.assertEqual(self.logger.filters, [])

    def test_set_combines_add_and_remove(self):
        logaugment.add(self.logger, custom_key='custom-value-1')
        logaugment.set(self.logger, custom_key='custom-value-2')
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: custom-value-2\n")

    def test_latest_set_value_takes_priority(self):
        logaugment.set(self.logger, custom_key='custom-value-2')
        logaugment.add(self.logger, custom_key='custom-value-1')
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: custom-value-1\n")

    def test_none_is_a_valid_value(self):
        logaugment.add(self.logger, custom_key=None)
        self.logger.info('message')
        self.assertEqual(self.stream.getvalue(),
                         "This is the message: None\n")

    def test_at_least_one_custom_key_needed(self):
        with self.assertRaises(ValueError):
            logaugment.add(self.logger)

        with self.assertRaises(ValueError):
            logaugment.set(self.logger)
