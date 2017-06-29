.. highlight:: shell

=======================
librdkafka installation
=======================

`syslogng_kafka`_ depends on the `confluent-kafka`_ lib:

`confluent-kafka`_ requires `librdkafka`_ >= 0.9.1 which is currently not
installed with mainstream Linux distribution.

librdkafka is a C library implementation of the Apache `Kafka`_ protocol,
containing both Producer and Consumer support. It was designed with message
delivery reliability and high performance in mind, current figures exceed
1 million msgs/second for the producer and 3 million msgs/second for the
consumer.

.. _syslogng_kafka: https://github.com/ilanddev/syslogng_kafka
.. _confluent-kafka: https://github.com/confluentinc/confluent-kafka-python
.. _librdkafka: https://github.com/edenhill/librdkafka
.. _Kafka: http://kafka.apache.org/

DEB packages via apt
--------------------

`Confluent`_ maintains apt repositories that provide packages for Debian-based
Linux distributions such as Debian and Ubuntu and the installation is documented
`here`_

First install Confluent’s public key, which is used to sign the packages in
the apt repository:

Below are extracts from that page if you are in a hurry:

.. code-block:: console

    $ wget -qO - http://packages.confluent.io/deb/3.2/archive.key | sudo apt-key add -

Add the repository to your /etc/apt/sources.list:

.. code-block:: console

    $ sudo add-apt-repository "deb [arch=amd64] http://packages.confluent.io/deb/3.2 stable main"

Pin down the version of `librdkafka`_ to 0.9.x

.. code-block:: console

    $ sudo vim /etc/apt/preferences.d/confluent-librdkafka

Then add the content below::

  Package: librdkafka1
  Pin: origin "packages.confluent.io"
  Pin: version 0.9.*
  Pin-Priority: 550

  Package: librdkafka-dev
  Pin: origin "packages.confluent.io"
  Pin: version 0.9.*
  Pin-Priority: 550

  Package: librdkafka++1
  Pin: origin "packages.confluent.io"
  Pin: version 0.9.*
  Pin-Priority: 550

Then update and install:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install librdkafka1 librdkafka-dev

Note, we need to install the `-dev` package so that `pip`_ can compile `confluent-kafka`_

.. _Confluent: https://www.confluent.io/
.. _here: http://docs.confluent.io/current/installation.html#deb-packages-via-apt
.. _pip: https://pip.pypa.io

From source
-----------

Alternatively, you can install `librdkafka`_ from source using the script
included in this repository:

.. code-block:: console

    $ sudo bash tools/bootstrap-librdkafka.sh ${LIBRDKAFKA_VERSION} /usr/local
    $ sudo ldconfig -vvv

This actual script is used by the `Travis CI integration tests`_

.. _Travis CI integration tests: https://travis-ci.org/ilanddev/syslogng_kafka


