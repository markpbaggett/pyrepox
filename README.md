# Pyrepox: Repox for Humans

![Travis icons](https://travis-ci.org/markpbaggett/pyrepox.png)

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



## Dependencies

* requests
* xmltodict