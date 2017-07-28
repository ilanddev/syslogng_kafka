**syslog-ng Apache Kafka destination**

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

- Free software: Apache Software License 2.0
- Documentation: https://syslogng-kafka.readthedocs.io.

============
Introduction
============

**syslogng_kafka** provides a `Python`_ module for `syslog-ng`_ 3.7 allowing one
to filter and forward syslog messages to `Apache Kafka`_ brokers.

The implementation leverages `confluent-kafka`_ which uses the awesome `librdkafka`_
library providing reliability and high performance.

**Please read the** `doc`_ **as in most cases a `pip install` won't work as they are particular requirements that are currently not met by mainstream Linux distributions.**

.. _Python: https://www.python.org/
.. _syslog-ng: https://github.com/balabit/syslog-ng
.. _Apache Kafka: http://kafka.apache.org/
.. _doc: https://syslogng-kafka.readthedocs.io
.. _confluent-kafka: https://github.com/confluentinc/confluent-kafka-python
.. _librdkafka: https://github.com/edenhill/librdkafka


