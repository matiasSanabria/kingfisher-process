Configuration
=============

Setup
-----

Create the tool's configuration directory::

    mkdir ~/.config/ocdskingfisher-process

Download the sample main configuration file::

    curl https://raw.githubusercontent.com/open-contracting/kingfisher-process/master/samples/config.ini -o ~/.config/ocdskingfisher-process/config.ini

Open the main configuration file at ``~/.config/ocdskingfisher-process/config.ini``, and follow the instructions below to update it.

PostgreSQL
----------

.. note::

   This step is required. All other steps are optional.

Configure the database connection settings:

.. code-block:: ini

   [DBHOST]
   HOSTNAME = localhost
   PORT = 5432
   USERNAME = ocdskingfisher
   PASSWORD = 
   DBNAME = ocdskingfisher

If you prefer not to store the password in ``config.ini``, you can use the `PostgreSQL Password File <https://www.postgresql.org/docs/11/libpq-pgpass.html>`__, ``~/.pgpass``, which overrides any password in ``config.ini``. Otherwise, if you used the same settings as in the examples during :doc:`requirements-install`, you only need to set ``PASSWORD`` above.

To override ``config.ini`` and/or ``.pgpass``, set the ``KINGFISHER_PROCESS_DB_URI`` environment variable. This is useful to temporarily use a different database than your default database. For example, in a bash-like shell::

    export KINGFISHER_PROCESS_DB_URI='postgresql://user:password@localhost:5432/dbname'

.. _config-logging:

Logging
-------

This tool uses the `Python logging module <https://docs.python.org/3/library/logging.html>`__. Loggers are in the ``ocdskingfisher`` namespace.

Logging from the :doc:`cli/index` can be configured with a ``~/.config/ocdskingfisher-process/logging.json`` file. To download the default configuration::

    curl https://raw.githubusercontent.com/open-contracting/kingfisher-process/master/samples/logging.json -o ~/.config/ocdskingfisher-process/logging.json

To download a different configuration that includes debug messages::

    curl https://raw.githubusercontent.com/open-contracting/kingfisher-process/master/samples/logging-debug.json -o ~/.config/ocdskingfisher-process/logging.json

Web API
-------

To allow access to the :ref:`web API <web-api>`, set API keys, separated by commas. For example, to set ``1234`` and ``5678`` as keys (in practice, you should use `long, random keys <https://www.avast.com/en-us/random-password-generator>`__):

.. code-block:: ini

    [WEB]
    API_KEYS = 1234,5678

To override ``config.ini``, set the ``KINGFISHER_PROCESS_WEB_API_KEYS`` environment variable.

Collection flags
----------------

When a :ref:`new collection <collections>` is created, :ref:`flags <schema-check-flags>` are set to indicate what operations to perform on them.

All flags are off by default. To turn any on:

.. code-block:: ini

    [COLLECTION_DEFAULT]
    CHECK_DATA = true
    CHECK_OLDER_DATA_WITH_SCHEMA_1_1 = false

Default pre-processing pipeline
-------------------------------

To enable the :doc:`standard-pipeline`:

.. code-block:: ini

    [STANDARD_PIPELINE]
    RUN = true

Redis
-----

Configure the Redis connection settings:

.. code-block:: ini

    [REDIS]
    HOST = localhost
    PORT = 6379
    DATABASE = 0

Sentry
------

To track crashes, `sign up <https://sentry.io/signup/>`__ for `Sentry <https://sentry.io/>`__, and set the DSN:

.. code-block:: ini

    [SENTRY]
    DSN = https://<key>@sentry.io/<project>

.. note::

    Sentry has its own `environment variables <https://docs.sentry.io/error-reporting/configuration/?platform=python>`__. Further reading: `Sentry for Python <https://sentry.io/for/python/>`__.
