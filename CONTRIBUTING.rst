Contributing
============

Report bugs, issues, and other problems
---------------------------------------

Report bugs through the `issue tracker <https://github.com/markpbaggett/pyrepox/issues>`_.

**NOTE**: some bugs are acknowledged in the `TODO list <https://pyrepox.readthedocs.io/en/latest/todo.html>`_.

Contributing Code
-----------------

* Fork the repo.
* Clone locally.
* Create a branch for your feature / issue.

.. code-block:: console

   $ git checkout -b name_of_bug_or_feature


* After you're done, run flake8 and black versus your changes and make sure you pass unittests:

.. code-block:: console

   $ flake8 file_changed.py
   $ black file_changed.py
   $ python -m unittest --verbose


* Add, commit, and push your branch to your fork.

.. code-block:: console

   $ git add file_changed.py
   $ git commit -m "Talk about your change."
   $ git push origin master

* Open pull request.

Tests
-----

Unit tests are appreciated.  Instead of relying on a Repox instance, use mocks instead.