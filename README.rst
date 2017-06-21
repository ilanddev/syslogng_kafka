======================
syslog-ng Kafka driver
======================

.. image:: https://img.shields.io/pypi/v/syslogng_kafka.svg
    :target: https://pypi.python.org/pypi/syslogng_kafka

.. image:: https://travis-ci.org/ilanddev/syslogng_kafka.svg?branch=master
    :target: https://travis-ci.org/ilanddev/syslogng_kafka

.. image:: https://readthedocs.org/projects/syslogng_kafka/badge/?version=latest
    :target: https://syslogng_kafka.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: https://requires.io/github/ilanddev/syslogng_kafka/requirements.svg?branch=master
    :target: https://requires.io/github/ilanddev/syslogng_kafka/requirements/?branch=master
    :alt: Requirements Status


syslog-ng mod-python Kafka driver

* Free software: Apache Software License 2.0
* Documentation: https://syslogng-kafka.readthedocs.io.

============
Introduction
============

`syslogng_kafka` provides a Python module for syslog-ng == 3.7 allowing one
to filter and forward syslog messages to multiple Kafka brokers on a given topic.

We are currently, 2016/06, not using `syslog-ng-mod-kafka` because of the
dependencies and state (testing) of this module hence the motivation to use a
simple Python component leveraging `syslog-ng-mod-python`.

=========================================
Ubuntu 16.04 syslog-ng 3.7.x installation
=========================================

Install syslog-ng 3.7.x::

    $ wget -qO -  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04/Release.key | sudo apt-key add -

    $ vim /etc/apt/sources.list.d/syslog-ng-obs.list

    >> deb  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04 ./

    $ vim /etc/apt/preferences.d/syslog-ng

        Package: syslog-ng-core
        Pin: origin "download.opensuse.org"
        Pin: version 3.7.*
        Pin-Priority: 550

        Package: syslog-ng-mod-python
        Pin: origin "download.opensuse.org"
        Pin: version 3.7.*
        Pin-Priority: 550

    $ apt-get update
    $ apt-get install syslog-ng-core syslog-ng-mod-python

Install syslog-ng kafka driver::

At the command line::

    $ pip install syslogng_kafka

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv syslogng_kafka
    $ pip install syslogng_kafka

You can also install syslogng_kafka using the actual source checkout::

    $ git clone https://github.com/ilanddev/syslogng_kafka.git
    $ cd syslogng_kafka
    $ pip install -e .

Configure syslog-ng daemon::

    $ sudo vim /etc/syslog-ng/syslog-ng.conf 

Replace the source directive with something like this::

    source s_src { 
        system(); 
        internal(); 
        tcp(ip(0.0.0.0) port(1000)); 
        tcp(ip(0.0.0.0) port(514)); 
        udp(ip(0.0.0.0) port(514)); 
    };

Configure the syslog-ng Python driver::

    $ vim /etc/syslog-ng/conf.d/kafka.conf

Sample driver configuration using the optional `programs` to filter out
before forwarding to Kafka::

    destination syslog_to_kafka {
        python(
            class("syslogng_kafka.kafkadriver.KafkaDestination")
                on-error("fallback-to-string")
                    options(
                        hosts("localhost:9092,localhost:9182")
                        topic("syslog")
                        programs("firewall,nat")
                    )
                    value-pairs(scope(rfc5424))
        );
    };

    log {
        source(s_src);
        destination(syslog_to_kafka);
    };

Restart the syslog-ng service::

    $ service syslog-ng restart

To start the service in the foreground and see errors::

    $ syslog-ng -F

Ensure your syslog-ng server is ready to get messages::

    $ netstat -tanpu | grep syslog
    tcp        0      0 0.0.0.0:514             0.0.0.0:*               LISTEN      11297/syslog-ng
    tcp        0      0 0.0.0.0:1000            0.0.0.0:*               LISTEN      11297/syslog-ng
    udp        0      0 0.0.0.0:514             0.0.0.0:*                           11297/syslog-ng

