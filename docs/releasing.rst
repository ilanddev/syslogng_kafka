.. highlight:: shell

=========
Releasing
=========

We using `bumpversion`_ to manage the releases.

Install bumpversion using pip:

.. code-block:: console

    $ pip install bumpversion

Run a dry run to make sure all is looking good:

.. code-block:: console

    $ bumpversion --dry-run --verbose $CURRENT_VERSION --new-version=$NEW_VERSION

Perform the actual release:

.. code-block:: console

    $ bumpversion $CURRENT_VERSION --new-version=$NEW_VERSION

Push the changes and actual tag:

.. code-block:: console

    $ git push

    $ git push --tags origin

Then publish the archive on `PyPI`_:

.. code-block:: console

    $ make release

Note, it requires valid server login in `~/.pypirc`

.. _bumpversion: https://github.com/peritus/bumpversion
.. _PyPI: https://pypi.python.org/pypi

