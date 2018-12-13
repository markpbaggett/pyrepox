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
        return requests.post(f"{self.swagger_endpoint}/aggregators", auth=(self.username, self.password),
                             headers=self.headers, data=json.dumps(aggregator_data)).status_code

    def update_aggregator(self, aggregator_id: str, aggregator_name: str="", name_code: str="", homepage: str="") \
            -> int:
        """Requires an aggregator_id.  Accepts an aggregator_name, name_code, or homepage.  If any of these are not
        present, the current data is passed.

        Returns an HTTP status code as an int.
        """
        old_data = self.get_aggregator(aggregator_id)
        if aggregator_name == "":
            aggregator_name = old_data["name"]
        if name_code == "":
            name_code = old_data["nameCode"]
        if homepage == "":
            homepage == old_data["homepage"]
        aggregator_data = {"id": aggregator_id,
                           "name": aggregator_name,
                           "nameCode": name_code,
                           "homepage": homepage}
        return requests.put(f"{self.swagger_endpoint}/aggregators/{aggregator_id}", headers=self.headers,
                            auth=(self.username, self.password), data=json.dumps(aggregator_data)).status_code

    def delete_aggregator(self, aggregator_id: str) -> int:
        """Takes an aggregator id and deletes the corresponding aggregator.  Returns the HTTP status code as an int."""
        return requests.delete(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                               auth=(self.username, self.password)).status_code

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

    # Add a static method to check the contents of metadata to avoid 400 / 406 status codes.
    def create_provider(self, aggregator_id: str, metadata: dict) -> int:
        """Takes an aggregator id and adds a new provider based on the contents of a metadata dict.
        A metadata dict looks like this:

        {"id": "abcd123",
         "name": "Test provider",
         "country": "United States",
         "countryCode": "",
         "description": "What is this",
         "nameCode": "abcd123",
         "homepage": "https://google.com",
         "providerType": "LIBRARY",
         "email": "mbagget1@utk.edu"}

        Returns an HTTP status code as a string.
        """
        return requests.post(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}", headers=self.headers,
                             auth=(self.username, self.password), data=json.dumps(metadata)).status_code

    def update_provider(self, provider_id: str, name: str="", country: str="", country_code: str="",
                        description: str="", name_code: str="", homepage: str="", provider_type: str="",
                        email: str="") -> int:
        """Takes a provider_id as a string and optionally any metadata value for any other field you want to change.
        If a field value is not provided, the current field value is passed to the API along with new fields.

        Returns the HTTP status code of the response.
        """
        old_data = json.loads(requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                           auth=(self.username, self.password)).content)
        if name == "":
            name = old_data["name"]
        if country == "":
            country = old_data["country"]
        if country_code == "":
            country_code = old_data["countryCode"]
        if description == "":
            description = old_data["description"]
        if name_code == "":
            name_code = old_data["nameCode"]
        if homepage == "":
            homepage = old_data["homepage"]
        if provider_type == "":
            provider_type = old_data["providerType"]
        if email == "":
            email = old_data["email"]
        metadata = {"id": provider_id,
                    "name": name,
                    "country": country,
                    "countryCode": country_code,
                    "description": description,
                    "nameCode": name_code,
                    "homepage": homepage,
                    "providerType": provider_type,
                    "email": email}
        return requests.put(f"{self.swagger_endpoint}/providers/{provider_id}", auth=(self.username, self.password),
                            headers=self.headers, data=json.dumps(metadata)).status_code

    def assign_provider_to_new_aggregator(self, provider_id: str, aggregator_id: str) -> int:
        """Takes a provider_id and an aggegator_id and moves the provider with the provider_id to the aggregator with
        the aggregator_id.

        Returns an HTTP status code as an int.
        """
        metadata = json.loads(requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                           auth=(self.username, self.password)).content)
        return requests.put(f"{self.swagger_endpoint}/providers/{provider_id}?newAggregatorId={aggregator_id}",
                            auth=(self.username, self.password), data=json.dumps(metadata),
                            headers=self.headers).status_code

    def delete_provider(self, provider_id: str) -> int:
        """Accepts a provider_id and deletes the corresponding provider in Repox.

        Returns the HTTP status code as an int.
        """
        return requests.delete(f"{self.swagger_endpoint}/providers/{provider_id}",
                               auth=(self.username, self.password)).status_code

    # Sets
    def get_list_of_sets_from_provider(self, provider_id: str, verbose: bool=False) -> list:
        """Takes a provider id and returns the data sets associated with it. If verbose is true, metadata about each
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

    # We need to determine what's actually required here and what is not and write something to help with unpacking this.
    def create_dataset(self, provider_id: str, metadata: dict) -> int:
        """Takes a provider_id and creates a new dataset in it based on the contents of a metadata dict.

        Example metadata:
        {
            "containerType": "DEFAULT",
            "dataSource":
                {
                    "exportDir": "/home/vagrant",
                    "metadataFormat": "oai_dc",
                    "marcFormat": "",
                    "recordIdPolicy":
                        {
                            "IdProvided":
                                {}
                        },
                    "isSample": False,
                    "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
                    "namespace": "http://purl.org/dc/elements/1.1/",
                    "description": "nashville_test",
                    "id": "nashville_test",
                    "dataSetType": "OAI",
                    "oaiSourceURL": "https://dpla.lib.utk.edu/repox/OAIHandler",
                    "oaiSet": "p15769coll18"
            },
            "name": "nashville_test",
            "nameCode": "nashville_test"
        }

        Returns an HTTP status code as an int.
        """
        return requests.post(f"{self.swagger_endpoint}/datasets?providerId={provider_id}", headers=self.headers,
                             auth=(self.username, self.password), data=json.dumps(metadata)).status_code

    # This returns a 200 but doesn't seem to work.
    def export_dataset(self, dataset_id: str) -> int:
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}/export", headers=self.headers,
                             auth=(self.username, self.password)).status_code

    def copy_dataset(self, dataset_id: str, new_dataset_id: str) -> int:
        """Takes a dataset_id for an existing dataset and creates a new dataset in the same provider based on existing
        metadata and a new_dataset_id.

        Returns an HTTP status code as an int.
        """
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}?newDatasetId={new_dataset_id}",
                             headers=self.headers, auth=(self.username, self.password)).status_code

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

    def get_record(self, record_id: str) -> str:
        """Takes the OAI id from //record/header/identifier as a string and returns the value of //record/metadata
        as a string if it exists. If there is no metadata xpath, an exception is thrown and an error string is returned.
        """
        try:
            return json.loads(requests.get(f"{self.swagger_endpoint}/records?recordId={record_id}",
                                           auth=(self.username, self.password)).content)["result"]
        except json.decoder.JSONDecodeError:
            return "REPOX Error: This is a generic error and is thrown when Repox can't find a matching metadata.  " \
                   "This can be caused by an OAI record with the status of deleted."

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
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_record("oai:dltn.repox.test.bernhardt:urn:dpla.lib.utk.edu.mtsu_buchanan:oai:cdm15838.contentdm.oclc.org:buchanan/29"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).update_aggregator("test", homepage="http://google.com"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_last_ingest_date_of_set("bcpl"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).delete_aggregator("test"))
    # x = {"id": "abcd",
    #      "name": "Test",
    #      "country": "United States",
    #      "countryCode": "",
    #      "description": "a",
    #      "nameCode": "abcd",
    #      "homepage": "google.com",
    #      "providerType": "LIBRARY",
    #      "email": "a"}
    # print(Repox(settings["url"], settings["username"], settings["password"]).create_provider("dltn", x))
    #print(Repox(settings["url"], settings["username"], settings["password"]).update_provider("abcd", email="mark@utk.edu"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).create_aggregator("mark", "mark"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).assign_provider_to_new_aggregator("abcd", "dltn"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).delete_provider("abcd"))
    # x = {
    #     "containerType": "DEFAULT",
    #     "dataSource":
    #         {
    #         "exportDir": "/home/vagrant",
    #         "metadataFormat": "oai_dc",
    #         "marcFormat": "",
    #         "recordIdPolicy":
    #             {"IdProvided": {}},
    #         "isSample": False,
    #         "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
    #         "namespace": "http://purl.org/dc/elements/1.1/",
    #         "description": "nashville_test",
    #         "id": "nashville_test",
    #         "dataSetType": "OAI",
    #         "oaiSourceURL": "https://dpla.lib.utk.edu/repox/OAIHandler",
    #         "oaiSet": "p15769coll18"
    #         },
    #     "name": "nashville_test",
    #     "nameCode": "nashville_test"
    # }
    # print(Repox(settings["url"], settings["username"], settings["password"]).create_dataset("utk", x))
    #print(Repox(settings["url"], settings["username"], settings["password"]).export_dataset("bcpl"))
    print(Repox(settings["url"], settings["username"], settings["password"]).copy_dataset("bcpl", "new_bcpl"))