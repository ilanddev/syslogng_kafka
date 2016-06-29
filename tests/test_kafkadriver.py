#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_syslogng_kafka
----------------------------------

Tests for `syslogng_kafka` module.
"""

import sys
import unittest

from syslogng_kafka.kafkadriver import KafkaDestination, date_str_to_timestamp


class TestKafkaDestinaton(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_smoke(self):
        dest = KafkaDestination()
        assert dest is not None

    def test_date_str_to_ts(self):
        date_str = 'Jun 22 12:49:16'
        ts = date_str_to_timestamp(date_str)
        # FIXME will break next year
        expected_ts = '1466599756'
        self.assertEqual(expected_ts, ts)


if __name__ == '__main__':
    sys.exit(unittest.main())
