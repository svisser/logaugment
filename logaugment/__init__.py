import logging


def add(logger, args):
    
    class AddFilter(logging.Filter):
        
        def __init__(self, name='', args=None):
            super(AddFilter, self).__init__(name)
            self.args = args
        
        def filter(self, record):
            if self.args is not None:
                for key, value in self.args.items():
                    setattr(record, key, value)
            return True
    
    logger.addFilter(AddFilter(name='logaugment.AddFilter', args=args))
