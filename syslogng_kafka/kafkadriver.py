# -*- coding: utf-8 -*-

"""A library that provides a syslog-ng Kafka destination.

Inspired from the syslog-ng documentation.

https://syslog-ng.gitbooks.io/getting-started/content/chapters/chapter_5/section_3.html
"""

from __future__ import print_function

import time

from kafka.common import LeaderNotAvailableError
from kafka.producer import KafkaProducer


class LogDestination(object):
    """Inspired from syslog-ng 3.5 documentation.
    """

    def open(self):
        """Open a connection to the target service"""
        return True

    def close(self):
        """Close the connection to the target service"""
        pass

    def is_opened(self):
        """Check if the connection to the target is able to receive messages"""
        return True

    def init(self, args):
        """This method is called at initialization time"""
        return True

    def deinit(self):
        """This method is called at deinitialization time"""
        pass

    def send(self, msg):
        """Send a message to the target service
        It should return True to indicate success, False will suspend the
        destination for a period specified by the time-reopen() option."""
        pass


class KafkaDestination(LogDestination):
    def __init__(self):
        self.hosts = None
        self.kafka_producer = None
        self.topic = None
        self.is_available = None

    def init(self, args):
        print("Initialization of Kafka Python driver w/ args=%s" % args)
        try:
            self.hosts = args['hosts']
            self.topic = args['topic']
        except KeyError:
            print("Missing `hosts` or `topic` option...")
            return False
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.hosts)
        return True

    def open(self):
        return True

    def close(self):
        self.kafka_producer.close()
        return True

    def deinit(self):
        return True

    def send(self, msg):
        msg_string = str(msg)
        try:
            print(msg.values())
            print(self.kafka_producer.send(self.topic, msg_string))
        except LeaderNotAvailableError:
            try:
                time.sleep(1)
                print(self.kafka_producer.send(self.topic, msg_string))
            except:
                return False
        return True
