# -*- coding: utf-8 -*-

"""A library that provides a custom logger for the `KafkaDestination` object."""

import logging
import sys

from syslog_rfc5424_formatter import RFC5424Formatter

LOG = logging.getLogger('syslogng_kafka')
LOG.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.DEBUG)

formatter = RFC5424Formatter()
ch.setFormatter(formatter)

LOG.addHandler(ch)
