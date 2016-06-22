===============================
syslog-ng Kafka driver
===============================

.. image:: https://img.shields.io/pypi/v/syslogng_kafka.svg
        :target: https://pypi.python.org/pypi/syslogng_kafka

.. image:: https://travis-ci.org/ilanddev/syslogng_kafka.svg?branch=master
        :target: https://travis-ci.org/ilanddev/syslogng_kafka

.. image:: https://readthedocs.org/projects/syslogng_kafka/badge/?version=latest
        :target: https://syslogng_kafka.readthedocs.org/en/latest/
        :alt: Documentation Status

.. image:: https://requires.io/github/ilanddev/syslogng_kafka/requirements.svg?branch=master
     :target: https://requires.io/github/ilanddev/syslogng_kafka/requirements/?branch=master
     :alt: Requirements Status

syslog-ng mod-python Kafka driver

* Free software: Apache Software License 2.0
* Documentation: https://syslogng-kafka.readthedocs.io.

============
Introduction
============

TODO

================
Getting the code
================

The code is hosted at https://github.com/ilanddev/syslogng_kafka

Check out the latest development version anonymously with::

    $ git clone https://github.com/ilanddev/syslogng_kafka.git
    $ cd syslogng_kafka

============
Installation
============

At the command line::

    $ pip install syslogng_kafka

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv syslogng_kafka
    $ pip install syslogng_kafka

You can also install syslogng_kafka using the actual source checkout::

    $ git clone https://github.com/ilanddev/syslogng_kafka.git

    $ cd syslogng_kafka

    $ pip install -e .

=============
Running Tests
=============

To run the unit tests::

    $ make test

To run the unit tests for all supported Python interpreters::

    $ make test-all

To check your changes before submitting a pull request::

    $ make lint

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
