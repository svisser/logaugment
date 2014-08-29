import logging


class AugmentFilter(logging.Filter):
        
    def __init__(self, name='', args=None):
        super(AugmentFilter, self).__init__(name)
        self._args = args
    
    def filter(self, record):
        if self._args is not None:
            data = {}
            try:
                if callable(self._args):
                    data = self._args(record)
            except NameError:  # Python 3.1
                if hasattr(self._args, '__call__'):
                    data = self._args(record)
            if isinstance(self._args, dict):
                data = self._args
            for key, value in data.items():
                setattr(record, key, value)
        return True


def add(logger, args):
    logger.addFilter(
        AugmentFilter(name='logaugment.AugmentFilter', args=args)
    )
