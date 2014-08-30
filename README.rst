logaugment
==========

Python logging library for augmenting log records with additional information.

This library supports Python 2.7+.

If you want custom keys in your logged string:

.. code:: python

    formatter = logging.Formatter("%(message)s: %(custom_key)s")

then this library allows you to add them easily:

.. code:: python

    logaugment.add(logger, custom_key='custom_value')
    logger.warn("My message")
    # My message: custom_value

Why?
====

If you need to add custom keys to your Python logging strings you need to pass
them in with each logging call. That is inconvenient so this library allows you
to add values just once and they're then available for all logging calls
afterwards.

Here is a full example:

.. code:: python

    import logging
    import logaugment
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s: %(custom_key)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logaugment.add(logger, custom_key='custom_value')
    logger.warn("My message")
    # My message: custom_value

Examples
========

You can use keywords to specify additional values:

.. code:: python

    logaugment.add(logger, custom_key='custom_value')
    logger.warn("My message")
    # My message: custom_value

You can also use a dictionary to specify the keys / values:

.. code:: python

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message")
    # My message: custom_value

You can also use a function which returns a dictionary:

.. code:: python

    logaugment.add(logger, lambda record: {'custom_key': record.levelname})
    logger.warn("My message")
    # My message: WARNING

You can pass an `extra` dictionary in the call which overrides the
augmented data:

.. code:: python

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message", extra={'custom_key': 'extra_value'})
    # My message: extra_value
