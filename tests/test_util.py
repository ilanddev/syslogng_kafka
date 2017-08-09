#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `syslogng_kafka` module.
"""

import ast
import sys
import unittest

from syslogng_kafka.util import date_str_to_timestamp
from syslogng_kafka.util import parse_firewall_msg
from syslogng_kafka.util import parse_nat_msg
from syslogng_kafka.util import parse_str_list


class TestUtil(unittest.TestCase):
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

    def test_parse_firewall_msg(self):
        msg = '[69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: DROP_131073IN=vNic_0 ' \
              'OUT= MAC=ff:ff:ff:ff:ff:ff:00:50:56:bd:70:59:08:00 ' \
              'SRC=10.11.12.53 ' \
              'DST=10.11.12.255 LEN=229 TOS=0x00 PREC=0x00 TTL=128 ID=13254 ' \
              'PROTO=UDP SPT=138 DPT=138 LEN=209 MARK=0x1'
        msg_s = parse_firewall_msg(msg)

        expected = {'code': -1, 'seq': -1, 'proto': 'UDP', 'tos': '0x00',
                    'ttl': '128', 'len': '209', 'mark': '0x1',
                    'src_ip': '10.11.12.53', 'source_port': '138',
                    'mac_address': 'ff:ff:ff:ff:ff:ff:00:50:56:bd:70:59:08:00',
                    'action': 'drop', 'destination_port': '138', 'out': '',
                    'proc': '0x00', 'id': '13254', 'dest_ip': '10.11.12.255'}

        d1 = ast.literal_eval(str(expected))
        self.assertDictEqual(d1, msg_s)

        msg = '[69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: DROP_131073IN=vNic_0 ' \
              'OUT= MAC=00:50:56:01:43:50:00:1f:6c:3d:d7:f7:08:00 ' \
              'SRC=10.11.254.108 DST=10.11.12.181 LEN=84 TOS=0x00 PREC=0x00 ' \
              'TTL=64 ID=54643 PROTO=ICMP TYPE=8 CODE=0 ID=65299 SEQ=10047 ' \
              'MARK=0x1'

        msg_s = parse_firewall_msg(msg)

        expected = {'code': '0', 'seq': '10047', 'proto': 'ICMP',
                    'tos': '0x00', 'ttl': '64', 'len': '84', 'mark': '0x1',
                    'src_ip': '10.11.254.108', 'source_port': -1,
                    'mac_address': '00:50:56:01:43:50:00:1f:6c:3d:d7:f7:08:00',
                    'action': 'drop', 'destination_port': -1, 'out': '',
                    'proc': '0x00', 'id': '65299', 'dest_ip': '10.11.12.181'}

        d1 = ast.literal_eval(str(expected))
        self.assertDictEqual(d1, msg_s)

    def test_parse_nat_msg(self):
        msg = \
            '[69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: DNAT_IN=vNic_0 OUT= ' \
            'MAC=00:50:56:01:35:27:00:a7:42:53:c5:c2:08:00 SRC=173.8.227.70 ' \
            'DST=209.143.151.73 LEN=52 TOS=0x00 PREC=0x00 TTL=122 ID=7082 DF ' \
            'PROTO=TCP SPT=54740 DPT=3389 WINDOW=8192 RES=0x00 SYN URGP=0 '

        msg_s = parse_nat_msg(msg)

        expected = {'dest_ip': '209.143.151.73',
                    'dnat_in': 'vNic_0',
                    'dpt': '3389',
                    'id': '7082',
                    'len': '52',
                    'mac_address': '00:50:56:01:35:27:00:a7:42:53:c5:c2:08:00',
                    'out': '',
                    'proc': '0x00',
                    'proto': 'TCP',
                    'res': '0x00',
                    'spt': '54740',
                    'src_ip': '173.8.227.70',
                    'tos': '0x00',
                    'ttl': '122',
                    'urgp': '0',
                    'window': '8192'}

        d1 = ast.literal_eval(str(expected))
        self.assertDictEqual(d1, msg_s)

    def test_date_str_to_ts(self):
        date_str = 'Jun 22 12:49:16'
        date_str_to_timestamp(date_str)
        # FIXME will break next year
        # expected_ts = '1498135756'
        # self.assertEqual(expected_ts, ts)


if __name__ == '__main__':
    sys.exit(unittest.main())
