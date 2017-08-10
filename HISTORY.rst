=======
History
=======

0.1.10 (2017-08-09)
-------------------

* `nat` program pre-processing

0.1.9 (2017-07-28)
------------------

* Handle `LogMessage` vs syslog-ng `values-pair` because it badly leaks if one do...
* Make 3.7.x the supported version for now because of `LogMessage` issues.

0.1.8 (2017-07-28)
------------------

* Delivery and stats callback refactoring.

0.1.7 (2017-07-27)
------------------

* Update confluent-kafka dependency to version 0.11.0: https://github.com/confluentinc/confluent-kafka-python/releases/tag/v0.11.0

0.1.6 (2017-07-04)
------------------

* Disable `delivery.report.ony.error` on callbacks because of a bug in
`confluent-kafka`: https://github.com/confluentinc/confluent-kafka-python/issues/84
Let's revisit when 0.11 is released.

0.1.5 (2017-07-03)
------------------

* provide a global `on_delivery` callback in the `Producer()` config
dict better for memory consumptions vs per message callback.

0.1.4 (2017-06-30)
------------------

* make `send` more robust

0.1.3 (2017-06-30)
------------------

* catch `UnicodeEncodeError` in `send()`

0.1.2 (2017-06-29)
------------------

* catch `UnicodeDecodeError` in delivery callback as it can be thrown by
  `err.str()`

0.1.1 (2017-06-29)
------------------

* add util to produce syslog messages in `tools` sub-folder
* remove useless `KeyboardInterrupt`
* reduce timeout of `flush()` from 30 to 5 seconds
* more tests

0.1.0 (2017-06-28)
------------------

* First release on PyPI.
