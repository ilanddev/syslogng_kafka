#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('requirements_dev.txt') as requirements_dev_file:
    test_requirements = requirements_dev_file.read().splitlines()

setup(
    name='syslogng_kafka',
    version='0.1.10',
    description="syslog-ng mod-python Kafka driver",
    long_description=readme + '\n\n' + history,
    author="Julien Anguenot",
    author_email='julien@anguenot.org',
    url='https://github.com/ilanddev/syslogng_kafka',
    packages=[
        'syslogng_kafka',
    ],
    package_dir={'syslogng_kafka': 'syslogng_kafka'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='syslogng kafka',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
