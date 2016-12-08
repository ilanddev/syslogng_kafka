#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    ['kafka-python==1.3.1']
]

test_requirements = ['bumpversion==0.5.3',
                     'wheel>=0.29.0',
                     'watchdog==0.8.3',
                     'flake8==3.2.1',
                     'tox==2.5.0',
                     'coverage==4.2',
                     'Sphinx==1.5',
                     'cryptography==1.6'
                    ],

setup(
    name='syslogng_kafka',
    version='0.1.0',
    description="syslog-ng mod-python Kafka driver",
    long_description=readme + '\n\n' + history,
    author="Julien Anguenot",
    author_email='julien@anguenot.org',
    url='https://github.com/ilanddev/syslogng_kafka',
    packages=[
        'syslogng_kafka',
    ],
    package_dir={'syslogng_kafka':
                 'syslogng_kafka'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='syslogng kafka',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
