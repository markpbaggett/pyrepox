from repox.repox import Repox
import unittest
from unittest.mock import patch


def mocked_requests_get_list(*args, **kwargs):
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


def mocked_requests_get_dict(*args, **kwargs):
    class MockResponse:
        def __init__(self, response):
            self.content = response

        def json(self):
            return self.content

    if args[0] is "an_aggregator_id":
        return MockResponse({'result': 'Aggregator does NOT exist!'}).json()

    return MockResponse(None)


class RepoxTestAggregatorMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestAggregatorMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch("repox.repox.Repox.list_all_aggregators", side_effect=mocked_requests_get_list)
    def test_list_aggregators(self, mock_get):
        repox_response = self.request.list_all_aggregators(False)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.list_all_aggregators(True)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch("repox.repox.Repox.get_aggregator", side_effect=mocked_requests_get_dict)
    def test_get_aggregator(self, mock_get):
        repox_response = self.request.get_aggregator("an_aggregator_id")
        self.assertIs(type(repox_response), dict)



if __name__ == '__main__':
    unittest.main()
