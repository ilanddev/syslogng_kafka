.. highlight:: shell

===========================
syslog-ng Kafka destination
===========================

Stable release
--------------

To install syslog-ng Kafka driver, run this command in your terminal:

.. code-block:: console

    $ pip install syslogng_kafka

This is the preferred method to install syslog-ng Kafka driver, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for syslog-ng Kafka driver can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/anguenot/syslogng_kafka

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/anguenot/syslogng_kafka/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .

.. _Github repo: https://github.com/anguenot/syslogng_kafka
.. _tarball: https://github.com/anguenot/syslogng_kafka/tarball/master

Configure
---------

First, let's make sure that your `syslog-ng`_ instance can accept messages.

Start by editing the main configuration file:

.. code-block:: console

    $ sudo vim /etc/syslog-ng/syslog-ng.conf 

.. _syslog-ng: https://syslog-ng.org/

Below is an example opening TCP and UDP port 514 on all interfaces::

    [...]
    source s_src { 
        system(); 
        internal(); 
        tcp(ip(0.0.0.0) port(514)); 
        udp(ip(0.0.0.0) port(514)); 
    };
    [...]

Configure the syslog-ng Apache Kafka destination:

.. code-block:: console

    $ vim /etc/syslog-ng/conf.d/kafka.conf

Sample driver configuration with every possible options. See below for documentation::

    destination syslog_to_kafka {
        python(
            class("syslogng_kafka.kafkadriver.KafkaDestination")
                on-error("fallback-to-string")
                options(
                    hosts("localhost:9092,localhost:9182")
                    topic("syslog")
                    partition("10")
                    msg_key("src_ip")
                    programs("firewall,nat")
                    broker_version("0.8.2.1")
                    verbose("True")
                    producer_config("{'client.id': 'sylog-ng'}")
                    )
                value-pairs(scope(rfc5424))
        );
    };
    log {
        source(s_src);
        destination(syslog_to_kafka);
    };

Restart the syslog-ng service:

.. code-block:: console

    $ service syslog-ng restart

To start the service in the foreground and see errors:

.. code-block:: console

    $ syslog-ng -F

Ensure your syslog-ng server is ready to get messages:

.. code-block:: console

    $ netstat -tanpu | grep syslog
    tcp        0      0 0.0.0.0:514             0.0.0.0:*               LISTEN      11297/syslog-ng
    udp        0      0 0.0.0.0:514             0.0.0.0:*                           11297/syslog-ng
