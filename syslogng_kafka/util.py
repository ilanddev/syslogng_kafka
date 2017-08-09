# -*- coding: utf-8 -*-

"""Util library for the kakfa driver.
"""

import datetime


def date_str_to_timestamp(date_str):
    """ Convert '%b %d %H:%M:%S' date string format to UNIX timestamp in local
    time assuming current year.

    :param date_str: string in '%b %d %H:%M:%S' format.
    :return: a string containing the UNIX timestamp
    """
    date = datetime.datetime.now()
    msg = datetime.datetime.strptime(date_str, '%b %d %H:%M:%S')
    date = date.replace(
        year=date.year, month=msg.month, day=msg.day,
        hour=msg.hour, minute=msg.minute, second=msg.second)
    return date.strftime("%s")


def parse_str_list(list_str):
    """ Parse a string containing comma separated values and return a list of
    strings.

    :param list_str: a string containing a comma separated list of strings
    :return: a list of string Python builtin object.
    """
    # remove all whitespace characters (space, tab, newline, etc.) and ignore
    # possible ending coma with filter.
    return list(filter(None, ''.join(list_str.split()).split(',')))


def parse_firewall_msg(msg):
    """ Parse a syslog message from the firewall program into a python
    dictionary.

    :param msg: firewall msg from syslog
    :return: a dictionary of firewall related key value pairs
    """

    words = msg.split(' ')
    action = 'allow'
    src = -1
    dest = -1
    proto = ''
    source_port = -1
    destination_port = -1
    mac = ''
    out = ''
    len_ = -1
    tos = -1
    proc = -1
    ttl = -1
    id_ = -1
    mark = -1
    seq = -1
    code = -1
    for w in words:
        if w.startswith('DROP'):
            action = 'drop'
        elif w.startswith('SRC='):
            src = w.split('=')[1]
        elif w.startswith('DST='):
            dest = w.split('=')[1]
        elif w.startswith('PROTO='):
            proto = w.split('=')[1]
        elif w.startswith('SPT='):
            source_port = w.split('=')[1]
        elif w.startswith('DPT='):
            destination_port = w.split('=')[1]
        elif w.startswith('MAC='):
            mac = w.split('=')[1]
        elif w.startswith('OUT='):
            out = w.split('=')[1]
        elif w.startswith('LEN='):
            len_ = w.split('=')[1]
        elif w.startswith('TOS='):
            tos = w.split('=')[1]
        elif w.startswith('PREC='):
            proc = w.split('=')[1]
        elif w.startswith('TTL='):
            ttl = w.split('=')[1]
        elif w.startswith('ID='):
            id_ = w.split('=')[1]
        elif w.startswith('MARK='):
            mark = w.split('=')[1]
        elif w.startswith('SEQ='):
            seq = w.split('=')[1]
        elif w.startswith('CODE='):
            code = w.split('=')[1]

    d = dict()
    d['action'] = action
    d['src_ip'] = src
    d['dest_ip'] = dest
    d['proto'] = proto
    d['source_port'] = source_port
    d['destination_port'] = destination_port
    d['mac_address'] = mac
    d['out'] = out
    d['len'] = len_
    d['tos'] = tos
    d['proc'] = proc
    d['ttl'] = ttl
    d['id'] = id_
    d['mark'] = mark
    d['seq'] = seq
    d['code'] = code
    return d


def parse_nat_msg(msg):
    """ Parse a syslog message from the nat program into a python
    dictionary.

    :param msg: nat msg from syslog
    :return: a dictionary of nat related key value pairs
    """

    dnat_in = ''
    out = ''
    mac = ''
    src = -1
    dest = -1
    len_ = -1
    tos = -1
    proc = -1
    ttl = -1
    id_ = -1
    proto = ''
    spt = -1
    dpt = -1
    window = -1
    res = ''
    urgp = -1

    words = msg.split(' ')
    for w in words:
        if w.startswith('DNAT_IN='):
            dnat_in = w.split('=')[1]
        elif w.startswith('OUT='):
            out = w.split('=')[1]
        elif w.startswith('MAC='):
            mac = w.split('=')[1]
        elif w.startswith('SRC='):
            src = w.split('=')[1]
        elif w.startswith('DST='):
            dest = w.split('=')[1]
        elif w.startswith('LEN='):
            len_ = w.split('=')[1]
        elif w.startswith('TOS='):
            tos = w.split('=')[1]
        elif w.startswith('PREC='):
            proc = w.split('=')[1]
        elif w.startswith('TTL='):
            ttl = w.split('=')[1]
        elif w.startswith('ID='):
            id_ = w.split('=')[1]
        elif w.startswith('PROTO='):
            proto = w.split('=')[1]
        elif w.startswith('SPT='):
            spt = w.split('=')[1]
        elif w.startswith('DPT='):
            dpt = w.split('=')[1]
        elif w.startswith('WINDOW='):
            window = w.split('=')[1]
        elif w.startswith('RES='):
            res = w.split('=')[1]
        elif w.startswith('URGP='):
            urgp = w.split('=')[1]

    d = dict()
    d['dnat_in'] = dnat_in
    d['out'] = out
    d['mac_address'] = mac
    d['src_ip'] = src
    d['dest_ip'] = dest
    d['len'] = len_
    d['tos'] = tos
    d['proc'] = proc
    d['ttl'] = ttl
    d['id'] = id_
    d['proto'] = proto
    d['spt'] = spt
    d['dpt'] = dpt
    d['window'] = window
    d['res'] = res
    d['urgp'] = urgp
    return d
