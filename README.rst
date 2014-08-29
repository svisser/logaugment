logaugment
==========

Python library for augmenting log records with additional information

If you need to add custom keys to your Python logging strings you can either
add them to each logging call:

.. code:: python

    logger.info("My message: {}".format(value))`

or:

.. code:: python

    logger.info("My message", extra={'key': 'value'})
    
That is inconvenient so this library allows you to add values just once and
they're then available for all logging calls afterwards:

.. code:: python

    >>> import logging, logaugment
    >>> logger = logging.getLogger()
    >>> handler = logging.StreamHandler()
    >>> formatter = logging.Formatter("%(message)s: %(custom_key)s")
    >>> handler.setFormatter(formatter)
    >>> logger.addHandler(handler)

You can now do:

.. code:: python

    >>> logaugment.add(logger, {
    ...     'custom_key': 'custom_value',
    ... })
    >>> logger.warn('My message')
    My message: custom_value
