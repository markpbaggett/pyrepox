# Contributing

## Report bugs, issues, and other problems

Report bugs through the [issue tracker](https://github.com/markpbaggett/pyrepox/issues).

**NOTE**: some bugs are acknowledge in the [TODO list](https://pyrepox.readthedocs.io/en/latest/todo.html).

## Contributing Code

* Fork the repo.
* Clone locally.
* Create a branch for your feature / issue.

```
$ git checkout -b name_of_bug_or_feature
```

* After you're done, run flake8 and black versus your changes and make sure you pass unittests:

```
$ flake8 file_changed.py
$ black file_changed.py
$ python -m unittest --verbose
```

* Add, commit, and push your branch to your fork.

```
$ git add file_changed.py
$ git commit -m "Talk about your change."
$ git push origin master
```

* Open pull request.
