import logging


class AugmentAddFilter(logging.Filter):
        
    def __init__(self, name='', args=None):
        super(AugmentAddFilter, self).__init__(name)
        self.args = args
    
    def filter(self, record):
        if self.args is not None:
            for key, value in self.args.items():
                setattr(record, key, value)
        return True


def add(logger, args):
    new_filter = AugmentAddFilter(name='logaugment.AugmentAddFilter', args=args)
    logger.addFilter(new_filter)
