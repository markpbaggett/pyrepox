TODO List
=========

repox.repox.Repox
-----------------

1. Simplify metadata dict parameter for create_dataset method.
   The contents of the metadata dict is complicated. Add something to make this simpler.
2. export_dataset() returns a 200 even if permissions are wrong.  Do something about this.
3. Right now, there is only an update_oai_dataset.  Either make this more agnostic or add other methods.
4. XML returned as strings are always do not format correctly in restructured text / doctests.
5. get_list_of_running_harvests() always returns a 405 status code.
6. delete_record() always returns a 200 status code but doesn't do anything.
7. add_record() does not work.
8. add_mapping() does not work.
9. add option to schedule_harvest based on day of week
