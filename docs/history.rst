Release History / Change Log
============================

0.0.3 (April 16, 2019)
----------------------

**Improvements**

* Added schedule_harvest() method.
* Added schedule_weekly_harvest() method.
* Added get_recently_ingested_sets_by_aggregator() method.
* Added get_list_of_scheduled_harvests_by_provider() method.

**Trivial and Dev Things**

* Switch to letting Sphinx automatically handle todos.
* Properly format XML output in docstrings.
* Switch type of return for count_records_in_set() to int.


0.0.2 (January 1, 2019)
-----------------------

**Improvements**

* Added get_list_of_sets_by_provider() method.
* Added get_options_for_harvests()
* Added doctests and docs for:
  - get_options_for_records()
  - get_options_for_mappings()
  - get_aggregator_options()
  _ get_mapping_details()

**Trivial and Dev Things**

* Separated packages and dev packages.
* Integrated pre-commit, black, and Flake8 into workflows.
* Created todo list.
* Created release history / change log.
* Created CONTRIBUTING.md.

0.0.1 (December 30, 2018)
-------------------------

* Birth and conception
