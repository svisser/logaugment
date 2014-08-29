import logging
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import logaugment


class LogaugmentTestCase(unittest.TestCase):
    
    def test_one(self):
        stream = StringIO()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stream)
        formatter = logging.Formatter("This is the value: %(key)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        logaugment.add(logger, {
            'key': 'new-value',
        })
        logger.info('message')
        self.assertEqual(stream.getvalue(), "This is the value: new-value\n")
