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
