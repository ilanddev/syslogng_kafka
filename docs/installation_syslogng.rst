.. highlight:: shell

======================
syslog-ng installation
======================

You will need `syslog-ng`_ >= 3.7.x

If your favorite Linux distribution does not provide a recent enough version read `this`_

In a nutshell, below is an example for Ubuntu / Debian

Add the repo keys:

.. code-block:: console

    $ wget -qO -  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04/Release.key | sudo apt-key add -

Add the repo sources:

.. code-block:: console

    $ vim /etc/apt/sources.list.d/syslog-ng-obs.list

::

    deb  http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_16.04 ./

Pin down version:

.. code-block:: console

    $ vim /etc/apt/preferences.d/syslog-ng

::

        Package: syslog-ng-core
        Pin: origin "download.opensuse.org"
        Pin: version 3.7.*
        Pin-Priority: 550

        Package: syslog-ng-mod-python
        Pin: origin "download.opensuse.org"
        Pin: version 3.7.*
        Pin-Priority: 550

Finally update and install:

.. code-block:: console

    $ apt-get update
    $ apt-get install syslog-ng-core syslog-ng-mod-python

Note, syslog-ng-mod-python has been introduced in syslog-ng 3.7.x

.. _syslog-ng: https://syslog-ng.org/
.. _this: https://www.balabit.com/blog/installing-the-latest-syslog-ng-on-ubuntu-and-other-deb-distributions/
