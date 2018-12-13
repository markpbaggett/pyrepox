import json
import requests
import xmltodict
import yaml # Adding temporarily for testing only


class Repox:
    def __init__(self, repox_url: str, username: str, password: str):
        self.swagger_endpoint = f"{repox_url}/repox/rest"
        self.username = username
        self.password = password
        self.headers = {'content-type': 'application/json'}

    # Aggregators
    def list_all_aggregators(self, verbose: bool=True) -> list:
        """Returns all aggregators. If verbose is true, returns a list of dicts with metadata about aggregator.
        If verbose is false, returns a list of aggregator ids as strings.
        """
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators",
                                           auth=(self.username, self.password)).content)
        else:
            aggregators = json.loads(requests.get(f"{self.swagger_endpoint}/aggregators",
                                                  auth=(self.username, self.password)).content)
            return [aggregator["id"] for aggregator in aggregators]

    def get_aggregator(self, aggregator_id: str) -> dict:
        """Takes an aggregator id and returns metadata about the aggregator as a dict."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                                       auth=(self.username, self.password)).content)

    def get_aggregator_options(self) -> dict:
        return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators/options",
                                       auth=(self.username, self.password)).content)

    def create_aggregator(self, aggregator_id: str, aggregator_name: str, name_code: str="", homepage: str="") -> int:
        """Requires an identifier and name of aggregator.  Optionally takes a name_code and a homepage.
        If name_code is not specified, it's the same string as the aggregator_id. By default, the value of homepage is
        blank.

        The HTTP status code is returned as an int.
        """
        if name_code == "":
            name_code = aggregator_id
        aggregator_data = {"id": aggregator_id,
                           "name": aggregator_name,
                           "nameCode": name_code,
                           "homepage": homepage}
        return type(requests.post(f"{self.swagger_endpoint}/aggregators",
                                  auth=(self.username, self.password), headers=self.headers,
                                  data=json.dumps(aggregator_data)).status_code)

    def update_an_aggregator(self, aggregator_id):
        return

    def delete_an_aggregator(self):
        return

    # Providers
    def get_list_of_providers(self, aggregator_id: str, verbose: bool=False) -> list:
        """Takes an aggregator id and returns the providers that belong to that aggregator as a list. If verbose is
        true, metadata is included about each provider. If it is false, the list consists of provider ids as strings.
        """
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                           auth=(self.username, self.password)).content)
        else:
            providers = json.loads(requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                                auth=(self.username, self.password)).content)
            return [provider["id"] for provider in providers]

    def get_provider(self, provider_id: str) -> dict:
        """Takes a provider id and returns a dict of metadata about the provider."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                       auth=(self.username, self.password)).content)

    def create_provider(self):
        return

    def update_provider(self):
        return

    def delete_provider(self):
        return

    # Sets
    def get_list_of_sets_from_provider(self, provider_id: str, verbose: bool=False) -> list:
        """Takes a provider id and returns the data sets assoicated with it. If verbose is true, metadata about each
        set is included and the list consists of dicts.  If verbose is false, the list consists of dataset ids as
        strings.
        """
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                           auth=(self.username, self.password)).content)
        else:
            data_sets = json.loads(requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                                auth=(self.username, self.password)).content)
            return [data_set["dataSource"]["id"] for data_set in data_sets]

    def get_dataset_details(self, data_set_id: str) -> dict:
        """Returns metadata about a dataset as a dict."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}",
                                       auth=(self.username, self.password)).content)

    def get_last_ingest_date_of_set(self, data_set_id: str) -> str:
        """Returns the last ingestion date of a dataset as a string."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/date",
                                       auth=(self.username, self.password)).content)["result"]

    def count_records_from_dataset(self, data_set_id: str) -> str:
        """Returns the total number of records from a dataset as a string."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/count",
                                       auth=(self.username, self.password)).content)["result"]

    # Statistics
    def get_statistics(self) -> dict:
        """Returns statistics about the entire Repox instance as a dict."""
        data = json.loads(requests.get(f"{self.swagger_endpoint}/statistics",
                                       auth=(self.username, self.password)).content)
        return json.dumps(xmltodict.parse(data["result"]))

    # Mappings
    def get_options_for_mappings(self) -> dict:
        return json.loads(requests.get(f"{self.swagger_endpoint}/mappings/options",
                                       auth=(self.username, self.password)).content)

    def get_options_for_records(self) -> dict:
        return json.loads(requests.get(f"{self.swagger_endpoint}/records/options",
                                       auth=(self.username, self.password)).content)

    def get_record(self, record_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/records?recordId={record_id}",
                                       auth=(self.username, self.password)).content)

    def get_mapping_details(self, mapping_id) -> dict:
        """Returns metadata about a mapping as a dict."""
        return json.loads(requests.get(f"{self.swagger_endpoint}/mappings/{mapping_id}",
                                       auth=(self.username, self.password)).content)


if __name__ == "__main__":
    settings = yaml.load(open("settings.yml", "r"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).list_all_aggregators(False))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_specific_aggregator("TNDPLAr0"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_aggregator_options())
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_list_of_providers("TNDPLAr0"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_provider("utcr0"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_list_of_sets_from_provider("utcr0"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).count_records_from_dataset("p16877coll2"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_mapping("UTKMODSrepaired"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_last_ingest_date_of_set("p16877coll2"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_record("urn:dpla.lib.utk.edu.country_mods:6e3b2417-b744-486a-827f-9fbbd81de0a6"))
    print(Repox(settings["url"], settings["username"], settings["password"]).create_aggregator("test", "test"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_last_ingest_date_of_set("bcpl"))