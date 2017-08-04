import json
import requests

class Aggregator:
    def __init__(self, identifier, name, name_code, home_page):
        self.identifier = identifier
        self.name = name
        self.name_code = name_code
        self.home_page = home_page

    def __str__(self):
        return self.name

    def create(self, username, password, url):
        headers = {'content-type': 'application/json'}
        data = {"Aggregator":
                    { "id": self.identifier, "name": self.name, "nameCode": self.name_code, "homepage": self.home_page}
                }
        r = requests.post(url, data=json.dumps(data), auth=(username, password), headers=headers)
        if r.status_code == 201:
            return "Successfully created aggregator."
        elif r.status_code == 409:
            return "Could not create aggregator. It already exists."
        else:
            return "There was a problem creating your aggregator."


class Provider:
    def __init__(self):
        self.identifier = ""
        self.name = ""
        self.country = ""
        self.country_code = ""
        self.description = ""
        self.name_code = ""
        self.home_page = ""
        self.provider_type = ""
        self.email = ""