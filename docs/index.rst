.. Pyrepox documentation master file, created by
   sphinx-quickstart on Wed Dec 26 17:24:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pyrepox: Repox for Humans
===================================
.. image:: https://travis-ci.org/markpbaggett/pyrepox.png
.. image:: https://readthedocs.org/projects/pyrepox/badge/?version=latest

Pyrepox is a lightweight `Repox <https://github.com/europeana/REPOX>`_
client written in Python. It is designed to make reading, writing,
updating, and deleting content in your Repox instance as convenient as
possible.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

-----------------------------

**Example**::

   >>> from repox.repox import Repox
   >>> r = Repox("http://localhost:8080", "username", "password")
   >>> r.list_all_aggregators()
   ['dltn']
   >>> r.list_all_aggregators(verbose=True)
   [{'id': 'dltn', 'name': 'Digital Library of Tennessee', 'nameCode': 'dltn',
   'homepage': 'http://localhost:8080/repox'}]
   >>> r.get_list_of_providers("dltn")
   ['utk', 'utc', 'cmhf', 'knox', 'mtsu', 'crossroads', 'tsla', 'nash', 'memphis']

The API Documentation / Guide
-----------------------------

If you are looking for information about a specific method, its parameters, or its return value, this part is for you.

.. toctree::
   :maxdepth: 2

   source/repox

Release History
---------------

See history of changes here:

.. toctree::
   :maxdepth: 2

   history.rst

TODO List
---------

See TODO list here:

.. toctree::
   :maxdepth: 2

   todo.rst

Contributing
------------

How to contribute:

.. include:: ../CONTRIBUTING.rst

Search / Index
--------------

Can't find what you're looking for? Try here.

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
