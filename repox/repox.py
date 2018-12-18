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
    def list_all_aggregators(self, verbose: bool=False) -> list:
        """Returns all aggregators. If verbose is true, returns a list of dicts with metadata about aggregator.
        If verbose is false, returns a list of aggregator ids as strings.
        """
        if verbose is True:
            return requests.get(f"{self.swagger_endpoint}/aggregators",
                                auth=(self.username, self.password)).json()
        else:
            aggregators = requests.get(f"{self.swagger_endpoint}/aggregators",
                                       auth=(self.username, self.password)).json()
            return [aggregator["id"] for aggregator in aggregators]

    def get_aggregator(self, aggregator_id: str) -> dict:
        """Takes an aggregator id and returns metadata about the aggregator as a dict."""
        return requests.get(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                            auth=(self.username, self.password)).json()

    def get_aggregator_options(self) -> dict:
        return requests.get(f"{self.swagger_endpoint}/aggregators/options",
                            auth=(self.username, self.password)).json()

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
            return requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                auth=(self.username, self.password)).json()
        else:
            providers = requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                     auth=(self.username, self.password)).json()
            return [provider["id"] for provider in providers]

    def get_provider(self, provider_id: str) -> dict:
        """Takes a provider id and returns a dict of metadata about the provider."""
        return requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                            auth=(self.username, self.password)).json()

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
        old_data = requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                auth=(self.username, self.password)).json()
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
        metadata = requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                auth=(self.username, self.password)).json()
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
            return requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                auth=(self.username, self.password)).json()
        else:
            data_sets = requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                     auth=(self.username, self.password)).json()
            return [data_set["dataSource"]["id"] for data_set in data_sets]

    def get_dataset_details(self, data_set_id: str) -> dict:
        """Returns metadata about a dataset as a dict."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}",
                            auth=(self.username, self.password)).json()

    def get_last_ingest_date_of_set(self, data_set_id: str) -> str:
        """Returns the last ingestion date of a dataset as a string."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/date",
                            auth=(self.username, self.password)).json()["result"]

    def count_records_from_dataset(self, data_set_id: str) -> str:
        """Returns the total number of records from a dataset as a string."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/count",
                            auth=(self.username, self.password)).json()["result"]

    # We need to determine what's actually required and what is not and write something to help with unpacking this.
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

    # This returns a 200 but doesn't seem to work. Could be write permissions?
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

    # If this goal is to humanize this, we need to make this as simple as possible for the user.
    # What does a oai set look like compared to a file set or z3950 set?
    def update_oai_dataset(self, dataset_id: str, export_dir: str="", metadata_format: str="", description: str="",
                           is_sample: bool=False, oai_url: str="", set_name: str="", name: str="", name_code: str="") \
            -> int:
        """Requires a dataset_id and accepts most metadata elements for an OAI dataset as a str.  If a metadata
        element is not passed, the value is taken from the previous data.

        Returns an HTTP status code as an int.
        """
        old_data = self.get_dataset_details(dataset_id)
        data_source_data = {"exportDir": export_dir, "description": description, "oaiSourceURL": oai_url,
                            "isSample": is_sample, "oaiSet": set_name}
        if metadata_format != "":
            format_data = self.__metadata_helper(metadata_format)
            if format_data["result"]["schema"] != "":
                data_source_data["schema"] = format_data["result"]["schema"]
                data_source_data["namespace"] = format_data["result"]["namespace"]
                data_source_data["metadataFormat"] = metadata_format
        for k, v in data_source_data.items():
            if v != "":
                old_data["dataSource"][k] = v
        if name != "":
            old_data["name"] = name
        if name_code != "":
            old_data["nameCode"] = name_code
        return requests.put(f"{self.swagger_endpoint}/datasets/{dataset_id}", headers=self.headers,
                            auth=(self.username, self.password), data=json.dumps(old_data)).status_code

    def delete_dataset(self, dataset_id: str) -> int:
        """Requires a dataset_id as a string and deletes the corresponding dataset.

        Returns an HTTP status code as an int.
        """
        return requests.delete(f"{self.swagger_endpoint}/datasets/{dataset_id}",
                               auth=(self.username, self.password)).status_code

    @staticmethod
    def __metadata_helper(metadata_format):
        """Private method that accepts a metadata format and returns a matching namespace and schema if one exists."""
        formats = {"mods":
            {
                "schema": 'http://www.loc.gov/standards/mods/v3/mods-3-5.xsd',
                "namespace": 'http://www.loc.gov/mods/v3'
            },
            "oai_dc":
                {
                    "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
                    "namespace": 'http://www.openarchives.org/OAI/2.0/'
                },
            "oai_qdc":
                {
                    "schema": "http://worldcat.org/xmlschemas/qdc/1.0/qdc-1.0.xsd",
                    "namespace": "http://worldcat.org/xmlschemas/qdc-1.0"
                }
        }
        current_format = metadata_format.lower()
        try:
            return {"result": formats[current_format]}
        except KeyError:
            return {"result": {"schema": "", "namespace": ""}}

    # Statistics
    def get_statistics(self) -> dict:
        """Returns statistics about the entire Repox instance as a dict."""
        data = requests.get(f"{self.swagger_endpoint}/statistics",
                            auth=(self.username, self.password)).json()
        return json.dumps(xmltodict.parse(data["result"]))

    # Harvests
    def get_scheduled_harvests(self, dataset_id: str) -> list:
        """Requires a dataset_id and returns a list of scheduled harvests as dicts."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedules",
                            auth=(self.username, self.password)).json()

    # What does a bad result look like?  Should we really return a dict here?
    def get_status_of_harvest(self, dataset_id: str) -> dict:
        """Requires a dataset_id and returns the status of the list havest as a dict."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/status",
                            auth=(self.username, self.password)).json()

    # This json.loads business everywhere else is ridiculous.  I forgot requests has a json method to handle this.
    def get_log_of_last_harvest(self, dataset_id: str) -> str:
        """Requires the dataset_id and returns the log of the last ingest as a string of XML."""
        return requests.get(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/log",
                            auth=(self.username, self.password)).json()["result"]

    # This seems to always return a 405 status code:  method not allowed for the requested resource.
    def get_list_of_running_harvests(self) -> str:
        """Returns a message about currently running harvests."""
        return requests.get(f"{self.swagger_endpoint}/datasets/harvest",
                            auth=(self.username, self.password)).text

    def harvest_set(self, dataset_id: str, is_sample: bool=False) -> int:
        """Requires a dataset_id as a string and optionally accepts an is_sample parameter as a bool.  By default,
        is_sample is False.  If is_sample is False, the entire set is harvested. If is_sample is True, only a subset
        of records are harvested.

        Returns the HTTP status code as an int.
        """
        if is_sample is False:
            harvest_type = "full"
        else:
            harvest_type = "sample"
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/start?type={harvest_type}",
                             auth=(self.username, self.password)).status_code

    # Need to figure out what the dict needs to look like. This isn't documented.
    def schedule_harvest(self, dataset_id: str, metadata: dict, incremental: bool=False) -> int:
        """Requires a dataset_id, metadata about the harvest as a dict, and optionally whether or not
        this is an incremental harvest (defaults to False).

        Returns the HTTP status code as an int.
        """
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedule?incremental="
                             f"{str(incremental).lower()}", headers=self.headers, data=json.dumps(metadata),
                             auth=(self.username, self.password)).status_code

    def cancel_running_harvest(self, dataset_id: str) -> int:
        """Requires the dataset_id as a string and cancels the associated harvest if it is running.

        Returns the HTTP status code as an int.
        """
        return requests.delete(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/cancel",
                               auth=(self.username, self.password)).status_code

    def delete_automatic_harvesting_task(self, dataset_id: str, task_id: str) -> int:
        """Requires the dataset_id of the set and the task_id related to the scheduled task.

        Returns the HTTP status code as an int.
        """
        return requests.delete(f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedules/{task_id}",
                               auth=(self.username, self.password)).status_code

    # Mappings
    def get_options_for_mappings(self) -> dict:
        return requests.get(f"{self.swagger_endpoint}/mappings/options",
                            auth=(self.username, self.password)).json()

    def get_options_for_records(self) -> dict:
        return requests.get(f"{self.swagger_endpoint}/records/options",
                            auth=(self.username, self.password)).json()

    def get_record(self, record_id: str) -> str:
        """Takes the OAI id from //record/header/identifier as a string and returns the value of //record/metadata
        as a string if it exists. If there is no metadata xpath, an exception is thrown and an error string is returned.
        """
        try:
            return requests.get(f"{self.swagger_endpoint}/records?recordId={record_id}",
                                auth=(self.username, self.password)).json()["result"]
        except json.decoder.JSONDecodeError:
            return "REPOX Error: This is a generic error and is thrown when Repox can't find a matching metadata.  " \
                   "This can be caused by an OAI record with the status of deleted."

    # While this returns a 200, it does not seem to do anything.  Post an issue in Repox.
    def delete_record(self, record_id: str) -> int:
        """Accepts a record id and deletes the corresponding record.  Returns the HTTP status code as an int."""
        return requests.get(f"{self.swagger_endpoint}/records?recordId={record_id}&type=delete",
                            auth=(self.username, self.password)).status_code

    # Need to test
    def add_a_record(self, dataset_id: str, record_id: str, xml_record: str) -> int:
        return requests.post(f"{self.swagger_endpoint}/records?datasetId={dataset_id}&recordId={record_id}",
                             auth=(self.username, self.password), headers="application/xml",
                             data=xml_record).status_code

    def get_mapping_details(self, mapping_id) -> dict:
        """Returns metadata about a mapping as a dict."""
        return requests.get(f"{self.swagger_endpoint}/mappings/{mapping_id}",
                            auth=(self.username, self.password)).json()

    # This is a TODO.
    def add_mapping(self):
        """
        {
        'id': 'UTKMODSrepaired',
        'description': 'UTK MODS modified for DLTN MODS',
        'sourceSchemaId': 'oai_mods',
        'destinationSchemaId': 'MODS',
        'stylesheet': 'utkmodstomods.xsl',
        'sourceSchemaVersion': '3.5',
        'versionTwo': True}

        :return:
        """
        return


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
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_mapping_details("UTKMODSrepaired"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).update_oai_dataset("bcpl", metadata_format="oai_qdc"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).delete_automatic_harvesting_task("bernhardt", "bernhardt_3"))
    print(Repox(settings["url"], settings["username"], settings["password"]).get_record("abc123"))