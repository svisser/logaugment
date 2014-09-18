logaugment
==========

Python logging library for augmenting log records with additional information.

This library supports Python 2.7.x and Python 3.1+.

If you want custom keys in your logged string:

.. code:: python

    formatter = logging.Formatter("%(message)s: %(custom_key)s")

then this library allows you to set them easily:

.. code:: python

    logaugment.set(logger, custom_key='custom_value')
    logger.warn("My message")
    # My message: custom_value

This allows you to safely make logging calls without getting exceptions
that those keys are missing. See below if you wish to override the value
for a particular logging call.

Installation
============

You can install the library with pip:

.. code:: bash

    $ pip install logaugment

Overview
========

This library provides three functions:

.. code:: python

    # Sets the custom keys and values for the logger.
    logaugment.set(logger, custom_key='custom_value')

    # Adds custom keys and values in addition to those already set.
    logaugment.add(logger, custom_key='custom_value')

    # Removes all custom keys and values for the logger.
    logaugment.reset(logger)

You can use `logaugment.set` to specify custom values for a given logger.

You can use `logaugment.add` to keep the custom values that were already
set and add new ones. If you're redefining a custom key / value then this
value will be used instead of the earlier value.

You can use `logaugment.reset` to remove all additional values that
were added using the `logaugment` library.

Notes on logaugment.add
=======================

The call `logaugment.add` adds default values for that key. You should
not repeatedly call logaugment.add just to change the value - it's
intended as set-once-and-forget functionality. In that case it's
better to use `logaugment.set`.

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

You can also use a dictionary or subclasses of collections.Mapping
to specify the keys / values:

.. code:: python

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message")
    # My message: custom_value

You can also use a function which returns a dictionary:

.. code:: python

    def process_record(record):
        return {'custom_key': record.levelname}

    logaugment.add(logger, process_record)
    logger.warn("My message")
    # My message: WARNING

You can pass an `extra` dictionary in the call which overrides the
augmented data:

.. code:: python

    logaugment.add(logger, {'custom_key': 'custom_value'})
    logger.warn("My message", extra={'custom_key': 'extra_value'})
    # My message: extra_value
