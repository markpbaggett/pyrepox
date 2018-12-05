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
            providers = json.loads(requests.get(f"{self.swagger_endpoint}/aggregators",
                                       auth=(self.username, self.password)).content)
            return [provider["id"] for provider in providers]


if __name__ == "__main__":
    settings = yaml.load(open("settings.yml", "r"))
    print(Repox(settings["url"], settings["username"], settings["password"]).list_all_aggregators(False))
