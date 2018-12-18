def mocked_aggregators_get_list(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if args[0] is False:
        return MockResponse(["a", "b", "c", "d"]).json()
    elif args[0] is True:
        return MockResponse([{"key1": "a"}, {"key1": "b"}, {"key1": "c"}]).json()

    return MockResponse(None)


def mocked_aggregators_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if len(args) is 0:
        return MockResponse({'option': [{"description": "test"}]}).json()

    elif args[0] is "an_aggregator_id":
        return MockResponse({'result': 'Aggregator does NOT exist!'}).json()

    return MockResponse(None)


def mocked_providers_get_list(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if kwargs["aggregator_id"] and kwargs["verbose"] is False:
        return MockResponse(["provider1", "provider2", "provider3"]).json()

    elif kwargs["aggregator_id"] and kwargs["verbose"] is True:
        return MockResponse([{"name": "provider1"}, {"name": "provider2"}, {"name": "provider3"}]).json()

    return MockResponse(None)


def mocked_providers_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if kwargs["provider_id"]:
        return MockResponse({"provider": "abc"}).json()

    return MockResponse(None)
