import json
import requests
import xmltodict


class Repox:
    def __init__(self, repox_url: str, username: str, password: str):
        """Creates a new instance of Repox.

        Args:
            repox_url (str): The url of your Repox instance.
            username (str): The username used to connect to the Swagger API.
            password (str): The password used to connect to the Swagger API.

        """
        self.swagger_endpoint = f"{repox_url}/repox/rest"
        self.username = username
        self.password = password
        self.headers = {'content-type': 'application/json'}

    def __repr__(self):
        return f"Repox connection instance based on {self.swagger_endpoint}."

    # Aggregators
    def list_all_aggregators(self, verbose: bool=False) -> list:
        """Returns all aggregators and optionally metadata about each.

        This method returns all aggregators for this Repox install.  Optionally, you can also retrieve metadata about
        each aggregator by passing True to the verbose parameter.  By default, this value is False.

        Args:
            verbose (bool): specify whether you want metadata returned. False by default.

        Returns:
            list: A list of aggregators.  The list is strings if verbose is False and dicts if it is True.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').list_all_aggregators(True)
            [{'id': 'dltn', 'name': 'Digital Library of Tennessee', 'nameCode': 'dltn',
            'homepage': 'http://localhost:8080/repox'}]
            >>> Repox('http://localhost:8080', 'username', 'password').list_all_aggregators(False)
            ['dltn']

        """
        if verbose is True:
            return requests.get(f"{self.swagger_endpoint}/aggregators",
                                auth=(self.username, self.password)).json()
        else:
            aggregators = requests.get(f"{self.swagger_endpoint}/aggregators",
                                       auth=(self.username, self.password)).json()
            return [aggregator["id"] for aggregator in aggregators]

    def get_aggregator(self, aggregator_id: str) -> dict:
        """Takes an aggregator id and returns metadata about the aggregator as a dict.

        Args:
            aggregator_id (str): Specify the aggregator you wish to return.

        Returns:
            dict: A dict of metadata about the specified aggregator.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').get_aggregator("dltn")
            {'id': 'dltn', 'name': 'DLTN Test', 'nameCode': 'dltn', 'homepage': 'http://localhost:8080/repox'}

        """
        return requests.get(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                            auth=(self.username, self.password)).json()

    def get_aggregator_options(self) -> dict:
        return requests.get(f"{self.swagger_endpoint}/aggregators/options",
                            auth=(self.username, self.password)).json()

    def create_aggregator(self, aggregator_id: str, aggregator_name: str, name_code: str="", homepage: str="") -> int:
        """Creates an aggregator.

        Requires an identifier and a name for the aggregator.  Optionally takes a name_code and a homepage for the new
        aggregator. If a name_code is not specified, it uses the same string as the aggregator_id. By default, the value
        of homepage is blank.

        Args:
            aggregator_id (str): Required. Specify an identifier for the new aggregator.
            aggregator_name (str): Required. Specify a name for the new aggregator.
            name_code (str): Optionally include a name_code for the new aggregator.
            homepage (str): Optionally include a homepage for the new aggregator.

        Returns:
            int: The HTTP status code based on your request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').create_aggregator("new_dltn", "New DLTN")
            201

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
        """Update an aggregator.

        Update an aggregator by specifying its aggregator_id.  Optionally, pass an aggregator_name, name_code, or
        homepage.  If any of these are not present, the current data will be used.

        Args:
            aggregator_id (str): Required. The aggregator_id for the aggregator you want to update.
            aggregator_name (str): Optionally update the aggregator_name.
            name_code (str): Optionally update the aggregator's name_code.
            homepage (str): Optionally update the aggregator's homepage.

        Returns:
            int: The HTTP status code from your request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').update_aggregator("new_dltn",
            ... homepage="http://www.tenn-share.org/af_membercommittee.asp?committeeid=28")
            200

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
        """Delete an aggregator.

        Delete an aggregator by specifying its aggregator_id.

        Args:
            aggregator_id (str): Required. The aggregator_id of the aggregator you want to delete.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').delete_aggregator("new_dltn")
            200

        """
        return requests.delete(f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
                               auth=(self.username, self.password)).status_code

    # Providers
    def get_list_of_providers(self, aggregator_id: str, verbose: bool=False) -> list:
        """Get a list of providers and its metadata for a specific aggregator.

        Requires an aggregator id and returns the providers that belong to it as a list. Optionally, you can also
        return metadata about each provider.

        Args:
            aggregator_id (str): Required. The aggregator_id of the providers you want to return.
            verbose (bool): Optional. If True, return metadata about each provider.

        Returns:
            list: The list of providers that match your request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').get_list_of_providers("TNDPLAr0")
            ['CountryMusicHallofFamer0', 'CrossroadstoFreedomr0', 'KnoxPLr0', 'memphispublicr0', 'MTSUr0',
            'nashvillepublicr0', 'tslar0', 'utcr0', 'UTKr0']

            >>> Repox('http://localhost:8080', 'username', 'password').get_list_of_providers("TNDPLAr0", True)
            [{'id': 'CountryMusicHallofFamer0', 'name': 'Country Music Hall of Fame', 'countryCode': 'al',
            'description': '', 'nameCode': '', 'homepage': 'http://digi.countrymusichalloffame.org/oai/oai.php',
            'providerType': 'MUSEUM', 'email': ''}, {'id': 'CrossroadstoFreedomr0', 'name': 'CrossroadstoFreedom',
            'countryCode': 'de', 'description': '', 'nameCode': '', 'homepage': '', 'providerType': 'ARCHIVE',
            'email': ''}, {'id': 'KnoxPLr0', 'name': 'Knoxville Public Library', 'countryCode': 'al', 'description': '',
            'nameCode': 'KnoxPublicLibrary', 'homepage': '', 'providerType': 'LIBRARY', 'email': ''},
            {'id': 'memphispublicr0', 'name': 'Memphis Public Library', 'countryCode': 'al', 'description': '',
            'nameCode': 'memphispublic', 'homepage': '', 'providerType': 'LIBRARY', 'email': ''}, {'id': 'MTSUr0',
            'name': 'Middle Tennessee State University', 'countryCode': 'al', 'description': '', 'nameCode': 'mtsu',
            'homepage': '', 'providerType': 'LIBRARY', 'email': ''}, {'id': 'nashvillepublicr0', 'name':
            'Nashville Public Library', 'countryCode': 'al', 'description': '', 'nameCode': 'nashvillepublic',
            'homepage': '', 'providerType': 'LIBRARY', 'email': ''}, {'id': 'tslar0', 'name': 'Tennessee State Library',
            'countryCode': 'al', 'description': '', 'nameCode': 'tsla', 'homepage': '', 'providerType': 'LIBRARY',
            'email': ''}, {'id': 'utcr0', 'name': 'UT Chattanooga', 'countryCode': 'al', 'description': '', 'nameCode':
            'utc', 'homepage': '', 'providerType': 'MUSEUM', 'email': ''}, {'id': 'UTKr0', 'name': 'UTK', 'countryCode':
            'al', 'description': 'University of Tennessee Knoxville', 'nameCode': '', 'homepage': '', 'providerType':
            'LIBRARY', 'email': ''}]

        """
        if verbose is True:
            return requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                auth=(self.username, self.password)).json()
        else:
            providers = requests.get(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                                     auth=(self.username, self.password)).json()
            return [provider["id"] for provider in providers]

    def get_provider(self, provider_id: str) -> dict:
        """Get metadata about a provider.

        Requires a provider id and returns metadata about it.

        Args:
            provider_id (str): The provider_id of the provider you want to return.

        Returns:
            dict: The metadata about your specified provider.

        Examples:
              >>> Repox('http://localhost:8080', 'username', 'password').get_provider("UTKr0")
              {'id': 'UTKr0', 'name': 'UTK', 'countryCode': 'al', 'description': 'University of Tennessee Knoxville',
              'nameCode': '', 'homepage': '', 'providerType': 'LIBRARY', 'email': ''}

        """
        return requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                            auth=(self.username, self.password)).json()

    # TODO Add a static method to check the contents of metadata to avoid 400 / 406 status codes.
    # TODO Describe the required parts of a metadata dict.
    def create_provider(self, aggregator_id: str, metadata: dict) -> int:
        """Create a provider in a specific aggregator.

        Requires an aggregator_id and adds a new provider based on the contents of a metadata dict.

        Args:
            aggregator_id (str): Required.  The aggregator_id of the aggregator you are adding your provider to.
            metadata (dict): Required.  Key value pairs that describe the provider you are creating.

        Returns:
            int: The HTTP status code of the request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').create_provider("dltn", {"id": "utc", "name":
            ... "UT Chattanooga", "country": "United States", "countryCode": "", "description":
            ... "OAI Sets from the University of Tennessee, Chattanooga", "nameCode": "utc", "homepage":
            ... "http://cdm16877.contentdm.oclc.org", "providerType": "LIBRARY", "email": "carolyn-runyon@utc.edu"})
            201

        """
        return requests.post(f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}", headers=self.headers,
                             auth=(self.username, self.password), data=json.dumps(metadata)).status_code

    # TODO Determine if there is a list of allowed country codes.
    # TODO Determine if there is an exhaustive list of provider_types.
    def update_provider(self, provider_id: str, name: str="", country: str="", country_code: str="",
                        description: str="", name_code: str="", homepage: str="", provider_type: str="",
                        email: str="") -> int:
        """Update the metadata about a provider.

        Requires a provider_id as a string and optionally any metadata value for any other field you want to modify.
        If a field value is not provided, the current field value is passed to the API along with new values.

        Args:
            provider_id (str): Required.  The provider_id of the provider you want to modify.
            name (str): Optional. A new name for the specified provider.
            country (str): Optional. A new country value for the specified provider.
            country_code (str): Optional.  A new country_code to represent the provider.
            description (str): Optional. A new description for the provider.
            name_code (str): Optional. A new name_code to represent the provider.
            homepage (str): Optional. A new homepage that represents the provider.
            provider_type (str): Optional. A new provider_type that represents the provider.
            email (str): Optional. A new email address to associate with the provider.

        Returns:
            int: The HTTP status code response of the request.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').update_provider("UTKr0",
            ... homepage="http://dloai.lib.utk.edu/cgi-bin/XMLFile/dlmodsoai/oai.pl", email="mbagget1@utk.edu")
            200

        """
        old_data = requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                auth=(self.username, self.password)).json()
        if name == "":
            name = old_data["name"]
        if country == "":
            try:
                country = old_data["country"]
            except KeyError:
                country = ""
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
        """Assign and existing provider to another aggregator.

        Requires a provider_id and an aggegator_id and moves the specified provider to the aggregator with the
        specified aggregator_id.

        Args:
            provider_id (str): Required. The provider_id of the provider you want to move.
            aggregator_id (str): Required. The aggregator_id of the aggregator you want to assign your provider to.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").assign_provider_to_new_aggregator("abcd123",
            ... "NewDLTNr0")
            200

        """
        metadata = requests.get(f"{self.swagger_endpoint}/providers/{provider_id}",
                                auth=(self.username, self.password)).json()
        return requests.put(f"{self.swagger_endpoint}/providers/{provider_id}?newAggregatorId={aggregator_id}",
                            auth=(self.username, self.password), data=json.dumps(metadata),
                            headers=self.headers).status_code

    def delete_provider(self, provider_id: str) -> int:
        """Delete a provider.

        Requires a provider_id and deletes the corresponding provider in Repox.

        Args:
            provider_id (str): The provider_id of the provider you want to delete.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").delete_provider("abcd123")
            200

        """
        return requests.delete(f"{self.swagger_endpoint}/providers/{provider_id}",
                               auth=(self.username, self.password)).status_code

    # Sets
    def get_list_of_sets_from_provider(self, provider_id: str, verbose: bool=False) -> list:
        """Get list of datasets associated with a provider.

        Requires a provider id and returns the data sets associated with it. If verbose is true, metadata about each
        set is also included in the response.

        Args:
            provider_id (str): Required. The provider_id of the provider from which you want sets returned.
            verbose (bool): Optional. Set to True if you want metadata in your response.  Defaults to False.

        Returns:
            list: A list of datasets and optionally each's metadata.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_list_of_sets_from_provider("utcr0")
            ['p16877coll1', 'p16877coll2', 'p16877coll3', 'p16877coll4', 'p16877coll5', 'p16877coll6', 'p16877coll7',
            'p16877coll8', 'p16877coll9', 'utc_p16877coll10', 'utc_p16877coll11', 'utc_p16877coll12',
            'utc_p16877coll13', 'utc_p16877coll14', 'utc_p16877coll15', 'utc_p16877coll16', 'utc_p16877coll17',
            'utc_p16877coll18', 'utc_p16877coll19', 'utc_p16877coll20', 'utc_p16877coll21', 'utc_p16877coll22',
            'utc_p16877coll23', 'utc_p16877coll24', 'utc_p16877coll25', 'utc_p16877coll26', 'utc_p16877coll27',
            'utc_p16877coll28']
            >>> Repox("http://localhost:8080", "username", "password").get_list_of_sets_from_provider("nashviller0",
            ... True)
            [{'containerType': 'DEFAULT', 'dataSource': {'dataSetType': 'OAI', 'id': 'nr', 'schema':
            'http://www.openarchives.org/OAI/2.0/oai_dc.xsd', 'namespace': 'http://www.openarchives.org/OAI/2.0/',
            'description': "Nashville Public Library's Digital Collections", 'metadataFormat': 'oai_dc', 'isSample':
            False, 'exportDir': '/vhosts/repoxdata/export/nr', 'oaiSourceURL':
            'http://nashville.contentdm.oclc.org/oai/oai.php', 'oaiSet': 'nr', 'recordIdPolicy': {'IdProvided': {}}},
            'nameCode': 'nashvillepublic_nr', 'name': 'Nashville Public Library nr'}, {'containerType': 'DEFAULT',
            'dataSource': {'dataSetType': 'OAI', 'id': 'p15769coll18', 'schema':
            'http://www.openarchives.org/OAI/2.0/oai_dc.xsd', 'namespace': 'http://www.openarchives.org/OAI/2.0/',
            'description': "Nashville's New Faces", 'metadataFormat': 'oai_dc', 'isSample': False, 'exportDir':
            '/vhosts/repoxdata/export/p15769coll18', 'oaiSourceURL': 'http://nashville.contentdm.oclc.org/oai/oai.php',
            'oaiSet': 'p15769coll18', 'recordIdPolicy': {'IdProvided': {}}}, 'nameCode': 'nashvillepublic_p15769coll18',
            'name': 'Nashville Public Library p15769coll18'}, {'containerType': 'DEFAULT', 'dataSource': {'dataSetType':
            'DIR', 'id': 'nash_p15769coll19', 'schema': 'http://worldcat.org/xmlschemas/qdc/1.0/qdc-1.0.xsd',
            'namespace': 'http://worldcat.org/xmlschemas/qdc-1.0', 'description': 'Picturing Nashville in Rotogravure,
            1926-1933', 'metadataFormat': 'oai_qdc', 'isSample': False, 'exportDir':
            '/vhosts/repoxdata/export/nash_p15769coll19', 'marcFormat': '', 'sourcesDirPath':
            '/vhosts/repoxdata/nash_p15769coll19', 'recordXPath': 'oai_qdc:qualifieddc', 'isoVariant': 'STANDARD',
            'recordIdPolicy': {'IdGenerated': {}}, 'retrieveStrategy': {'FOLDER': {}}}, 'nameCode': 'nash_p15769coll19',
            'name': 'nash_p15769coll19'}]

        """
        if verbose is True:
            return requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                auth=(self.username, self.password)).json()
        else:
            data_sets = requests.get(f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                                     auth=(self.username, self.password)).json()
            return [data_set["dataSource"]["id"] for data_set in data_sets]

    def get_dataset_details(self, data_set_id: str) -> dict:
        """Get details about a specific dataset.

        Requires a data_set_id and returns metadata about it as a dict.

        Args:
            data_set_id (str): data_set_id of the dataset you want details about.

        Returns:
            dict: Details about the dataset as a dict.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_dataset_details("nr")
            {'containerType': 'DEFAULT', 'dataSource': {'dataSetType': 'OAI', 'id': 'nr', 'schema':
            'http://www.openarchives.org/OAI/2.0/oai_dc.xsd', 'namespace': 'http://www.openarchives.org/OAI/2.0/',
            'description': "Nashville Public Library's Digital Collections", 'metadataFormat': 'oai_dc', 'isSample':
            False, 'exportDir': '/vhosts/repoxdata/export/nr', 'oaiSourceURL':
            'http://nashville.contentdm.oclc.org/oai/oai.php', 'oaiSet': 'nr', 'recordIdPolicy': {'IdProvided': {}}},
            'nameCode': 'nashvillepublic_nr', 'name': 'Nashville Public Library nr'}"
            >>> Repox("http://localhost:8080", "username", "password").get_dataset_details("cmhf_musicaudio")
            "{'containerType': 'DEFAULT', 'dataSource': {'dataSetType': 'DIR', 'id': 'cmhf_musicaudio', 'schema':
            'http://worldcat.org/xmlschemas/qdc/1.0/qdc-1.0.xsd', 'namespace': 'http://worldcat.org/xmlschemas/qdc-1.0',
            'description': 'cmhf_musicaudio', 'metadataFormat': 'oai_qdc', 'isSample': False, 'exportDir':
            '/vhosts/repoxdata/export/cmhf_musicaudio', 'marcFormat': '', 'sourcesDirPath':
            '/vhosts/repoxdata/cmhf_qdc', 'recordXPath': 'oai_qdc:qualifieddc', 'isoVariant': 'STANDARD',
            'recordIdPolicy': {'IdGenerated': {}}, 'retrieveStrategy': {'FOLDER': {}}}, 'nameCode': 'cmhf_musicaudio',
            'name': 'cmhf_musicaudio'}

        """
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}",
                            auth=(self.username, self.password)).json()

    def get_last_ingest_date_of_set(self, data_set_id: str) -> str:
        """Get the last time a datset was ingested or updated.

        Returns the last ingestion date of a dataset as a string.

        Args:
            data_set_id (str): The data_set_id of the dataset you're querying.

        Returns:
            str: The last ingestion date as a str.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_last_ingest_date_of_set("cmhf_musicaudio")
            "12/14/2018 08:56:32"

        """
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/date",
                            auth=(self.username, self.password)).json()["result"]

    def count_records_in_dataset(self, data_set_id: str) -> str:
        """Get the total number of records in a dataset.

        Returns the total number of records from a dataset as a string.

        Args:
            data_set_id (str): The data_set_id of the dataset you're querying.

        Returns:
            str: The total number of records in a dataset as a str.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").count_records_in_dataset("cmhf_musicaudio")
            "7927"

        """
        return requests.get(f"{self.swagger_endpoint}/datasets/{data_set_id}/count",
                            auth=(self.username, self.password)).json()["result"]

    # TODO Determine which keys are required and which are not and write something to help with unpacking this.
    def create_dataset(self, provider_id: str, metadata: dict) -> int:
        """Create a dataset.

        Takes a provider_id and creates a new dataset in it based on the contents of a metadata dict.

        Args:
            provider_id (str): The provider_id of the provider that you want to add your new dataset to.
            metadata (dict): Metadata about the new dataset you want to create.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> details = {
            ... "containerType": "DEFAULT", "dataSource": { "exportDir": "/home/vagrant", "metadataFormat": "oai_dc",
            ... "marcFormat": "", "recordIdPolicy": { "IdProvided": {} }, "isSample": False, "schema":
            ... "http://www.openarchives.org/OAI/2.0/oai_dc.xsd", "namespace": "http://purl.org/dc/elements/1.1/",
            ... "description": "nashville_test", "id": "nashville_test", "dataSetType": "OAI", "oaiSourceURL":
            ... "https://dpla.lib.utk.edu/repox/OAIHandler", "oaiSet": "p15769coll18" }, "name": "nashville_test",
            ... "nameCode": "nashville_test" }
            >>> Repox("http://localhost:8080", "username", "password").create_dataset("nashville", details)
            201

        """
        return requests.post(f"{self.swagger_endpoint}/datasets?providerId={provider_id}", headers=self.headers,
                             auth=(self.username, self.password), data=json.dumps(metadata)).status_code

    # TODO This returns a 200 even if permissions are wrong. Can we do something about this.
    def export_dataset(self, dataset_id: str) -> int:
        """Exports a metadata records from a dataset to disk.

        Requires a dataset_id and exports the records associated with it to disk based on the value of its exportDir.
        Use update_dataset to modify the value of exportDir.

        Args:
            dataset_id (str): The dataset_id of the dataset you want to export.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").export_dataset("nr")
            200

        """
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}/export", headers=self.headers,
                             auth=(self.username, self.password)).status_code

    def copy_dataset(self, dataset_id: str, new_dataset_id: str) -> int:
        """Make a copy of an existing dataset with a new id.

        Requires the dataset_id of an existing dataset and creates a new dataset in the same provider based on existing
        metadata and the value of new_dataset_id.

        Args:
            dataset_id (str): The dataset_id of the dataset you want to copy.
            new_dataset_id (str): A dataset_id for your new copy of the dataset.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").copy_dataset("nashville_test2",
            ... "nashville_test3")
            201

        """
        return requests.post(f"{self.swagger_endpoint}/datasets/{dataset_id}?newDatasetId={new_dataset_id}",
                             headers=self.headers, auth=(self.username, self.password)).status_code

    # TODO Create similar update methods for other dataset types.
    def update_oai_dataset(self, dataset_id: str, export_dir: str="", metadata_format: str="", description: str="",
                           is_sample: bool=False, oai_url: str="", set_name: str="", name: str="", name_code: str="") \
            -> int:
        """Update an existing oai dataset.

        Requires a dataset_id and optionally accepts most metadata elements for an OAI dataset as a str.  If a metadata
        element is not passed, the value is taken from the previous data.

        Args:
            dataset_id (str): Required. The dataset_id of the dataset being updated.
            export_dir (str): Optional. A new path to export files to on disk.
            metadata_format (str): Optional. A new metadata format for the set.
            description (str): Optional. A new description for the oai set.
            is_sample (bool): Optional. Specify whether the oai set is a sample (False) or all records (True).
            oai_url (str): Optional.  A new url for the associated OAI provider.
            set_name (str): Optional. Change the set_name for the associated OAI provider.
            name (str): Optional. Change the name of the oai set.
            name_code (str): Optional. Change the name_code of the oai_set.

        Returns:
            int: The HTTP status Code of the request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").update_oai_dataset("bcpl",
            ... export_dir="/vagrant/export")
            200

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
        """Delete a dataset.

        Requires the dataset_id and deletes the corresponding dataset.

        Args:
            dataset_id (str): The dataset_id of the dataset you want to delete.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").delete_dataset("nashville_test")
            200

        """
        return requests.delete(f"{self.swagger_endpoint}/datasets/{dataset_id}",
                               auth=(self.username, self.password)).status_code

    @staticmethod
    def __metadata_helper(metadata_format: str) -> dict:
        """Finds matching namespace and schema if known.

        Private method that accepts a metadata format and returns a matching namespace and schema if one exists.

        Args:
            metadata_format (str): The metadata format to match on.

        Returns:
            dict: A dict with schema and namespace if found. If not, returned dict has empty schema and namespace.

        """
        formats = {
            "edm":
                {
                    "schema": "http://www.europeana.eu/schemas/edm/EDM.xsd",
                    "namespace": "http://www.europeana.eu/schemas/edm/",
                },
            "ese":
                {
                    "schema": "http://www.europeana.eu/schemas/ese/ESE-V3.4.xsd",
                    "namespace": "http://www.europeana.eu/schemas/ese/"
                },
            "ISO2709":
                {
                    "schmea": "info:lc/xmlns/marcxchange-v1.xsd",
                    "namespace": "info:lc/xmlns/marcxchange-v1"
                },
            "lido":
                {
                    "schema": "http://www.lido-schema.org/schema/v1.0/lido-v1.0.xsd",
                    "namespace": "http://www.lido-schema.org",
                },
            "MarcXchange":
                {
                    "namespace": "info:lc/xmlns/marcxchange-v1",
                    "schema": "info:lc/xmlns/marcxchange-v1.xsd"
                },
            "mods":
                {
                    "schema": 'http://www.loc.gov/standards/mods/v3/mods-3-5.xsd',
                    "namespace": 'http://www.loc.gov/mods/v3'
                },
            "NLM-AI":
                {
                    "schema": "ncbi-mathml2/mathml2.xsd",
                    "namespace": "http://www.w3.org/1998/Math/MathML"
                },
            "NLM-Book":
                {
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                    "schema": "ncbi-mathml2/mathml2.xsd",
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
                },
            "tel":
                {
                    "schema": "http://www.europeana.eu/schemas/ese/ESE-V3.4.xsd",
                    "namespace": "http://krait.kb.nl/coop/tel/handbook/telterms.html"
                }
        }
        current_format = metadata_format.lower()
        try:
            return {"result": formats[current_format]}
        except KeyError:
            return {"result": {"schema": "", "namespace": ""}}

    # Statistics
    def get_statistics(self) -> dict:
        """Get statistics about an entire Repox instance.

        Returns:
            dict: A dict of statistics.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_statistics()
            '{"repox-statistics": {"@generationDate": "2018-12-27 16:08:02 EST", "dataSourcesIdExtracted": "0",
            "dataSourcesIdGenerated": "11", "dataSourcesIdProvided": "175", "aggregators": "1", "dataProviders": "9",
            "dataSourcesOai": "175", "dataSourcesZ3950": "0", "dataSourcesDirectoryImporter": "11",
            "dataSourcesMetadataFormats": {"dataSourcesMetadataFormat": [{"metadataFormat": "mods", "dataSources": "45",
            "records": "25636"}, {"metadataFormat": "oai_dc", "dataSources": "86", "records": "160203"}, {
            "metadataFormat": "oai_qdc", "dataSources": "55", "records": "30799"}]}, "recordsAvgDataSource":
            "1164.7205", "recordsAvgDataProvider": "24070.889", "countriesRecords": {"countryRecords": [{"@country":
            "al", "records": "100853"}, {"@country": "de", "records": "115785"}]}, "recordsTotal": "216638"}}'

        """
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
