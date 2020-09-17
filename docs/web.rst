Web interface
=============

.. _web-api:

Web API
-------

The web API allows other applications (notably `Kingfisher Collect <https://kingfisher-collect.readthedocs.io>`__) to submit data to this tool to store.

All requests must set an `HTTP Authorization request header <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization>`__ with an authentication type of ``ApiKey``. For example::

    Authorization: ApiKey <key>

To configure the API keys, see :doc:`../config`.

API endpoints are documented on `SwaggerHub <https://app.swaggerhub.com/apis-docs/jpmckinney/kingfisher-process/v1>`__.

.. _web-app:

Web app
-------

The web app allows you to view metadata about collections and files.

To run the app locally in **development** mode::

    FLASK_APP=ocdskingfisherprocess.web.app FLASK_ENV=development flask run

Then, open <http://127.0.0.1:5000/>

To use Kingfisher Process in a **production** environment with `Kingfisher Collect <https://kingfisher-collect.readthedocs.io/en/latest/kingfisher_process.html>`__, see `Flask's documentation <https://flask.palletsprojects.com/en/1.1.x/deploying/>`__ on deploying apps.
