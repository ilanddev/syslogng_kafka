=======
History
=======

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
