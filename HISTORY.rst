=======
History
=======

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
