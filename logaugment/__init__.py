import logging


class AugmentFilter(logging.Filter):
        
    def __init__(self, name='', args=None):
        super(AugmentFilter, self).__init__(name)
        self._args = args
    
    def filter(self, record):
        if self._args is not None:
            for key, value in self._args.items():
                setattr(record, key, value)
        return True


def add(logger, args):
    logger.addFilter(
        AugmentFilter(name='logaugment.AugmentFilter', args=args)
    )
