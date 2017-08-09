# -*- coding: utf-8 -*-

"""A library that provides a syslog-ng Apache Kafka destination.
"""

from __future__ import print_function

import ast
import json
from time import time, sleep

from confluent_kafka import KafkaException
from confluent_kafka import Producer

from .log import LOG
from .util import date_str_to_timestamp
from .util import parse_firewall_msg
from .util import parse_nat_msg
from .util import parse_str_list

# this is the default broker version fallback defined by `librdkafka`
DEFAULT_BROKER_VERSION_FALLBACK = '0.9.0.1'


class KafkaDestination(object):
    """ syslog-ng Apache Kafka destination.
    """

    _kafka_producer = None

    _conf = dict()

    def __init__(self):
        self.hosts = None
        self.topic = None
        self.msg_key = None
        self.partition = None
        self.programs = None
        self.group_id = None
        self.broker_version = None
        self.verbose = False
        self.producer_config = None

    def init(self, args):
        """ This method is called at initialization time.

        Should return False if initialization fails.
        """

        if 'producer_config' in args:
            try:
                self.producer_config = ast.literal_eval(args['producer_config'])
                self._conf.update(self.producer_config)
            except ValueError:
                LOG.error("Given config %s is not in a Python dict format."
                          % args['producer_config'])

        try:
            self.hosts = args['hosts']
            self.topic = args['topic']
            self._conf['bootstrap.servers'] = self.hosts
        except KeyError:
            LOG.error("Missing `hosts` or `topic` option...")
            return False

        if 'msg_key' in args:
            self.msg_key = args['msg_key']
            LOG.info("Message key used will be %s" % self.msg_key)

        if 'partition' in args:
            self.partition = args['partition']
            LOG.info("Partition to produce to %s" % self.partition)

        # optional `programs` parameter to filter out messages
        if 'programs' in args:
            self.programs = parse_str_list(args['programs'])
            LOG.info("Programs to filter against %s" % self.programs)

        if 'group_id' in args:
            self.group_id = args['group_id']
            self._conf['group.id'] = self.group_id
            LOG.info("Broker group_id=%s" % self.group_id)

        if 'broker_version' in args:
            self.broker_version = args['broker_version']
            if '.'.join(self.broker_version.split('.')[:2]) in ('0.10', '0.11'):
                self._conf['api.version.request'] = True
            else:
                self._conf['broker.version.fallback'] = self.broker_version
                self._conf['api.version.request'] = False
            LOG.info("Broker version=%s" % self.broker_version)
        else:
            self.broker_version = DEFAULT_BROKER_VERSION_FALLBACK
            self._conf[
                'broker.version.fallback'] = DEFAULT_BROKER_VERSION_FALLBACK
            self._conf['api.version.request'] = False
            LOG.warn("Default broker version fallback %s "
                     "will be applied here." % DEFAULT_BROKER_VERSION_FALLBACK)

        self._conf['on_delivery'] = delivery_callback
        self._conf['stats_cb'] = stats_callback
        if 'verbose' in args:
            # provide a global `on_delivery` callback in the `Producer()` config
            # dict better for memory consumptions vs per message callback.
            self.verbose = ast.literal_eval(args['verbose'])
        if not self.verbose:
            # only interested in delivery failures here. We do provide a
            # global on_delivery callback in the Producer() config dict and
            # also set delivery.report.only.error.
            self._conf['delivery.report.only.error'] = True
            LOG.info("Verbose mode is OFF: you will not be able to see "
                     "messages in here. Failures only. Use 'verbose=('True')' "
                     "in your destination options to see successfully "
                     "processed messages in your logs.")

        LOG.info(
            "Initialization of Kafka Python driver w/ args=%s" % self._conf)
        return True

    def open(self):
        """ Open a connection to the Kafka service.

        Should return False if initialization fails.
        """
        LOG.info("Opening connection to the remote Kafka services at %s"
                 % self.hosts)
        self._kafka_producer = Producer(**self._conf)
        return True

    def is_opened(self):
        """ Check if the connection to Kafka is able to receive messages.

        Should return False if target is not open.
        """
        return self._kafka_producer is not None

    def close(self):
        """ Close the connection to the Kafka service.
        """
        LOG.debug("KafkaDestination.close()....")
        if self._kafka_producer is not None:
            LOG.debug("Flushing producer w/ a timeout of 30 seconds...")
            self._kafka_producer.flush(30)
        return True

    # noinspection PyMethodMayBeStatic
    def deinit(self):
        """ This method is called at deinitialization time.
        """
        LOG.debug("KafkaDestination.deinit()....")
        if self._kafka_producer:
            self._kafka_producer = None
        return True

    def send(self, ro_msg):
        """ Send a message to the target service

        It should return True to indicate success, False will suspend the
        destination for a period specified by the time-reopen() option.

        :return: True or False
        """

        # do nothing if msg is empty
        if not ro_msg:
            return True

        # no syslog-ng `values-pair` here we dealing with `LogMessage`
        if type(ro_msg) != dict:
            # syslog-ng `LogMessage` is read-only
            # goal is rfc5424 we cannot use values-pair because of memory leaks
            try:
                msg = {'FACILITY': ro_msg.FACILITY, 'PRIORITY': ro_msg.PRIORITY,
                       'HOST': ro_msg.HOST, 'PROGRAM': ro_msg.PROGRAM,
                       'DATE': ro_msg.DATE, 'MESSAGE': ro_msg.MESSAGE}
            except AttributeError:
                LOG.error("Your version of syslog-ng is not supported. "
                          "Please use syslog-ng 3.7.x")
                return False
        else:
            LOG.warn("You are using `values-pair` if you are using "
                     "syslog-ng <= 3.11 it is known to be leaking...")
            msg = ro_msg
        try:

            # check if we do have a program filter defined.
            msg_program = msg['PROGRAM']
            if self.programs is not None:
                if msg_program not in self.programs:
                    # notify of success
                    return True
            if msg_program == 'firewall':
                firewall_msg = msg['MESSAGE']
                msg['MESSAGE'] = parse_firewall_msg(firewall_msg)
            elif msg_program == 'nat':
                nat_msg = msg['MESSAGE']
                msg['MESSAGE'] = parse_nat_msg(nat_msg)
            # convert date string to UNIX timestamp
            msg_date = msg['DATE']
            if msg_date is not None:
                msg['DATE'] = date_str_to_timestamp(msg_date)

            msg_string = str(msg)

            kwargs = {}
            if self.msg_key and self.msg_key in msg.keys():
                kwargs['key'] = msg[self.msg_key]
            if self.partition:
                try:
                    kwargs['partition'] = int(self.partition)
                except ValueError:
                    LOG.warning(
                        "Ignore partition=%s because it is not an int."
                        % self.partition)

            self._kafka_producer.produce(self.topic, msg_string, **kwargs)

            # `poll()` doesn't do any sleeping at all if you give it 0, all
            # it does is grab a mutex, check a queue, and release the mutex.
            # It is okay to call poll(0) after each produce call, the
            # performance impact is negligible, if any.
            self._kafka_producer.poll(0)
        except BufferError:
            LOG.error("Producer queue is full. This message will be discarded. "
                      "%d messages waiting to be delivered.",
                      len(self._kafka_producer))
            # do not return False here as the destination would be closed
            # and we would have to restart syslog-ng
            sleep(5)
            return True
        except (KafkaException, UnicodeEncodeError) as e:
            LOG.error("An error occurred while trying to send messages...   "
                      "See details: %s" % e, exc_info=True)
            sleep(5)
            # do not return False here as the destination would be closed
            # and we would have to restart syslog-ng
            return True

        return True


def delivery_callback(err, msg):
    if err is not None:
        try:
            LOG.error("Failed to deliver message: {0}: {1}"
                      .format(msg.value(), err.str()))
        except UnicodeDecodeError:
            LOG.error("Failed to deliver message: {0}: {1}"
                      .format(msg.value(), repr(err)))
    elif msg is not None:
        LOG.debug("Message produced: {0}".format(msg.value()))


def stats_callback(json_str):
    producer_metrics = json.loads(json_str)
    print("#" * 80)
    print("Time: %d" % time())
    print("Message count: %s" % producer_metrics['msg_cnt'])
    for broker in producer_metrics['brokers']:
        print(producer_metrics['brokers'][broker]['throttle'])
    print("#" * 80)
