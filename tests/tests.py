from repox.repox import Repox
import unittest
from unittest.mock import patch


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


class RepoxTestGetAggregatorMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestGetAggregatorMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch("repox.repox.Repox.list_all_aggregators", side_effect=mocked_aggregators_get_list)
    def test_list_aggregators(self, mock_get):
        repox_response = self.request.list_all_aggregators(False)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.list_all_aggregators(True)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch("repox.repox.Repox.get_aggregator", side_effect=mocked_aggregators_get_dict)
    def test_get_aggregator(self, mock_get):
        repox_response = self.request.get_aggregator("an_aggregator_id")
        self.assertIs(type(repox_response), dict)

    @patch("repox.repox.Repox.get_aggregator_options", side_effect=mocked_aggregators_get_dict)
    def test_get_aggregator_options(self, mock_get):
        repox_response = self.request.get_aggregator_options()
        self.assertIs(type(repox_response), dict)


class RepoxTestGetProviderMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestGetProviderMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch("repox.repox.Repox.get_list_of_providers", side_effect=mocked_providers_get_list)
    def test_get_list_of_providers(self, mock_get):
        repox_response = self.request.get_list_of_providers(aggregator_id="abc", verbose=False)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.get_list_of_providers(aggregator_id="abc", verbose=True)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch("repox.repox.Repox.get_provider", side_effect=mocked_providers_get_dict)
    def test_get_provider(self, mock_get):
        repox_response = self.request.get_provider(provider_id="abc")
        self.assertIs(type(repox_response), dict)

if __name__ == '__main__':
    unittest.main()
