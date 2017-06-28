# -*- coding: utf-8 -*-

"""A library that provides a syslog-ng Apache Kafka destination.
"""

import ast
from time import sleep

from confluent_kafka import Producer
from confluent_kafka import KafkaException

from .log import LOG
from .util import date_str_to_timestamp
from .util import parse_firewall_msg
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
        LOG.info(
            "Initialization of Kafka Python driver w/ args=%s" % args)

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
            self.verbose = ast.literal_eval(args['verbose'])
        if not self.verbose:
            LOG.info("Verbose mode is OFF: you will not be able to see "
                     "messages in here. Use 'verbose=('True')' in your "
                     "destination options.")

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
            LOG.debug("Flushing producer with a timeout of 30 seconds....")
            self._kafka_producer.flush(30)
            self._kafka_producer = None
        return True

    def deinit(self):
        """ This method is called at deinitialization time.
        """
        LOG.debug("KafkaDestination.deinit()....")
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
            kwargs = {'callback': self._acked}
            if self.msg_key:
                if msg.get(self.msg_key):
                    kwargs['key'] = msg.get(self.msg_key)
            if self.partition:
                try:
                    kwargs['partition'] = int(self.partition)
                except ValueError:
                    LOG.warning(
                        "Ignore partition=%s because it is not an int."
                        % self.partition)
            self._kafka_producer.produce(self.topic, msg_string, **kwargs)
        except BufferError:
            LOG.error("Producer queue is full. This message will be discarded. "
                      "%d messages waiting to be delivered.",
                      len(self._kafka_producer))
            try:
                sleep(5)
            except KeyboardInterrupt:
                return False
            return True
        except KafkaException as e:
            LOG.error("An error occurred while trying to send messages..."
                      "See details: %s" % e, exc_info=True)
            # do not return False here as the destination would be closed
            # and we would have to restart syslog-ng
            try:
                sleep(5)
            except KeyboardInterrupt:
                return False
            return True
        finally:
            self._kafka_producer.poll(0)

        return True

    def _acked(self, err, msg):
        if err is not None:
            LOG.error("Failed to deliver message: {0}: {1}"
                      .format(msg.value(), err.str()))
        else:
            if self.verbose:
                LOG.debug("Message produced: {0}".format(msg.value()))
