#!/usr/bin/env python2.7

"""Script injecting UDP messages to a remote syslog server
"""

from __future__ import print_function

import socket
import sys
import threading
import time
from random import randint

NEVER_ENDING = True
SYSLOG_SERVER = 'localhost'
SYSLOG_SERVER_PORT = 514
NB_THREADS = 1
NB_MESSAGES = 100

""" Starts worker threads.

Each thread will publish a certain amount of messages.
"""


def start_threads(amount=1):
    for i in range(amount):
        thread = threading.Thread(target=inject)
        thread.daemon = True
        thread.start()


def inject():

    message = """firewall[]: [69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: 
    DROP_131073IN=vNic_0 OUT= MAC=00:50:56:01:43:50:00:1f:6c:3d:d7:f7:08:00 
    SRC=10.11.254.108 DST=10.11.12.181 LEN=84 TOS=0x00 PREC=0x00 TTL=64 
    ID=54643 PROTO=ICMP TYPE=8 CODE=0 ID=65299 SEQ=10047 MARK=0x1 """

    message2 = """firewall[]: [69e9c2b7-ee9f-4a3e-80f0-8ffc66aac147]: 
    DROP_131073IN=vNic_0 OUT= MAC=ff:ff:ff:ff:ff:ff:00:50:56:bd:70:59:08:00 
    SRC=10.11.12.53 DST=10.11.12.181 LEN=229 TOS=0x00 PREC=0x00 
    TTL=128 ID=13254 PROTO=UDP SPT=138 DPT=138 LEN=209 MARK=0x1 """

    i = 0
    while True:
        event_id = randint(1, 1000000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if i % 2 == 0:
            sock.sendto(message, (SYSLOG_SERVER, SYSLOG_SERVER_PORT))
        else:
            sock.sendto(message2, (SYSLOG_SERVER, SYSLOG_SERVER_PORT))
        print("Sending event #%s with id=%s" % (i, event_id))
        if i >= NB_MESSAGES and not NEVER_ENDING:
            break
        i += 1

if __name__ == '__main__':
    start_threads(NB_THREADS)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(1)
