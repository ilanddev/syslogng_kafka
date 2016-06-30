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
from syslogng_kafka.util import date_str_to_timestamp
from syslogng_kafka.util import parse_str_list


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

    def test_parser_str_list(self):
        s = 'x'
        l_s = parse_str_list(s)
        self.assertListEqual(['x'], l_s)

        s = 'x,'
        l_s = parse_str_list(s)
        self.assertListEqual(['x'], l_s)

        s = 'x, '
        l_s = parse_str_list(s)
        self.assertListEqual(['x'], l_s)

        s = 'x, y'
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = 'x, y '
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = ' x, y '
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = ' x , y , '
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = ', x , y , '
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = ', x , y , ,'
        l_s = parse_str_list(s)
        self.assertListEqual(['x', 'y'], l_s)

        s = ''
        l_s = parse_str_list(s)
        self.assertListEqual([], l_s)

        s = ' '
        l_s = parse_str_list(s)
        self.assertListEqual([], l_s)

        s = ' , '
        l_s = parse_str_list(s)
        self.assertListEqual([], l_s)


if __name__ == '__main__':
    sys.exit(unittest.main())
