logaugment
==========

Python logging library for augmenting log records with additional information.

If you need to add custom keys to your Python logging strings you can either
add them to each logging call:

.. code:: python

    logger.info("My message: {}".format(value))

or:

.. code:: python

    logger.info("My message", extra={'key': 'value'})

That is inconvenient so this library allows you to add values just once and
they're then available for all logging calls afterwards:

.. code:: python

    import logging
    import logaugment
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s: %(custom_key)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

You can now use a dictionary to specify the keys / values:

.. code:: python

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message")
    # My message: custom_value

You can also use a function which returns a dictionary:

.. code:: python

    logaugment.add(logger, lambda record: {'custom_key': record.levelname})
    logger.warn("My message")
    # My message: WARNING

You can pass the `extra` dictionary which overrides the augmented data:

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message", extra={'custom_key': 'extra_value'})
    # My message: extra_value
