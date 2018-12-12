import json
import requests
import xmltodict
import yaml # Adding temporarily for testing only


class Repox:
    def __init__(self, repox_url, username, password):
        self.swagger_endpoint = f"{repox_url}/repox/rest"
        self.username = username
        self.password = password

    def list_all_aggregators(self, verbose=True):
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators",
                                       auth=(self.username, self.password)).content)
        else:
            aggregators = json.loads(requests.get(f"{self.swagger_endpoint}/aggregators",
                                       auth=(self.username, self.password)).content)
            return [aggregator["id"] for aggregator in aggregators]

    def get_specific_aggregator(self, aggregator_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                                       auth=(self.username, self.password)).content)

    def get_aggregator_options(self):
        return json.loads(requests.get(f"{self.swagger_endpoint}/aggregators/options",
                                       auth=(self.username, self.password)).content)

    def create_aggregator(self):
        return

    def update_an_aggregator(self):
        return

    def delete_an_aggregator(self):
        return

    def get_list_of_providers(self, aggregator_id, verbose=False):
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                       auth=(self.username, self.password)).content)
        else:
            providers = json.loads(requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                       auth=(self.username, self.password)).content)
            return [provider["id"] for provider in providers]

    def get_provider(self, provider_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                       auth=(self.username, self.password)).content)

    def create_provider(self):
        return

    def update_provider(self):
        return

    def delete_provider(self):
        return

    def get_list_of_sets_from_provider(self, provider_id, verbose=False):
        if verbose is True:
            return json.loads(requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                       auth=(self.username, self.password)).content)
        else:
            data_sets = json.loads(requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                       auth=(self.username, self.password)).content)
            return [data_set["dataSource"]["id"] for data_set in data_sets]

    def get_dataset_details(self, data_set_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}",
                                       auth=(self.username, self.password)).content)

    def get_last_ingest_date_of_set(self, data_set_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/date",
                                       auth=(self.username, self.password)).content)["result"]

    def count_records_from_dataset(self, data_set_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/count",
                                       auth=(self.username, self.password)).content)["result"]

    def get_statistics(self):
        data = json.loads(requests.get(f"{self.swagger_endpoint}/statistics",
                                       auth=(self.username, self.password)).content)
        return json.dumps(xmltodict.parse(data["result"]))

    def get_options_for_mappings(self):
        return json.loads(requests.get(f"{self.swagger_endpoint}/mappings/options",
                                       auth=(self.username, self.password)).content)

    def get_options_for_records(self):
        return json.loads(requests.get(f"{self.swagger_endpoint}/records/options",
                                       auth=(self.username, self.password)).content)

    def get_record(self, record_id):
        return json.loads(requests.get(f"{self.swagger_endpoint}/records?recordId={record_id}",
                                       auth=(self.username, self.password)).content)

    def get_mapping_details(self, mapping_id):
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
    print(Repox(settings["url"], settings["username"], settings["password"]).get_mapping("UTKMODSrepaired"))