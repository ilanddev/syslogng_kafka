# -*- coding: utf-8 -*-

"""A library that provides a syslog-ng Apache Kafka destination.
"""

from confluent_kafka import Producer

from .log import LOG
from .util import date_str_to_timestamp
from .util import parse_firewall_msg
from .util import parse_str_list

# this is the default broker version fallback defined by `librdkafka`
DEFAULT_BROKER_VERSION_FALLBACK = '0.9.0.1'

DEFAULT_FLUSH_AFTER = 10000

DEFAULT_MAX_MSG_WAITING = 1000000


class KafkaDestination(object):
    """ syslog-ng Apache Kafka destination.
    """

    _kafka_producer = None

    _conf = dict()

    def __init__(self):
        self.hosts = None
        self.topic = None
        self.programs = None
        self.group_id = None
        self.broker_version = None
        self.verbose = False
        self.flush_after = None
        self.msg_waiting_max = None

    def init(self, args):
        """ This method is called at initialization time.

        Should return False if initialization fails.
        """
        LOG.info(
            "Initialization of Kafka Python driver w/ args=%s" % args)
        try:
            self.hosts = args['hosts']
            self.topic = args['topic']
            self._conf['bootstrap.servers'] = self.hosts
        except KeyError:
            LOG.error("Missing `hosts` or `topic` option...")
            return False

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
            if '.'.join(self.broker_version.split('.')[:2]) == '0.10':
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
        if 'verbose' in args:
            self.verbose = bool(args['verbose'])
        if 'flush_after' in args:
            self.flush_after = int(args['flush_after'])
        else:
            self.flush_after = DEFAULT_FLUSH_AFTER
        LOG.info("Flush will occur if %d messages are waiting to be "
                 "delivered" % self.flush_after)

        if 'msg_waiting_max' in args:
            self.msg_waiting_max = int(args['msg_waiting_max'])
        else:
            self.msg_waiting_max = DEFAULT_MAX_MSG_WAITING
        LOG.info("Maximum number of messages and Kafka protocol requests "
                 "that can be waiting to be delivered to broker: %d"
                 % self.msg_waiting_max)

        return True

    def open(self):
        """ Open a connection to the Kafka service.

        Should return False if initialization fails.
        """
        LOG.info("Opening connection to the remote Kafka services.")
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
        # no `close()` method on Consumer API
        if self._kafka_producer is not None:
            self._kafka_producer = None
        return True

    def deinit(self):
        """ This method is called at deinitialization time.
        """
        LOG.debug("KafkaDestination.deinit()....")
        if self._kafka_producer is not None:
            self._kafka_producer.flush(30)
        return True

    def send(self, msg):
        """ Send a message to the target service

        It should return True to indicate success, False will suspend the
        destination for a period specified by the time-reopen() option.

        :return: True or False
        """

        # do nothing if msg is empty
        if not msg:
            return True

        # check if we do have a program filter defined.
        msg_program = msg.get('PROGRAM')
        if self.programs is not None:
            if msg_program not in self.programs:
                # notify of success
                return True
        if msg_program == 'firewall':
            firewall_msg = msg.get('MESSAGE')
            msg['MESSAGE'] = parse_firewall_msg(firewall_msg)
        # convert date string to UNIX timestamp
        msg_date = msg.get('DATE')
        if msg_date is not None:
            msg['DATE'] = date_str_to_timestamp(msg_date)

        msg_string = str(msg)

        try:
            if len(self._kafka_producer) >= self.msg_waiting_max:
                LOG.error(
                    "Maximum number of messages of %s and Kafka protocol "
                    "requests waiting to be delivered to broker reached. "
                    "Message will be dropped."
                    % DEFAULT_MAX_MSG_WAITING)
            else:
                self._kafka_producer.produce(
                    self.topic, msg_string, callback=self._acked)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return False
        finally:
            queued = len(self._kafka_producer)
            if queued >= self.flush_after:
                LOG.info(
                    "Flushing message per configuration. "
                    "After=%d messages." % self.flush_after)
                queued_after = self._kafka_producer.flush(10)
                if queued_after == queued:
                    LOG.warning("We having issues flushing the producer. "
                                "Is Kafka available?")
        return True

    def _acked(self, err, msg):
        if err is not None:
            LOG.error("Failed to deliver message: {0}: {1}"
                      .format(msg.value(), err.str()))
        else:
            if self.verbose:
                LOG.debug("Message produced: {0}".format(msg.value()))
