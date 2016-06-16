#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_syslogng_kafka
----------------------------------

Tests for `syslogng_kafka` module.
"""

import sys
import unittest

from syslogng_kafka.kafkadriver import KafkaDestination


class TestKafkaDestinaton(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_smoke(self):
        dest = KafkaDestination()
        assert dest is not None


if __name__ == '__main__':
    sys.exit(unittest.main())
