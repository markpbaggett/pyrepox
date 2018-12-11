import json
import requests
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


if __name__ == "__main__":
    settings = yaml.load(open("settings.yml", "r"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).list_all_aggregators(False))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_specific_aggregator("TNDPLAr0"))
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_aggregator_options())
    #print(Repox(settings["url"], settings["username"], settings["password"]).get_list_of_providers("TNDPLAr0"))
    print(Repox(settings["url"], settings["username"], settings["password"]).get_provider("utcr0"))
