def mocked_aggregators_get_list(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if args[0] is False:
        return MockResponse(["a", "b", "c", "d"]).json()
    elif args[0] is True:
        return MockResponse(
            [{"key1": "a"}, {"key1": "b"}, {"key1": "c"}]
        ).json()

    return MockResponse(None)


def mocked_aggregators_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if len(args) is 0:
        return MockResponse({"option": [{"description": "test"}]}).json()

    elif args[0] is "an_aggregator_id":
        return MockResponse({"result": "Aggregator does NOT exist!"}).json()

    return MockResponse(None)


def mocked_providers_get_list(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if "aggregator_id" in kwargs and kwargs["verbose"] is False:
        return MockResponse(["provider1", "provider2", "provider3"]).json()

    elif "aggregator_id" in kwargs and kwargs["verbose"] is True:
        return MockResponse(
            [
                {"name": "provider1"},
                {"name": "provider2"},
                {"name": "provider3"},
            ]
        ).json()

    return MockResponse(None)


def mocked_providers_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if "provider_id" in kwargs:
        return MockResponse({"provider": "abc"}).json()

    return MockResponse(None)


def mocked_datasets_get_list(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if "provider_id" in kwargs and kwargs["verbose"] is False:
        return MockResponse(["set1, set2, set3"]).json()

    elif "provider_id" in kwargs and kwargs["verbose"] is True:
        return MockResponse(
            [{"name": "set1"}, {"name": "set2"}, {"name": "set3"}]
        ).json()

    return MockResponse(None)


def mocked_datasets_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if "data_set_id" in kwargs:
        return MockResponse({"set_name": "nr", "id": "4"}).json()

    return MockResponse(None)


def mocked_datasets_get_str(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

    if "data_set_id" in kwargs:
        return MockResponse("November 8, 2018").content

    return MockResponse(None)
