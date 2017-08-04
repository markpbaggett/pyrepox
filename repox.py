import json
import requests


class Aggregator:
    def __init__(self, identifier, name, name_code, home_page, headers=None):
        self.identifier = identifier
        self.name = name
        self.name_code = name_code
        self.home_page = home_page
        if headers is None:
            self.headers = {'content-type': 'application/json'}
        else:
            self.headers = headers

    def __str__(self):
        return self.name

    def create(self, username, password, url):
        data = {"id": self.identifier, "name": self.name, "nameCode": self.name_code, "homepage": self.home_page}
        r = requests.post(url, data=json.dumps(data), auth=(username, password), headers=self.headers)
        if r.status_code == 201:
            return "Successfully created aggregator {}.".format(self.name)
        elif r.status_code == 409:
            return "ERROR {}: Could not create aggregator {}. It already exists.".format(r.status_code, self.name)
        else:
            return "ERROR {}: There was a problem creating aggregator {}.".format(r.status_code, self.name)

    def update(self, username, password, url, data=None):
        if data is None:
            return "Could not update aggregator {}. The request body was empty.".format(self.name)
        r = requests.put("{}/{}".format(url, self.identifier), data=json.dumps(data), auth=(username, password),
                       headers=self.headers)
        if r.status_code == 200:
            return "Successfully updated aggegator {}.".format(self.name)
        elif r.status_code == 400:
            return "ERROR {}: Could not update {}.  The arguments were invalid".format(r.status_code, self.name)
        elif r.status_code == 404:
            return "ERROR {}: Could not update {}.  The aggregator does not exist.".format(r.status_code, self.name)
        else:
            return "ERROR {}: Could not update {}.".format(r.status_code, self.name)

    def delete(self, username, password, url):
        r = requests.delete("{}{}".format(url, self.identifier), auth=(username, password))
        if r.status_code == 200:
            return "Sucessfully deleted aggregator {}.".format(self.name)
        elif r.status_code == 404:
            return "ERROR {}: Aggregator {} could not be deleted because it does not exist.".format(r.status_code,
                                                                                                    self.name)
        else:
            return "ERROR {}: Could not delete aggregator {}.".format(r.status_code, self.name)


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