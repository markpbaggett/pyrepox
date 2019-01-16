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


def mocked_schedule_weekly_harvest(*args, **kwargs):
    class MockWeeklyResponse:
        def __init__(self, dataset_id, day="Tuesday"):
            self.status_code = self.test_day(day)

        @staticmethod
        def test_day(user_input):
            days_of_week = (
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            )
            if user_input in days_of_week:
                return 201
            else:
                return 500

    if "dataset_id" in kwargs and "day_of_week" in kwargs:
        return MockWeeklyResponse("abc", kwargs["day_of_week"]).status_code
    else:
        return 500


def mocked_schedule_harvest(*args, **kwargs):
    class MockScheduleHarvest:
        def __init__(
            self,
            dataset_id,
            frequency="ONCE",
            time="NOT SET",
            date="NOT SET",
            xmonths=0,
            incremental=False,
        ):
            self.dataset_id = dataset_id
            self.frequency = frequency
            self.time = time
            self.date = date
            self.xmonths = xmonths
            self.incremental = incremental
            self.status_code = self.determine_status()

        def determine_status(self):
            possible_frequencies = ("ONCE", "DAILY", "WEEKLY", "XMONTHLY")
            if self.frequency not in possible_frequencies:
                return 500
            elif type(self.incremental) != bool:
                return 500
            else:
                return 201

    if "dataset_id" in kwargs and "frequency" in kwargs:
        return MockScheduleHarvest(
            kwargs["dataset_id"], frequency=kwargs["frequency"]
        ).status_code
    elif "dataset_id" in kwargs:
        return MockScheduleHarvest(kwargs["dataset_id"]).status_code
    else:
        return 500
