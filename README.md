# Pyrepox: Repox for Humans

![Travis icon](https://travis-ci.org/markpbaggett/pyrepox.png)
![readthedocs icon](https://readthedocs.org/projects/pyrepox/badge/?version=latest)
[![PyPI version](https://badge.fury.io/py/repox.svg)](https://badge.fury.io/py/repox)

Pyrepox is a lightweight [Repox](https://github.com/europeana/REPOX)
client written in Python. It is designed to make reading, writing,
updating, and deleting content in your Repox instance as convenient as
possible.

```python
>>> from repox.repox import Repox
>>> r = Repox("http://localhost:8080", "username", "password")
>>> r.list_all_aggregators()
['dltn']
>>> r.list_all_aggregators(verbose=True)
[{'id': 'dltn', 'name': 'Digital Library of Tennessee', 'nameCode': 'dltn',
'homepage': 'http://localhost:8080/repox'}]
>>> r.get_list_of_providers("dltn")
['utk', 'utc', 'cmhf', 'knox', 'mtsu', 'crossroads', 'tsla', 'nash', 'memphis']
```

## Installation

```
$ pip install repox
```

## Documentation

Documentation is available at [https://pyrepox.readthedocs.io/en/latest/](https://pyrepox.readthedocs.io/en/latest/).

Examples for each currently defined method is documented in the 
[repox package documentation](https://pyrepox.readthedocs.io/en/latest/source/repox.html).

[Todos](https://pyrepox.readthedocs.io/en/latest/todo.html) are also documented.

## Want to Help?

Help is very much appreciated.  See [Contributing](https://github.com/markpbaggett/pyrepox/blob/master/CONTRIBUTING.rst)
or open an issue in the [issue tracker](https://github.com/markpbaggett/pyrepox/issues). 
