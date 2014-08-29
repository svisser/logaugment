import logging


class AugmentAddFilter(logging.Filter):
        
    def __init__(self, name='', args=None):
        super(AugmentAddFilter, self).__init__(name)
        self._args = args
    
    def filter(self, record):
        if self._args is not None:
            for key, value in self._args.items():
                setattr(record, key, value)
        return True


def add(logger, args):
    new_filter = AugmentAddFilter(name='logaugment.AugmentAddFilter', args=args)
    logger.addFilter(new_filter)
