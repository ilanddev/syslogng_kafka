===============================
syslog-ng Kafka driver
===============================

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

`syslogng_kafka` provides a Python module for syslog-ng >= 3.7 allowing one
to filter and forward syslog messages to multiple Kafka brokers on a given topic.

We are currently, 2016/06, not using `syslog-ng-mod-kafka` because of the
dependencies and state (testing) of this module hence the motivation to use a
simple Python component leveraging `syslog-ng-mod-python`.

=========================================
Ubuntu 16.04 syslog-ng 3.7.x installation
=========================================

Install Oracle JDK::

    $ sudo apt-get install python-software-properties software-properties-common
    $ sudo apt-add-repository ppa:webupd8team/java
    $ sudo apt-get update
    $ sudo apt-get install oracle-java8-set-default

Install syslog-ng 3.7.x::

    $ wget -qO -  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04/Release.key | sudo apt-key add -

    $ vim /etc/apt/sources.list.d/syslog-ng-obs.list

    >> deb  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04 ./

    $ apt-get update
    $ apt-get install syslog-ng-core syslog-ng-mod-python

Work around a Java bug::

    $ vim /etc/ld.so.conf.d/java.conf

    >>  /usr/lib/jvm/java-8-oracle/jre/lib/amd64/server/

    $ ldconfig -v | grep jvm

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

    $ netstat -tanpu|grep syslog
    tcp        0      0 0.0.0.0:514             0.0.0.0:*               LISTEN      11297/syslog-ng
    tcp        0      0 0.0.0.0:1000            0.0.0.0:*               LISTEN      11297/syslog-ng
    udp        0      0 0.0.0.0:514             0.0.0.0:*                           11297/syslog-ng

===============================
Ubuntu 16.04 Kafka installation
===============================

Install Oracle JDK::

    $ sudo apt-get install python-software-properties software-properties-common
    $ sudo apt-add-repository ppa:webupd8team/java
    $ sudo apt-get update
    $ sudo apt-get install oracle-java8-set-default

Prepare Kafka user::

    $ sudo useradd kafka -m
    $ sudo passwd kafka
    $ sudo adduser kafka sudo

Install Zookeeper::

    $ su - kafka
    $ sudo apt-get install zookeeperd

Test Zookeeper::

    $ telnet localhost 2181

At the Telnet prompt, type in ruok and press ENTER. You should see imok.

Download and install Kafka::

    $ mkdir -p ~/Downloads
    $ cd Downloads
    $ wget http://mirror.stjschools.org/public/apache/kafka/0.8.2.1/kafka_2.11-0.8.2.1.tgz

    $ mkdir -p ~/kafka && cd ~/kafka
    $ tar -xvzf ~/Downloads/kafka_2.11-0.8.2.1.tgz--strip 1

Start Kafka::

    $ nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server
    .properties > ~/kafka/kafka.log 2>&1 &

Check messages a given topic::

    $ ./bin/kafka-console-consumer.sh --from-beginning --zookeeper
    localhost:2181 --topic syslog

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
