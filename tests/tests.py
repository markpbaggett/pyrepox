from repox.repox import Repox
import unittest
from unittest.mock import patch
from .mocks import (
    mocked_aggregators_get_dict,
    mocked_aggregators_get_list,
    mocked_datasets_get_dict,
    mocked_datasets_get_list,
    mocked_datasets_get_str,
    mocked_providers_get_dict,
    mocked_providers_get_list,
    mocked_schedule_weekly_harvest,
    mocked_schedule_harvest,
)


class RepoxTestInitializeAndPrivates(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestInitializeAndPrivates, self).__init__(*args, **kwargs)

    def test_initialization(self):
        self.assertIsInstance(Repox("a", "b", "c"), Repox)

    @unittest.expectedFailure
    def test_esure_failure(self):
        self.assertNotIsInstance(Repox("a", "b"), Repox)
        self.assertNotIsInstance(Repox("a"), Repox)


class RepoxTestGetAggregatorMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestGetAggregatorMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch(
        "repox.repox.Repox.list_all_aggregators",
        side_effect=mocked_aggregators_get_list,
    )
    def test_list_aggregators(self, mock_get):
        repox_response = self.request.list_all_aggregators(False)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.list_all_aggregators(True)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch(
        "repox.repox.Repox.get_aggregator",
        side_effect=mocked_aggregators_get_dict,
    )
    def test_get_aggregator(self, mock_get):
        repox_response = self.request.get_aggregator("an_aggregator_id")
        self.assertIs(type(repox_response), dict)

    @patch(
        "repox.repox.Repox.get_aggregator_options",
        side_effect=mocked_aggregators_get_dict,
    )
    def test_get_aggregator_options(self, mock_get):
        repox_response = self.request.get_aggregator_options()
        self.assertIs(type(repox_response), dict)


class RepoxTestGetProviderMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestGetProviderMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch(
        "repox.repox.Repox.get_list_of_providers",
        side_effect=mocked_providers_get_list,
    )
    def test_get_list_of_providers(self, mock_get):
        repox_response = self.request.get_list_of_providers(
            aggregator_id="abc", verbose=False
        )
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.get_list_of_providers(
            aggregator_id="abc", verbose=True
        )
        print(repox_response)
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch(
        "repox.repox.Repox.get_provider", side_effect=mocked_providers_get_dict
    )
    def test_get_provider(self, mock_get):
        repox_response = self.request.get_provider(provider_id="abc")
        self.assertIs(type(repox_response), dict)

    @patch(
        "repox.repox.Repox.get_list_of_sets_from_provider",
        side_effect=mocked_datasets_get_list,
    )
    def test_get_list_of_sets_from_provider(self, mock_get):
        repox_response = self.request.get_list_of_sets_from_provider(
            provider_id="abc", verbose=False
        )
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), str)
        repox_response = self.request.get_list_of_sets_from_provider(
            provider_id="abc", verbose=True
        )
        self.assertIs(type(repox_response), list)
        self.assertIs(type(repox_response[0]), dict)

    @patch(
        "repox.repox.Repox.get_dataset_details",
        side_effect=mocked_datasets_get_dict,
    )
    def test_get_dataset_details(self, mock_get):
        repox_response = self.request.get_dataset_details(data_set_id="abc")
        self.assertIs(type(repox_response), dict)

    @patch(
        "repox.repox.Repox.get_last_ingest_date_of_set",
        side_effect=mocked_datasets_get_str,
    )
    def test_get_last_ingest_date_of_set(self, mock_get):
        repox_response = self.request.get_last_ingest_date_of_set(
            data_set_id="abc"
        )
        self.assertIs(type(repox_response), str)

    @patch(
        "repox.repox.Repox.count_records_in_dataset",
        side_effect=mocked_datasets_get_str,
    )
    def test_get_count_records_in_set(self, mock_get):
        repox_response = self.request.count_records_in_dataset(
            data_set_id="abc"
        )
        self.assertIs(type(repox_response), str)


class RepoxTestHarvestMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RepoxTestHarvestMethods, self).__init__(*args, **kwargs)
        self.request = Repox("http://localhost:8080", "admin", "admin")

    @patch(
        "repox.repox.Repox.schedule_weekly_harvest",
        side_effect=mocked_schedule_weekly_harvest,
    )
    def test_schedule_weekly_harvest(self, mock_get):
        repox_response = self.request.schedule_weekly_harvest(
            dataset_id="new_bcpl", day_of_week="Monday"
        )
        self.assertEqual(repox_response, 201)
        repox_response = self.request.schedule_weekly_harvest(
            dataset_id="new_bcpl", day_of_week="Tomorrow"
        )
        self.assertEqual(repox_response, 500)

    @patch(
        "repox.repox.Repox.schedule_harvest",
        side_effect=mocked_schedule_harvest,
    )
    def test_schedule_harvest(self, mock_get):
        repox_response = self.request.schedule_harvest(dataset_id="abc")
        self.assertEqual(repox_response, 201)
        repox_response = self.request.schedule_harvest(
            dataset_id="abc", frequency="DAILY"
        )
        self.assertEqual(repox_response, 201)
        repox_response = self.request.schedule_harvest(
            dataset_id="abc", frequency="YEARLY"
        )
        self.assertEqual(repox_response, 500)


if __name__ == "__main__":
    unittest.main()
