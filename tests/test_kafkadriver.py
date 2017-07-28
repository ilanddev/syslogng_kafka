#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_syslogng_kafka
----------------------------------

Tests for `syslogng_kafka` module.
"""

import ast
import sys
import unittest

from confluent_kafka import KafkaException
from mock import MagicMock
from mock import ANY

# noinspection PyUnresolvedReferences
import monkey  # NOQA
import syslogng_kafka
from syslogng_kafka.kafkadriver import DEFAULT_BROKER_VERSION_FALLBACK
from syslogng_kafka.kafkadriver import KafkaDestination
from syslogng_kafka.kafkadriver import delivery_callback, stats_callback
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
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'delivery.report.only.error': True,
             'on_delivery': delivery_callback,
             'stats_cb': stats_callback
             })

    def test_z_producer_config(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'producer_config': "{'x': 'y'}"}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.producer_config,
                          ast.literal_eval(conf['producer_config']))
        # true only if a subset of dest_.conf
        self.assertTrue(
            ast.literal_eval(conf['producer_config']) <= dest._conf)
        self.assertTrue(
            {'api.version.request': False, 'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK}
            <= dest._conf)

    def test_zz_producer_config(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'producer_config': "{'x': 'y', 'a': 'b'}"}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertEquals(dest.producer_config,
                          ast.literal_eval(conf['producer_config']))
        # true only if a subset of dest_.conf
        self.assertTrue(
            ast.literal_eval(conf['producer_config']) <= dest._conf)
        self.assertTrue(
            {'api.version.request': False, 'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK}
            <= dest._conf)

    def test_zzz_producer_config(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'producer_config': "WRONG"}
        self.assertTrue(dest.init(conf))
        self.assertEquals(dest.hosts, conf['hosts'])
        self.assertEquals(dest.topic, conf['topic'])
        self.assertEquals(dest.programs, None)
        self.assertEquals(dest.group_id, None)
        self.assertEquals(dest.broker_version, DEFAULT_BROKER_VERSION_FALLBACK)
        self.assertEquals(dest.verbose, False)
        self.assertIsNone(dest.producer_config)

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
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'delivery.report.only.error': True,
             'on_delivery': delivery_callback,
             'stats_cb': stats_callback
             })

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
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'delivery.report.only.error': True,
             'on_delivery': delivery_callback,
             'stats_cb': stats_callback
             })

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
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'delivery.report.only.error': True,
             'on_delivery': delivery_callback,
             'stats_cb': stats_callback
             })

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
        self.assertEquals(
            dest._conf,
            {'api.version.request': False,
             'bootstrap.servers': conf['hosts'],
             'broker.version.fallback': DEFAULT_BROKER_VERSION_FALLBACK,
             'delivery.report.only.error': True,
             'group.id': conf['group_id'],
             'on_delivery': delivery_callback,
             'stats_cb': stats_callback
             })

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

    def test_init_open_close(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        dest.init(conf)
        dest.open()
        self.assertTrue(dest.close())

    def test_init_open_deinit(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())
        self.assertTrue(dest.deinit())

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

    def test_send_message_key(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic',
                'msg_key': 'src_ip'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_called_once_with(
            conf['topic'], ANY, key=u'10.11.12.53')

    def test_send_message_bad_key(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic', 'msg_key': 'nope'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_called_once_with(
            conf['topic'], ANY)

    def test_send_message_partition(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic', 'partition': '10'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.produce = MagicMock(name='produce')

        dest.send(msg)

        dest._kafka_producer.produce.assert_called_once_with(
            conf['topic'], ANY, partition=int(conf['partition']))

    def test_send_message_partition_bad(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic', 'partition': 'XXX'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53', 'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.produce = MagicMock(name='produce')
        LOG.warning = MagicMock(name='warning')

        dest.send(msg)

        LOG.warning.assert_called_once()
        dest._kafka_producer.produce.assert_called_once_with(conf['topic'], ANY)

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

    def test_produce_fails_kafka_exception(self):
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
        syslogng_kafka.delivery_callback = MagicMock(name='delivery_callback')
        LOG.error = MagicMock(name='error')

        def produce(topic, msg, **kwargs):
            raise KafkaException("Fake exception.")

        dest._kafka_producer.produce = produce

        # even if it fails
        self.assertTrue(dest.send(msg))

        dest._kafka_producer.flush.assert_not_called()
        syslogng_kafka.delivery_callback.assert_not_called()
        LOG.error.assert_called_once()

    def test_produce_fails_buffer_error(self):
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
            raise BufferError("Fake exception.")

        dest._kafka_producer.produce = produce

        # even if it fails
        self.assertTrue(dest.send(msg))

        dest._kafka_producer.flush.assert_not_called()
        dest._kafka_producer._acked.assert_not_called()
        LOG.error.assert_called_once()

    def test_produce_fails_unicodencodeerror(self):
        dest = KafkaDestination()
        conf = {'hosts': '192.168.0.1', 'topic': 'my_topic'}
        self.assertTrue(dest.init(conf))
        self.assertTrue(dest.open())

        msg = {'FACILITY': u'user', 'PRIORITY': u'notice',
               'HOST': u'10.11.12.102', 'PROGRAM': u'XXX',
               'DATE': 'Jun 22 12:49:16', 'ttl': u'128', 'len': u'209',
               'mark': u'0x1', 'src_ip': u'10.11.12.53',
               'source_port': u'138',
               'destination_port': u'138', 'out': u'', 'proc': u'0x00',
               'id': u'13254', 'dest_ip': u'209.143.151.70'}

        dest._kafka_producer.flush = MagicMock(name='flush')
        dest._kafka_producer._acked = MagicMock(name='_acked')
        LOG.error = MagicMock(name='error')

        def produce(topic, msg, **kwargs):
            raise UnicodeEncodeError("Fake exception.", u"x", 2, 3, "x")

        dest._kafka_producer.produce = produce

        # even if it fails
        self.assertTrue(dest.send(msg))

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

        delivery_callback(None, None)
        LOG.error.assert_not_called()
        LOG.debug.assert_not_called()

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        delivery_callback(FakeError("XXX"), FakeMessage("XXX"))
        LOG.error.assert_called_once()
        LOG.debug.assert_not_called()

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        delivery_callback(None, FakeMessage("XXX"))
        LOG.error.assert_not_called()
        LOG.debug.assert_called_once()

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        dest.verbose = True

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        delivery_callback(None, FakeMessage("XXX"))
        LOG.error.assert_not_called()
        LOG.debug.assert_called_once()

        LOG.error = MagicMock(name='error')
        LOG.debug = MagicMock(name='debug')

        delivery_callback(FakeError("XXX"), FakeMessage("XXX"))
        LOG.error.assert_called_once()
        LOG.debug.assert_not_called()


if __name__ == '__main__':
    sys.exit(unittest.main())
