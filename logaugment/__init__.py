import collections
import logging

__title__ = 'logaugment'
__version__ = '0.1.3'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Simeon Visser'


class AugmentFilter(logging.Filter):

    def __init__(self, name='', args=None):
        super(AugmentFilter, self).__init__(name)
        self._args = args

    def filter(self, record):
        if self._args is not None:
            data = {}
            try:
                data = self._args(record)
            except TypeError:
                pass
            if not data and isinstance(self._args, collections.Mapping):
                data = self._args
            if data and not hasattr(record, '_logaugment'):
                record._logaugment = {}
            for key, value in data.items():
                if (record.__dict__.get(key) is None or
                        key in record._logaugment):
                    setattr(record, key, value)
                    record._logaugment[key] = value
        return True


def add(logger, *args, **kwargs):
    if not args and not kwargs:
        raise ValueError("You need to provide at least one "
                         "custom key or function")
    argument = None
    if len(args) == 1 and not kwargs:
        argument = args[0]
    elif not args and kwargs:
        argument = kwargs
    logger.addFilter(
        AugmentFilter(name='logaugment.AugmentFilter', args=argument)
    )


def reset(logger):
    remove = []
    for filter_obj in logger.filters:
        if isinstance(filter_obj, AugmentFilter):
            remove.append(filter_obj)
    for remove_obj in remove:
        logger.removeFilter(remove_obj)


def set(logger, *args, **kwargs):
    reset(logger)
    add(logger, *args, **kwargs)
