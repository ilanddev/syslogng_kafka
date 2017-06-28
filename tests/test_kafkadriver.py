#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_syslogng_kafka
----------------------------------

Tests for `syslogng_kafka` module.
"""

import sys
import unittest

from confluent_kafka import KafkaException
from mock import MagicMock

# noinspection PyUnresolvedReferences
import monkey  # NOQA
from syslogng_kafka.kafkadriver import DEFAULT_BROKER_VERSION_FALLBACK
from syslogng_kafka.kafkadriver import DEFAULT_FLUSH_AFTER
from syslogng_kafka.kafkadriver import DEFAULT_MAX_MSG_WAITING
from syslogng_kafka.kafkadriver import KafkaDestination
from syslogng_kafka.log import LOG


class TestKafkaDestination(unittest.TestCase):
    def test_init_missing_params(self):
        dest = KafkaDestination()
        conf = dict()
        self.assertFalse(dest.init(conf))

    def test_init_config_minimum(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK})

    def test_init_config_program(self):
        # single program to filter against
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'programs': 'firewall'}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, [conf['programs']])
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK})

        # multiple programs
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'programs': 'firewall,nat'}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, ['firewall', 'nat'])
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK})

        # multiple programs with space after coma.
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'programs': 'firewall, nat'}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, ['firewall', 'nat'])
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK})

    def test_init_group_config(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'group_id': 'my_group_id'}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, conf['group_id'])
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'group.id': conf['group_id']})

    def test_init_verbose_config(self):
        dest_msg = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'verbose': "True"}
        self.assertTrue(dest_msg.init(conf))
        self.assertEquals(dest_msg.hosts, conf['hosts'])
        self.assertEquals(dest_msg.topic, conf['topic'])
        self.assertEquals(dest_msg.programs, None)
        self.assertEquals(dest_msg.group_id, None)
        self.assertEquals(dest_msg.broker_version,
                          DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest_msg.verbose, True)
        self.assertEquals(dest_msg.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest_msg.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)

    def test_init_flush_after_config(self):
        dest_msg = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'flush_after': "10"}
        self.assertTrue(dest_msg.init(conf))
        self.assertEquals(dest_msg.hosts, conf['hosts'])
        self.assertEquals(dest_msg.topic, conf['topic'])
        self.assertEquals(dest_msg.programs, None)
        self.assertEquals(dest_msg.group_id, None)
        self.assertEquals(dest_msg.broker_version,
                          DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest_msg.verbose, False)
        self.assertEquals(dest_msg.flush_after, 10)
        self.assertEquals(dest_msg.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)

    def test_init_msg_waiting_max_config_01(self):
        dest_msg = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'msg_waiting_max': "100"}
        self.assertTrue(dest_msg.init(conf))
        self.assertEquals(dest_msg.hosts, conf['hosts'])
        self.assertEquals(dest_msg.topic, conf['topic'])
        self.assertEquals(dest_msg.programs, None)
        self.assertEquals(dest_msg.group_id, None)
        self.assertEquals(dest_msg.broker_version,
                          DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest_msg.verbose, False)
        self.assertEquals(dest_msg.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest_msg.msg_waiting_max, 100)

    def test_init_msg_waiting_max_config_02(self):
        dest_msg = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'msg_waiting_max': "0"}
        self.assertTrue(dest_msg.init(conf))
        self.assertEquals(dest_msg.hosts, conf['hosts'])
        self.assertEquals(dest_msg.topic, conf['topic'])
        self.assertEquals(dest_msg.programs, None)
        self.assertEquals(dest_msg.group_id, None)
        self.assertEquals(dest_msg.broker_version,
                          DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest_msg.verbose, False)
        self.assertEquals(dest_msg.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest_msg.msg_waiting_max, 0)

        self.assertTrue(dest_msg.init(conf))
        self.assertTrue(dest_msg.open())

        dest_msg._kafka_producer.flush = MagicMock(name='flush')
        dest_msg._kafka_producer.produce = MagicMock(name='produce')

        LOG.error = MagicMock(name='error')

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}
        dest_msg.send(msg)

        dest_msg._kafka_producer.produce.assert_not_called()
        dest_msg._kafka_producer.flush.assert_not_called()
        LOG.error.assert_called_once()

    def test_init_broker_version_config_2(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'broker_version': "0.8.2.1"}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, conf['broker_version'])
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)

        self.assertEquals(dest._conf['broker.version.fallback'],
                          conf['broker_version'])
        self.assertEquals(dest._conf['api.version.request'], False)

        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'broker_version': "0.9.2.1"}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, conf['broker_version'])
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.flush_after, DEFAULT_FLUSH_AFTER)

        self.assertEquals(dest._conf['broker.version.fallback'],
                          conf['broker_version'])
        self.assertEquals(dest._conf['api.version.request'], False)

    def test_init_broker_version_config_1(self):
        dest_10 = KafkaDestination()
        conf_10 = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                   'broker_version': "0.10.0.1"}
        self.assertTrue(dest_10.init(conf_10))
        self.assertEquals(dest_10.hosts, conf_10['hosts'])
        self.assertEquals(dest_10.topic, conf_10['topic'])
        self.assertEquals(dest_10.programs, None)
        self.assertEquals(dest_10.group_id, None)
        self.assertEquals(dest_10.broker_version, conf_10['broker_version'])
        self.assertEquals(dest_10.verbose, False)
        self.assertEquals(dest_10.flush_after, DEFAULT_FLUSH_AFTER)
        self.assertEquals(dest_10.msg_waiting_max, DEFAULT_MAX_MSG_WAITING)

        self.assertFalse('broker.version.fallback' in dest_10._conf.keys())
        self.assertEquals(dest_10._conf['api.version.request'], True)

    def test_open(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

    def test_isopened(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        dest.init(conf)
        dest.open()
        self.assertTrue(dest.is_opened())

    def test_init_open_deinit(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        dest.init(conf)
        dest.open()

        dest._kafka_producer.flush = MagicMock(name='flush')
        self.assertTrue(dest.deinit())
        dest._kafka_producer.flush.assert_called_once()

    def test_init_open_close(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())
        self.assertTrue(dest.close())

    def test_send_empty_message(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.flush.assert_not_called()
        dest._kafka_producer.produce.assert_not_called()

    def test_send_message(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_called_once()

        dest._kafka_producer.flush.assert_not_called()

    def test_send_filter_message(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic', 'programs': 'YYY'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_not_called()
        dest._kafka_producer.flush.assert_not_called()

    def test_send_filter_message_firewall(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'programs': 'firewall', 'verbose': "True"}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        f = '[69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: DROP_131073IN=vNic_0 ' \
            'OUT= MAC=00:50:56:01:43:50:00:1f:6c:3d:d7:f7:08:00 ' \
            'SRC=10.11.254.108 DST=10.11.12.181 LEN=84 TOS=0x00 PREC=0x00 ' \
            'TTL=64 ID=54643 PROTO=ICMP TYPE=8 CODE=0 ID=65299 SEQ=10047 ' \
            'MARK=0x1'

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'firewall',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70',
               'MESSAGE': f}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_called_once()

        dest._kafka_producer.flush.assert_not_called()

    def test_send_message_flush(self):
        log_dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'flush_after': "0"}
        self.assertTrue(log_dest.init(conf))
        self.assertTrue(log_dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        log_dest._kafka_producer.produce = MagicMock(name='produce')
        LOG.info = MagicMock(name='info')
        LOG.warning = MagicMock(name='warning')

        def flush(self):
            return 10
        log_dest._kafka_producer.flush = flush

        def __len__(self):
            return 10
        monkey.MockProducer.__len__ = __len__

        log_dest.send(msg)

        log_dest._kafka_producer.produce.assert_called_once()
        LOG.info.assert_called_once()
        LOG.warning.assert_called_once()

    def test_produce_fails_KafkaException(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer._acked = MagicMock(name='_acked')
        LOG.error = MagicMock(name='error')

        def produce(topic, msg, **kwargs):
            raise KafkaException("Fake exception.")

        dest._kafka_producer.produce = produce

        self.assertFalse(dest.send(msg))

        dest._kafka_producer.flush.assert_not_called()
        dest._kafka_producer._acked.assert_not_called()
        LOG.error.assert_called_once()

    def test_consumer_acked(self):

        class FakeMessage:

            def __init__(self, value):
                self._value = value

            def value(self):
                return self._value

        class FakeError:

            def __init__(self, msg):
                self._msg = msg

            def str(self):
                return self._msg

        dest = KafkaDestination()

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        dest._acked(None, None)
        LOG.error.assert_not_called()
        LOG.debug.assert_not_called()

        dest._acked(FakeError("XXX"), FakeMessage("XXX"))
        LOG.error.assert_called_once()
        LOG.debug.assert_not_called()

        dest._acked(None, FakeMessage("XXX"))
        LOG.error.assert_called_once()
        LOG.debug.assert_not_called()

        dest.verbose = True
        dest._acked(None, FakeMessage("XXX"))
        LOG.error.assert_called_once()
        LOG.debug.assert_called_once()


if __name__ == '__main__':
    sys.exit(unittest.main())
