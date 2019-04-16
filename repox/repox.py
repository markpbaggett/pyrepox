import json
import requests
import xmltodict
import arrow
from collections import deque
import operator


class Repox:
    """An object to connect to and perform actions in a Repox instance.

    Attributes:
        swagger_endpoint: A string that represents the base URL of the Repox Swagger API.
        username: The username used to connect to the Swagger API.
        password: The password used to connect to the Swagger API.
        headers: A dict to act as the default HTTP header of a request.

    """

    def __init__(self, repox_url: str, username: str, password: str):
        """Inits Repox with the base URL of your Repox instance and your Swagger username and password.

        Args:
            repox_url (str): The url of your Repox instance.
            username (str): The username used to connect to the Swagger API.
            password (str): The password used to connect to the Swagger API.

        Todo:
            * (markpbaggett) Decide whether swagger_endpoint should include /repox or not.

        """
        self.swagger_endpoint = f"{repox_url}/repox/rest"
        self.username = username
        self.password = password
        self.headers = {"content-type": "application/json"}

    def __repr__(self):
        return f"Repox connection instance based on {self.swagger_endpoint}."

    # Aggregators
    def list_all_aggregators(self, verbose: bool = False) -> list:
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
            return requests.get(
                f"{self.swagger_endpoint}/aggregators",
                auth=(self.username, self.password),
            ).json()
        else:
            aggregators = requests.get(
                f"{self.swagger_endpoint}/aggregators",
                auth=(self.username, self.password),
            ).json()
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
        return requests.get(
            f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
            auth=(self.username, self.password),
        ).json()

    def get_aggregator_options(self) -> dict:
        """Get details from Repox Swagger about all the Aggregator APIs.

        This is a direct implementation of an API from Repox.

        Returns:
            dict: Details about the Aggregator Options.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_aggregator_options()
            {'option': [{'description': '[OPTIONS]Get options over Aggregators.', 'syntax':
            'http://localhost:8080/repox/rest/aggregators'}, {'description': '[GET]Get options over Aggregators.',
            'syntax': 'http://localhost:8080/repox/rest/aggregators/options'}, {'description':
            '[GET]Gets an Aggregator by Id.', 'syntax': 'http://localhost:8080/repox/rest/aggregators/{aggregatorId}'},
            {'description': '[POST]Create an aggregator provided in the body of the post call.', 'syntax':
            'http://localhost:8080/repox/rest/aggregators'}, {'description':
            '[DELETE]Delete an aggregator by specifying the Id.', 'syntax':
            'http://localhost:8080/repox/rest/aggregators/{aggregatorId}'}, {'description':
            '[PUT]Update an aggregator by specifying the Id on the context path.', 'syntax':
            'http://localhost:8080/repox/rest/aggregators/{aggregatorId}'}, {'description':
            '[GET]Get a list of aggregators by specifying a range.', 'syntax':
            'http://localhost:8080/repox/rest/aggregators', 'queryParameter': ['offset', 'number']}]}

        """
        return requests.get(
            f"{self.swagger_endpoint}/aggregators/options",
            auth=(self.username, self.password),
        ).json()

    def create_aggregator(
        self,
        aggregator_id: str,
        aggregator_name: str,
        name_code: str = "",
        homepage: str = "",
    ) -> int:
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
        aggregator_data = {
            "id": aggregator_id,
            "name": aggregator_name,
            "nameCode": name_code,
            "homepage": homepage,
        }
        return requests.post(
            f"{self.swagger_endpoint}/aggregators",
            auth=(self.username, self.password),
            headers=self.headers,
            data=json.dumps(aggregator_data),
        ).status_code

    def update_aggregator(
        self,
        aggregator_id: str,
        aggregator_name: str = "",
        name_code: str = "",
        homepage: str = "",
    ) -> int:
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
        aggregator_data = {
            "id": aggregator_id,
            "name": aggregator_name,
            "nameCode": name_code,
            "homepage": homepage,
        }
        return requests.put(
            f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
            headers=self.headers,
            auth=(self.username, self.password),
            data=json.dumps(aggregator_data),
        ).status_code

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
        return requests.delete(
            f"{self.swagger_endpoint}/aggregators/{aggregator_id}",
            auth=(self.username, self.password),
        ).status_code

    # Providers
    def get_list_of_providers(
        self, aggregator_id: str, verbose: bool = False
    ) -> list:
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
            return requests.get(
                f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                auth=(self.username, self.password),
            ).json()
        else:
            providers = requests.get(
                f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
                auth=(self.username, self.password),
            ).json()
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
        return requests.get(
            f"{self.swagger_endpoint}/providers/{provider_id}",
            auth=(self.username, self.password),
        ).json()

    def create_provider(self, aggregator_id: str, metadata: dict) -> int:
        """Create a provider in a specific aggregator.

        Requires an aggregator_id and adds a new provider based on the contents of a metadata dict.

        Args:
            aggregator_id (str): Required.  The aggregator_id of the aggregator you are adding your provider to.
            metadata (dict): Required.  Key value pairs that describe the provider you are creating.

        Returns:
            int: The HTTP status code of the request.

        Todo:
            * (markpbaggett) Describe the required parts of a metadata dict.
            * (markpbaggett) Add a static method to check the contents of metadata to avoid 400 / 406 status codes.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').create_provider("dltn", {"id": "utc", "name":
            ... "UT Chattanooga", "country": "United States", "countryCode": "", "description":
            ... "OAI Sets from the University of Tennessee, Chattanooga", "nameCode": "utc", "homepage":
            ... "http://cdm16877.contentdm.oclc.org", "providerType": "LIBRARY", "email": "carolyn-runyon@utc.edu"})
            201

        """
        return requests.post(
            f"{self.swagger_endpoint}/providers?aggregatorId={aggregator_id}",
            headers=self.headers,
            auth=(self.username, self.password),
            data=json.dumps(metadata),
        ).status_code

    def update_provider(
        self,
        provider_id: str,
        name: str = "",
        country: str = "",
        country_code: str = "",
        description: str = "",
        name_code: str = "",
        homepage: str = "",
        provider_type: str = "",
        email: str = "",
    ) -> int:
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

        Todo:
            * (markpbaggett) Determine if there is a list of allowed country codes.

        Examples:
            >>> Repox('http://localhost:8080', 'username', 'password').update_provider("UTKr0",
            ... homepage="http://dloai.lib.utk.edu/cgi-bin/XMLFile/dlmodsoai/oai.pl", email="mbagget1@utk.edu")
            200

        """
        old_data = requests.get(
            f"{self.swagger_endpoint}/providers/{provider_id}",
            auth=(self.username, self.password),
        ).json()
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
        elif provider_type not in (
            "ARCHIVE",
            "MUSEUM",
            "LIBRARY",
            "AUDIO_VISUAL_ARCHIVE",
            "RESEARCH_EDUCATIONAL",
            "CROSS_SECTOR",
            "PUBLISHER",
            "PRIVATE",
            "AGGREGATOR",
            "UNKNOWN",
        ):
            provider_type = old_data["providerType"]
        if email == "":
            email = old_data["email"]
        metadata = {
            "id": provider_id,
            "name": name,
            "country": country,
            "countryCode": country_code,
            "description": description,
            "nameCode": name_code,
            "homepage": homepage,
            "providerType": provider_type,
            "email": email,
        }
        return requests.put(
            f"{self.swagger_endpoint}/providers/{provider_id}",
            auth=(self.username, self.password),
            headers=self.headers,
            data=json.dumps(metadata),
        ).status_code

    def assign_provider_to_new_aggregator(
        self, provider_id: str, aggregator_id: str
    ) -> int:
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
        metadata = requests.get(
            f"{self.swagger_endpoint}/providers/{provider_id}",
            auth=(self.username, self.password),
        ).json()
        return requests.put(
            f"{self.swagger_endpoint}/providers/{provider_id}?newAggregatorId={aggregator_id}",
            auth=(self.username, self.password),
            data=json.dumps(metadata),
            headers=self.headers,
        ).status_code

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
        return requests.delete(
            f"{self.swagger_endpoint}/providers/{provider_id}",
            auth=(self.username, self.password),
        ).status_code

    # Sets
    def get_list_of_sets_from_provider(
        self, provider_id: str, verbose: bool = False
    ) -> list:
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
            return requests.get(
                f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                auth=(self.username, self.password),
            ).json()
        else:
            data_sets = requests.get(
                f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
                auth=(self.username, self.password),
            ).json()
            return [data_set["dataSource"]["id"] for data_set in data_sets]

    def get_list_of_sets_from_provider_by_format(
        self, provider_id: str
    ) -> list:
        """Gets a list of sets with the metadata format.

        Requires a provider_id and returns dicts with the id of the set and its format.

        Args:
            provider_id (str): The provider_id of a provider.

        Returns:
            list: A list of provider_ids and formats as dicts.

        Example:
            >>> Repox("http://localhost:8080", "username", "password").get_list_of_sets_from_provider_by_format(
            ... "KnoxPLr0")
            [{'name': 'p15136coll1', 'format': 'oai_dc'}, {'name': 'p15136coll2', 'format': 'oai_dc'}, {'name':
            'p16311coll1', 'format': 'oai_dc'}, {'name': 'p16311coll2', 'format': 'oai_dc'}, {'name': 'p265301coll005',
            'format': 'oai_dc'}, {'name': 'p265301coll7', 'format': 'oai_dc'}, {'name': 'p265301coll9', 'format':
            'oai_dc'}]

        """
        r = requests.get(
            f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
            auth=(self.username, self.password),
        ).json()
        return [
            {
                "name": oai_set["dataSource"]["id"],
                "format": oai_set["dataSource"]["metadataFormat"],
            }
            for oai_set in r
        ]

    def count_records_from_provider(self, provider_id: str) -> int:
        """Counts records from provider.

        Returns the total number of records from a dataset as a string.

        Args:
             provider_id (str): provider_id of the provider you want details about.

        Returns:
            int: The number of records from a provider.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").count_records_from_provider("utc")
            15652
        """
        records = 0
        sets = self.get_list_of_sets_from_provider(provider_id)
        for dataset in sets:
            records += self.count_records_in_dataset(dataset)
        return records

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
            {'containerType': 'DEFAULT', 'dataSource': {'dataSetType': 'DIR', 'id': 'cmhf_musicaudio', 'schema':
            'http://worldcat.org/xmlschemas/qdc/1.0/qdc-1.0.xsd', 'namespace': 'http://worldcat.org/xmlschemas/qdc-1.0',
            'description': 'cmhf_musicaudio', 'metadataFormat': 'oai_qdc', 'isSample': False, 'exportDir':
            '/vhosts/repoxdata/export/cmhf_musicaudio', 'marcFormat': '', 'sourcesDirPath':
            '/vhosts/repoxdata/cmhf_qdc', 'recordXPath': 'oai_qdc:qualifieddc', 'isoVariant': 'STANDARD',
            'recordIdPolicy': {'IdGenerated': {}}, 'retrieveStrategy': {'FOLDER': {}}}, 'nameCode': 'cmhf_musicaudio',
            'name': 'cmhf_musicaudio'}

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/{data_set_id}",
            auth=(self.username, self.password),
        ).json()

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
        return requests.get(
            f"{self.swagger_endpoint}/datasets/{data_set_id}/date",
            auth=(self.username, self.password),
        ).json()["result"]

    def count_records_in_dataset(self, data_set_id: str) -> int:
        """Get the total number of records in a dataset.

        Returns the total number of records from a dataset as a string.

        Args:
            data_set_id (str): The data_set_id of the dataset you're querying.

        Returns:
            str: The total number of records in a dataset as a str.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").count_records_in_dataset("cmhf_musicaudio")
            7927

        """
        return int(
            requests.get(
                f"{self.swagger_endpoint}/datasets/{data_set_id}/count",
                auth=(self.username, self.password),
            ).json()["result"]
        )

    def create_dataset(self, provider_id: str, metadata: dict) -> int:
        """Create a dataset.

        Takes a provider_id and creates a new dataset in it based on the contents of a metadata dict.

        Args:
            provider_id (str): The provider_id of the provider that you want to add your new dataset to.
            metadata (dict): Metadata about the new dataset you want to create.

        Returns:
            int: The HTTP status code of your request.

        Todo:
            * (markpbaggett) Determine which keys are required and which are not and write something to help with
              unpacking this.
            * (markpbaggett) This is all about OAI.  What about other things?  File sets?

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
        return requests.post(
            f"{self.swagger_endpoint}/datasets?providerId={provider_id}",
            headers=self.headers,
            auth=(self.username, self.password),
            data=json.dumps(metadata),
        ).status_code

    def export_dataset(self, dataset_id: str) -> int:
        """Exports a metadata records from a dataset to disk.

        Requires a dataset_id and exports the records associated with it to disk based on the value of its exportDir.
        Use update_dataset to modify the value of exportDir.

        Args:
            dataset_id (str): The dataset_id of the dataset you want to export.

        Returns:
            int: The HTTP status code of your request.

        Todo:
            * (markpbaggett) This returns a 200 even if permissions are wrong. Can we do something about this.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").export_dataset("nr")
            200

        """
        return requests.post(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/export",
            headers=self.headers,
            auth=(self.username, self.password),
        ).status_code

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
        return requests.post(
            f"{self.swagger_endpoint}/datasets/{dataset_id}?newDatasetId={new_dataset_id}",
            headers=self.headers,
            auth=(self.username, self.password),
        ).status_code

    def update_oai_dataset(
        self,
        dataset_id: str,
        export_dir: str = "",
        metadata_format: str = "",
        description: str = "",
        is_sample: bool = False,
        oai_url: str = "",
        set_name: str = "",
        name: str = "",
        name_code: str = "",
    ) -> int:
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

        Todo:
            * (markpbaggett) Create similar update methods for other dataset types.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").update_oai_dataset("bcpl",
            ... export_dir="/vagrant/export")
            200

        """
        old_data = self.get_dataset_details(dataset_id)
        data_source_data = {
            "exportDir": export_dir,
            "description": description,
            "oaiSourceURL": oai_url,
            "isSample": is_sample,
            "oaiSet": set_name,
        }
        if metadata_format != "":
            format_data = self.__metadata_helper(metadata_format)
            if format_data["result"]["schema"] != "":
                data_source_data["schema"] = format_data["result"]["schema"]
                data_source_data["namespace"] = format_data["result"][
                    "namespace"
                ]
                data_source_data["metadataFormat"] = metadata_format
        for k, v in data_source_data.items():
            if v != "":
                old_data["dataSource"][k] = v
        if name != "":
            old_data["name"] = name
        if name_code != "":
            old_data["nameCode"] = name_code
        return requests.put(
            f"{self.swagger_endpoint}/datasets/{dataset_id}",
            headers=self.headers,
            auth=(self.username, self.password),
            data=json.dumps(old_data),
        ).status_code

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
        return requests.delete(
            f"{self.swagger_endpoint}/datasets/{dataset_id}",
            auth=(self.username, self.password),
        ).status_code

    @staticmethod
    def __metadata_helper(metadata_format: str) -> dict:
        """Finds matching namespace and schema if known.

        Private method that accepts a metadata format and returns a matching namespace and schema if one exists.

        Args:
            metadata_format (str): The metadata format to match on.

        Todo:
            * (markpbaggett): Some of this interacts with flat files.  Minimally, I should make it possible to update
              this list of formats and add some error handling for when the specified format is missing.

        Returns:
            dict: A dict with schema and namespace if found. If not, returned dict has empty schema and namespace.

        """
        formats = {
            "edm": {
                "schema": "http://www.europeana.eu/schemas/edm/EDM.xsd",
                "namespace": "http://www.europeana.eu/schemas/edm/",
            },
            "ese": {
                "schema": "http://www.europeana.eu/schemas/ese/ESE-V3.4.xsd",
                "namespace": "http://www.europeana.eu/schemas/ese/",
            },
            "ISO2709": {
                "schmea": "info:lc/xmlns/marcxchange-v1.xsd",
                "namespace": "info:lc/xmlns/marcxchange-v1",
            },
            "lido": {
                "schema": "http://www.lido-schema.org/schema/v1.0/lido-v1.0.xsd",
                "namespace": "http://www.lido-schema.org",
            },
            "MarcXchange": {
                "namespace": "info:lc/xmlns/marcxchange-v1",
                "schema": "info:lc/xmlns/marcxchange-v1.xsd",
            },
            "mods": {
                "schema": "http://www.loc.gov/standards/mods/v3/mods-3-5.xsd",
                "namespace": "http://www.loc.gov/mods/v3",
            },
            "NLM-AI": {
                "schema": "ncbi-mathml2/mathml2.xsd",
                "namespace": "http://www.w3.org/1998/Math/MathML",
            },
            "NLM-Book": {
                "namespace": "http://www.w3.org/1998/Math/MathML",
                "schema": "ncbi-mathml2/mathml2.xsd",
            },
            "oai_dc": {
                "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
                "namespace": "http://www.openarchives.org/OAI/2.0/",
            },
            "oai_qdc": {
                "schema": "http://worldcat.org/xmlschemas/qdc/1.0/qdc-1.0.xsd",
                "namespace": "http://worldcat.org/xmlschemas/qdc-1.0",
            },
            "tel": {
                "schema": "http://www.europeana.eu/schemas/ese/ESE-V3.4.xsd",
                "namespace": "http://krait.kb.nl/coop/tel/handbook/telterms.html",
            },
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
        data = requests.get(
            f"{self.swagger_endpoint}/statistics",
            auth=(self.username, self.password),
        ).json()
        return json.dumps(xmltodict.parse(data["result"]))

    # Harvests
    def get_scheduled_harvests(self, dataset_id: str) -> list:
        """Get currently scheduled harvests for a give dataset.

        Requires a dataset_id and returns a list of scheduled harvests for that dataset.

        Args:
            dataset_id (str): The dataset_id of the dataset you are querying.

        Returns:
            list: A list of scheduled harvests as dicts.

        Todo:
            (markpbaggett): Implement a method to get a list of all scheduled harvests from a particular provider.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_scheduled_harvests("nr")
            [{'taskType': 'SCHEDULED', 'id': 'nr_3', 'frequency': 'WEEKLY', 'xmonths': 1, 'time': '23:45',
            'date': '27/12/2018'}]

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedules",
            auth=(self.username, self.password),
        ).json()

    def get_list_of_scheduled_harvests_by_provider(
        self, provider_id: str
    ) -> list:
        """Get a list of scheduled harvests by provider.

        Requires a provider_id.  Iterates through all datasets and appends its list of schedued harvests if not empty.

        Args:
            provider_id (str): The provider_id of the provider you are querying.

        Returns:
            list: A list of lists of scheduled harvests for each set is harvests are scheduled for any sets.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_list_of_scheduled_harvests_by_provider(
            ... 'utcr0')
            []

        """
        return [
            self.get_scheduled_harvests(dataset)
            for dataset in self.get_list_of_sets_from_provider(provider_id)
            if len(self.get_scheduled_harvests(dataset)) is not 0
        ]

    def get_status_of_harvest(self, dataset_id: str) -> dict:
        """Get status of most recent harvest of a dataset.

        Requires a dataset_id and returns the status of its last harvest.

        Args:
            dataset_id (str): The dataset_id of the dataset you are queryings.

        Returns:
            dict: A dict with a key result with the status of the last harvest.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_status_of_harvest("nr")
            {'result': 'CANCELED'}
            >>> Repox("http://localhost:8080", "username", "password").get_status_of_harvest("nr")
            {'result': 'RUNNING'}
            >>> Repox("http://localhost:8080", "username", "password").get_status_of_harvest("nr")
            {'result': 'OK'}

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/status",
            auth=(self.username, self.password),
        ).json()

    def get_log_of_last_harvest(self, dataset_id: str) -> str:
        """Get the log of the last harvest.

        Requires a dataset_id and returns the log of the last ingest as a string of XML.

        Args:
            dataset_id (str): The dataset_id of the associated dataset.

        Returns:
            str: The log of the last harvest as a str of XML.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_log_of_last_harvest("new_bcpl")
            '\\n<report> \\n  <status>OK</status>  \\n  <dataSetId>new_bcpl</dataSetId>  \\n  <startTime>2018-12-28
            05:00:50</startTime>  \\n  <endTime>2018-12-28 05:00:52</endTime>  \\n  <duration>00:00:01</duration>  \\n
            <records>93</records>  \\n  <deleted>0</deleted>  \\n  <summary> \\n    <info time="2018-12-28 05:00:50 UTC"
            class="pt.utl.ist.oai.OaiDataSource">Starting to import from Data Source with id new_bcpl</info>  \\n
            <info time="2018-12-28 05:00:51 UTC" class="pt.utl.ist.oai.OaiHarvester">Starting OAI Harvest URL:
            https://dpla.lib.utk.edu/repox/OAIHandler - Set:bcpl</info>  \\n    <info time="2018-12-28 05:00:51 UTC"
            class="pt.utl.ist.oai.OaiHarvester">sourceUrl: https://dpla.lib.utk.edu/repox/OAIHandler, sourceSet: bcpl,
            outputBaseDir: /data/repoxData/[temp]OAI-PMH_Requests/-bcpl, fromDateString: null, untilDateString: null,
            metadataFormat: mods</info>  \\n   <info time="2018-12-28 05:00:51 UTC" class="pt.utl.ist.oai.OaiHarvester">
            Harvest finished - number of requests: 1</info>  \\n    <info time="2018-12-28 05:00:51 UTC"
            class="pt.utl.ist.oai.OaiHarvester">Response was an empty list in operation ListRecords (may be invalid set
            or does not exist new records from the last ingest)</info>  \\n    <info time="2018-12-28 05:00:51 UTC"
            class="pt.utl.ist.oai.OaiHarvester">Finished OAI Harvest URL: https://dpla.lib.utk.edu/repox/OAIHandler -
            Set:bcpl</info>  \\n    <info time="2018-12-28 05:00:52 UTC" class="pt.utl.ist.oai.ResponseTransformer">
            Starting to split OAI-PMH request to Record Files</info>  \\n    <info time="2018-12-28 05:00:52 UTC"
            class="pt.utl.ist.oai.ResponseTransformer">Finished splitting OAI-PMH request to List</info>  \\n
            <info time="2018-12-28 05:00:52 UTC" class="pt.utl.ist.oai.OaiDataSource">Ingest Process ended. Exiting.
            </info>  \\n    <info time="2018-12-28 05:00:52 UTC" class="pt.utl.ist.oai.OaiDataSource">Finished importing
            from Data Source with id new_bcpl. Exit status: OK</info> \\n  </summary> \\n</report>'

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/log",
            auth=(self.username, self.password),
        ).json()["result"]

    def get_list_of_running_harvests(self) -> str:
        """Returns a message about currently running harvests.

        Todo:
            * (markpbaggett) This seems to always return a 405 status code: method not allowed for the requested
              resource. Find out why.

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/harvest",
            auth=(self.username, self.password),
        ).text

    def harvest_set(self, dataset_id: str, is_sample: bool = False) -> int:
        """Harvest a dataset.

        Requires a dataset_id and optionally accepts an is_sample parameter and triggers a harvest of the specified
        dataset.

        Args:
            dataset_id (str): Required. The dataset_id associated with a dataset.
            is_sample (bool): Optional. Specify whether to harvest the full set or just a sample.

        Returns:
            int: The HTTP status code of your request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_status_of_harvest("new_bcpl")
            200

        """
        if is_sample is False:
            harvest_type = "full"
        else:
            harvest_type = "sample"
        return requests.post(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/start?type={harvest_type}",
            auth=(self.username, self.password),
        ).status_code

    def schedule_harvest(
        self,
        dataset_id: str,
        frequency: str = "ONCE",
        time: str = "NOT SET",
        date: str = "NOT SET",
        xmonths: int = 0,
        incremental: bool = False,
    ) -> int:
        """Schedule a future harvest.

        Requires a dataset_id and schedules a future harvest. Optionally takes arguments for frequency of the harvest,
        the time of the harvest, and the date of the first harvest.

        Args:
            dataset_id (str): Required. The dataset_id of the set to harvest
            frequency (str): Optional. The frequency of the harvest. Defaults to ONCE. Other options: DAILY, WEEKLY,
                XMONTHLY. Note, if XMONTHLY, also define xmonthly.
            time (str): Optional. Time of day of the harvest. If not set, schedules harvest for 15 minutes from now.
            date (str): Optional. Date of first harvest. If not set, schedules harvest for 15 minutes from now.
            xmonths (int): Optional. If frequency is XMONTHLY, how frequent to perform harvest. Defaults to 1.
            incremental (bool): Optional. Defaults to False.

        Returns:
            int: the HTTP status code as the request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").schedule_harvest("bcpl")
            201
            >>> Repox("http://localhost:8080", "username", "password").schedule_harvest("bcpl", frequency="XMONTHLY",
            ... xmonths=2, time="01:00", date="01/12/2019")
            201

        """
        if time == "NOT SET" or date == "NOT SET":
            now = arrow.utcnow().to("local")
            if time == "NOT SET":
                time = now.shift(minutes=15).format("HH:mm")
            if date == "NOT SET":
                date = now.format("DD/MM/YYYY")
        if frequency == "XMONTHLY" and xmonths == 0:
            xmonths = 1
        metadata = {
            "taskType": "SCHEDULED",
            "id": "",
            "frequency": frequency,
            "xmonths": xmonths,
            "time": time,
            "date": date,
        }
        return requests.post(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedule?incremental="
            f"{str(incremental).lower()}",
            headers=self.headers,
            data=json.dumps(metadata),
            auth=(self.username, self.password),
        ).status_code

    def schedule_weekly_harvest(
        self, dataset_id: str, day_of_week: str, time: str = "Not Set"
    ) -> int:
        """Schedule a weekly harvest for a set on a specific day of the week.

        Requires a dataset_id and a day_of_week and schedules a recurring harvest of a specific set each week.

        Args:
            dataset_id (str): Required. The dataset_id of the associated dataset.
            day_of_week (str): Required. The day of the week of the week of the harvest.
            time (str): Optional.  The time of day to schedule the harvest.  Defaults to 15 minutes from now.

        Returns:
            int:  The HTTP status code of the request

        Examples:
            >>> Repox("http://localhost:8080", "admin", "admin").schedule_weekly_harvest("nr", "Sunday")
            201
            >>> Repox("http://localhost:8080", "admin", "admin").schedule_weekly_harvest("nr", "Sunday", time="04:00")
            201
            >>> Repox("http://localhost:8080", "admin", "admin").schedule_weekly_harvest("nr", "Tomorrow")
            500

        """
        days_of_week = deque(
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
        )
        if day_of_week not in days_of_week:
            return 500
        now = arrow.utcnow().to("local")
        today = days_of_week.index(now.format("dddd"))
        days_of_week.rotate(-today)
        shift_time = days_of_week.index(day_of_week)
        if shift_time == 0:
            shift_time = 7
        if time == "Not Set":
            time = now.shift(minutes=15).format("HH:mm")
        metadata = {
            "taskType": "SCHEDULED",
            "id": "",
            "frequency": "WEEKLY",
            "xmonths": 0,
            "time": time,
            "date": now.shift(days=shift_time).format("DD/MM/YYYY"),
        }
        return requests.post(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedule?incremental=false",
            headers=self.headers,
            data=json.dumps(metadata),
            auth=(self.username, self.password),
        ).status_code

    def cancel_running_harvest(self, dataset_id: str) -> int:
        """Cancel a running harvest.

        Requires the dataset_id and cancels the associated harvest if it is running. Returns a 404 if its not running.

        Args:
            dataset_id (str): The dataset_id of the associated dataset.

        Returns:
            int: The HTTP status code of the request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").cancel_running_harvest("nr")
            200
            >>> Repox("http://localhost:8080", "username", "password").cancel_running_harvest("nr")
            404

        """
        return requests.delete(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/cancel",
            auth=(self.username, self.password),
        ).status_code

    def delete_automatic_harvesting_task(
        self, dataset_id: str, task_id: str
    ) -> int:
        """Delete an automatic harvesting task.

        Requires the dataset_id of the set and the task_id related to the scheduled task and deletes it.

        Args:
            dataset_id (str): The dataset_id of the associated dataset.
            task_id (str): The task_id of the associated task.

        Returns:
            int: The HTTP status code of a request.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").delete_automatic_harvesting_task("nr", "nr_3")
            200

        """
        return requests.delete(
            f"{self.swagger_endpoint}/datasets/{dataset_id}/harvest/schedules/{task_id}",
            auth=(self.username, self.password),
        ).status_code

    def get_options_for_harvests(self) -> dict:
        """Get details from Repox Swagger about all the Harvest APIs.

        This is a direct implementation of an API from Repox.

        Returns:
            dict: Details about Harvest APIs.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_options_for_harvests()
            {'option': [{'description': '[OPTIONS]Get options over dataset.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/harvest'}, {'description': '[GET]Get options over dataset.',
            'syntax': 'http://localhost:8080/repox/rest/datasets/harvest/options'}, {'description':
            '[POST]Initiates a new harvest of the dataset with id.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/start', 'queryParameter': ['type']},
            {'description': '[DELETE]Cancels a harvesting ingest.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/cancel'}, {'description':
            '[POST]Schedules an automatic harvesting.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/schedule', 'queryParameter':
            ['incremental']}, {'description': '[GET]Retrieves the list of schedules.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/schedules'}, {'description':
            '[DELETE]Deletes an automatic harvesting.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/schedules/{taskId}'}, {'description':
            '[GET]Gets the status of a specific dataset harvesting.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/status'}, {'description':
            '[GET]Gets the logs of the last ingest.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/{datasetId}/harvest/log'}, {'description':
            '[GET]Gets a list of currently executing dataset harvests.', 'syntax':
            'http://localhost:8080/repox/rest/datasets/harvests'}]}

        """
        return requests.get(
            f"{self.swagger_endpoint}/datasets/harvest/options",
            auth=(self.username, self.password),
        ).json()

    # Mappings
    def get_options_for_mappings(self) -> dict:
        """Get details from Repox Swagger about all the Mappings APIs.

        This is a direct implementation of an API from Repox.

        Returns:
            dict:  Details about Mappings APIs.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_options_for_mappings()
            {'option': [{'description': '[OPTIONS]Get options over mappings.', 'syntax':
            'http://localhost:8080/repox/rest/mappings'}, {'description': '[GET]Get options over mappings.', 'syntax':
            'http://localhost:8080/repox/rest/mappings/options'}, {'description':
            '[POST]Create a new mapping - XSL file through HTTP POST.', 'syntax':
            'http://localhost:8080/repox/rest/mappings'}, {'description': '[GET]Retrieve a mapping.', 'syntax':
            'http://localhost:8080/repox/rest/mappings/mappingId'}, {'description': '[PUT]Update a mapping.', 'syntax':
            'http://localhost:8080/repox/rest/mappings/mappingId'}, {'description': '[DELETE]Delete a mapping.',
            'syntax': 'http://localhost:8080/repox/rest/mappings/mappingId'}]}

        """
        return requests.get(
            f"{self.swagger_endpoint}/mappings/options",
            auth=(self.username, self.password),
        ).json()

    def get_options_for_records(self) -> dict:
        """Get details from Repox Swagger about all the Records APIs.

        This is a direct implementation of an API from Repox.

        Returns:
            dict:  Details about Records APIs.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_options_for_records()
            {'option': [{'description': '[OPTIONS]Get options over Records.', 'syntax':
            'http://localhost:8080/repox/rest/records'}, {'description': '[GET]Get options over Records.', 'syntax':
            'http://localhost:8080/repox/rest/records/options'}, {'description':
            '[GET]Retrieve the record with the provided id.', 'syntax': 'http://localhost:8080/repox/rest/records',
            'queryParameter': ['recordId']}, {'description': '[DELETE]Deletes (mark) or permanently erase a record.',
            'syntax': 'http://localhost:8080/repox/rest/records', 'queryParameter': ['recordId', 'type']},
            {'description': '[POST]Create a new record.', 'syntax': 'http://localhost:8080/repox/rest/records',
            'queryParameter': ['datasetId', 'recordId']}]}

        """
        return requests.get(
            f"{self.swagger_endpoint}/records/options",
            auth=(self.username, self.password),
        ).json()

    def get_record(self, record_id: str) -> str:
        """Get a specific record.

        Requires an OAI id from //record/header/identifier and returns the value of //record/metadata
        as a string if it exists. If there is no metadata xpath, an exception is thrown and an error string is returned.

        Args:
            record_id (str): The OAI identifier from //record/header/identifier

        Returns:
            str: The value of //record/metadata if it exists.  If not, an error string.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_record(
            ... "oai:dltn.repox.test.new_bcpl:urn:dpla.lib.utk.edu.bcpl:bcpl_123")
            '\\n<mods xmlns="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            version="3.5" xsi:schemaLocation="http://www.loc.gov/mods/v3
            http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">  \\n  <identifier type="local">bcpl_00775</identifier>
            \\n  <titleInfo> \\n    <title>Macklin Kerr House (NR)</title> \\n  </titleInfo>  \\n
            <typeOfResource>still image</typeOfResource>  \\n  <originInfo> \\n    <dateCreated>1847</dateCreated>  \\n
            <dateCreated encoding="edtf" keyDate="yes">1847</dateCreated> \\n  </originInfo>  \\n  <physicalDescription>
            \\n    <form authority="aat" valueURI="http://vocab.getty.edu/aat/300046300">photographs</form>  \\n
            <digitalOrigin>reformatted digital</digitalOrigin> \\n  </physicalDescription>  \\n  <abstract>Architectural
            -- two story brick with frame side and rear additions; built 1847</abstract>  \\n  <abstract>Historical --
            site of Gen. O. O. Howard\'s headquarters during the Federal Army\'s visit to Blount County, December 1863.
            </abstract>  \\n  <language> \\n    <languageTerm authority="iso639-2b" type="code">zxx</languageTerm> \\n
            </language>  \\n  <note>This structure appears on the National Historical Registry.</note>  \\n
            <note>Ownership: Private; Current Use: Residence</note>  \\n  <note>Address: Big Gully Rd., 0.3 mi. N. of
            Kyker Rd., Maryville, TN</note>  \\n  <location> \\n    <physicalLocation>Blount County Public Library
            </physicalLocation>  \\n    <url access="object in context" usage="primary display">
            https://digital.lib.utk.edu/collections/islandora/object/bcpl%3A123</url>  \\n    <url access="preview">
            https://digital.lib.utk.edu/collections/islandora/object/bcpl%3A123/datastream/TN/view</url> \\n </location>
            \\n  <subject authority="lcsh" valueURI="http://id.loc.gov/authorities/subjects/sh85061097"> \\n
            <topic>Historic buildings</topic> \\n  </subject>  \\n  <subject> \\n    <geographic authority="naf"
            valueURI="http://id.loc.gov/authorities/names/n81025935">Blount County (Tenn.)</geographic>  \\n
            <cartographics> \\n      <coordinates>35.68724, -83.92553</coordinates> \\n    </cartographics> \\n
            </subject>\\n  <subject> \\n    <hierarchicalGeographic> \\n      <country>United States</country>  \\n
            <state>Tennessee</state>  \\n      <city>Maryville</city>  \\n      <citySection>Street: Big Gully Road, 0.3
            mile North of Kyker Road</citySection> \\n    </hierarchicalGeographic> \\n  </subject>  \\n
            <relatedItem displayLabel="Project" type="host"> \\n    <titleInfo> \\n      <title>Blount County Historical
            and Architectural Inventory</title> \\n    </titleInfo> \\n  </relatedItem> \\n <accessCondition type="local
            rights statement">Digital Image Copyright (c) 2004. Blount County Public Library, Maryville, TN. All Rights
            Reserved. For permission to use, contact: Reference Department, Blount County Public Library, 508 N. Cusick
            Street, Maryville, TN 37804 (865-982-0982).</accessCondition>  \\n  <recordInfo> \\n    <recordIdentifier>
            record_bcpl_00775</recordIdentifier>  \\n    <recordContentSource>University of Tennessee, Knoxville
            Libraries</recordContentSource>  \\n    <languageOfCataloging> \\n      <languageTerm authority="iso639-2b"
            type="code">eng</languageTerm> \\n    </languageOfCataloging>  \\n    <recordOrigin>Created and edited in
            general conformance to MODS Guidelines (Version 3.5).</recordOrigin> \\n  </recordInfo> \\n</mods>'
            >>> Repox("http://localhost:8080", "username", "password").get_record(
            ... "urn:dpla.lib.utk.edu.p16877coll1:oai:cdm16877.contentdm.oclc.org:p16877coll1/17")
            "REPOX Error: This is a generic error and is thrown when Repox can't find a matching metadata.
            This can be caused by an OAI record with the status of deleted."

        """
        try:
            return requests.get(
                f"{self.swagger_endpoint}/records?recordId={record_id}",
                auth=(self.username, self.password),
            ).json()["result"]
        except json.decoder.JSONDecodeError:
            return (
                "REPOX Error: This is a generic error and is thrown when Repox can't find a matching metadata.  "
                "This can be caused by an OAI record with the status of deleted."
            )

    def delete_record(self, record_id: str) -> int:
        """Accepts a record id and deletes the corresponding record.

        Args:
            * record_id (str): a record_id of a record based on OAI_PMH.

        Returns:
            * int: The HTTP status code of the request.

        Todo:
            * (markpbaggett) While this returns a 200, it does not seem to do anything.
              Post an issue in Repox GitHub repo about this.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").delete_record(
            ... "urn:dpla.lib.utk.edu.p16877coll1:oai:cdm16877.contentdm.oclc.org:p16877coll1/17")
            200

        """
        return requests.get(
            f"{self.swagger_endpoint}/records?recordId={record_id}&type=delete",
            auth=(self.username, self.password),
        ).status_code

    def add_a_record(
        self, dataset_id: str, record_id: str, xml_record: str
    ) -> int:
        """Add a record to a set.

        Todo:
            * (markpbaggett) Although this follows the API docs, this doesn't seem to do anything.

        """
        return requests.post(
            f"{self.swagger_endpoint}/records?datasetId={dataset_id}&recordId={record_id}",
            auth=(self.username, self.password),
            headers="application/xml",
            data=xml_record,
        ).status_code

    def get_mapping_details(self, mapping_id: str) -> dict:
        """Returns metadata about a mapping as a dict.

        Requires the mapping_id of a mapping and returns metadata about it as a dict.

        Args:
            mapping_id (str): The mapping_id of a mapping.

        Returns:
            dict:  Metadata about the mapping.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_mapping_details("UTKMODSrepaired")
            {'id': 'UTKMODSrepaired', 'description': 'UTK MODS modified for DLTN MODS', 'sourceSchemaId': 'oai_mods',
            'destinationSchemaId': 'MODS', 'stylesheet': 'utkmodstomods.xsl', 'sourceSchemaVersion': '3.5',
            'versionTwo': True}

        """
        return requests.get(
            f"{self.swagger_endpoint}/mappings/{mapping_id}",
            auth=(self.username, self.password),
        ).json()

    def add_mapping(self, metadata: dict) -> int:
        """ Add a mapping.

        Todo:
            * (markpbaggett) This still needs to be implemented.  See note from Simon:
              https://github.com/europeana/REPOX/issues/40

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
        return requests.post(
            f"{self.swagger_endpoint}/mappings",
            auth=(self.username, self.password),
            headers="application/xml",
            data=metadata,
        ).status_code

    def get_recently_ingested_sets_by_provider(
        self, provider_id: str, since: str = "YYYY-MM-DD"
    ) -> list:
        """ Get an ordered list of recently updated sets as a list of tuples.

        Args:
            provider_id (str): Required. The id of the aggregator you want
            since (str): Optional.  Date of last ingest

        Returns:
            list: A list of tuples with dataset_id and date of last ingest.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_recently_ingested_sets_by_provider('utcr0')
            [('utc_p16877coll30', '03/18/2019 10:25:49'), ('utc_p16877coll29', '03/18/2019 10:25:19'), ('p16877coll9',
            '03/13/2019 12:08:51'), ('utc_p16877coll28', '03/13/2019 11:49:51'), ('utc_p16877coll27',
            '03/13/2019 11:47:51'), ('utc_p16877coll26', '03/13/2019 11:46:06'), ('utc_p16877coll25',
            '03/13/2019 11:45:06'), ('utc_p16877coll24', '03/13/2019 11:38:06'), ('utc_p16877coll23',
            '03/13/2019 11:36:21'), ('utc_p16877coll15', '03/13/2019 11:30:21'), ('utc_p16877coll22',
            '03/13/2019 11:20:06'), ('utc_p16877coll21', '03/13/2019 11:17:36'), ('utc_p16877coll20',
            '03/13/2019 11:16:06'), ('utc_p16877coll19', '03/13/2019 11:13:06'), ('utc_p16877coll18',
            '03/13/2019 11:10:21'), ('utc_p16877coll17', '03/13/2019 11:09:21'), ('utc_p16877coll16',
            '03/13/2019 11:05:36'), ('utc_p16877coll14', '03/13/2019 10:59:21'), ('utc_p16877coll13',
            '03/13/2019 10:57:51'), ('utc_p16877coll12', '03/13/2019 10:56:51'), ('utc_p16877coll11',
            '03/13/2019 10:54:51'), ('utc_p16877coll10', '03/13/2019 10:53:21'), ('p16877coll8',
            '03/13/2019 10:51:06'), ('p16877coll7', '03/13/2019 10:49:51'), ('p16877coll6', '03/13/2019 10:44:51'),
            ('p16877coll5', '03/13/2019 10:43:36'), ('p16877coll4', '03/13/2019 10:31:06'), ('p16877coll3',
            '03/13/2019 10:28:36'), ('p16877coll2', '03/13/2019 10:25:36'), ('p16877coll1', '03/13/2019 10:20:51'),
            ('utc_p16877coll31', '03/07/2019 08:19:45')]
            >>> Repox("http://localhost:8080", "username", "password").get_recently_ingested_sets_by_provider('utcr0',
            ... '2019-03-14')
            [('utc_p16877coll30', '03/18/2019 10:25:49'), ('utc_p16877coll29', '03/18/2019 10:25:19')]

        """
        datasets = self.get_list_of_sets_from_provider(provider_id)
        datasets_by_date = []
        for dataset in datasets:
            if since != "YYYY-MM-DD":
                since = arrow.get(since, "YYYY-MM-DD").format("YYYY-MM-DD")
                try:
                    if (
                        arrow.get(
                            self.get_last_ingest_date_of_set(dataset),
                            "MM/DD/YYYY",
                        ).format("YYYY-MM-DD")
                        > since
                    ):
                        datasets_by_date.append(
                            (
                                dataset,
                                self.get_last_ingest_date_of_set(dataset),
                            )
                        )
                except arrow.parser.ParserError:
                    pass
            else:
                datasets_by_date.append(
                    (dataset, self.get_last_ingest_date_of_set(dataset))
                )
        datasets_by_date.sort(key=operator.itemgetter(1), reverse=True)
        return datasets_by_date

    def get_recently_ingested_sets_by_aggregator(
        self, aggregator_id: str, since: str = "YYYY-MM-DD"
    ):
        """Returns a list of tuples ordered by date of last ingest with dataset_id

         Requires an aggregator_id and optionally takes a date as the since parameter.  Returns a list of datasets as
         tuples with date of last ingest based on the since parameter.

         Args:
             aggregator_id (str): Requrired. The aggregator_id to search providers for.
             since (str): Optional.  A date in YYYY-MM-DD format to limit results by.

        Returns:
            list: A list of datasets and last ingest dates as tuples ordered by date of last ingest.

        Examples:
            >>> Repox("http://localhost:8080", "username", "password").get_recently_ingested_sets_by_aggregator(
            ... 'TNDPLAr0', '2019-03-01')
            [('utk_volvoices', '03/18/2019 10:53:05'), ('utc_p16877coll30', '03/18/2019 10:25:49'), ('utc_p16877coll29',
             '03/18/2019 10:25:19'), ('utk_cdf', '03/18/2019 09:54:49'), ('utk_agrtfhs', '03/18/2019 08:55:49'),
             ('p16877coll9', '03/13/2019 12:08:51'), ('utc_p16877coll28', '03/13/2019 11:49:51'), ('utc_p16877coll27',
             '03/13/2019 11:47:51'), ('utc_p16877coll26', '03/13/2019 11:46:06'), ('utc_p16877coll25',
             '03/13/2019 11:45:06'), ('utc_p16877coll24', '03/13/2019 11:38:06'), ('utc_p16877coll23',
             '03/13/2019 11:36:21'), ('utc_p16877coll15', '03/13/2019 11:30:21'), ('utc_p16877coll22',
             '03/13/2019 11:20:06'), ('utc_p16877coll21', '03/13/2019 11:17:36'), ('utc_p16877coll20',
             '03/13/2019 11:16:06'), ('utc_p16877coll19', '03/13/2019 11:13:06'), ('utc_p16877coll18',
             '03/13/2019 11:10:21'), ('utc_p16877coll17', '03/13/2019 11:09:21'), ('utc_p16877coll16',
             '03/13/2019 11:05:36'), ('utc_p16877coll14', '03/13/2019 10:59:21'), ('utc_p16877coll13',
             '03/13/2019 10:57:51'), ('utc_p16877coll12', '03/13/2019 10:56:51'), ('utc_p16877coll11',
             '03/13/2019 10:54:51'), ('utc_p16877coll10', '03/13/2019 10:53:21'), ('p16877coll8',
             '03/13/2019 10:51:06'), ('p16877coll7', '03/13/2019 10:49:51'), ('p16877coll6', '03/13/2019 10:44:51'),
             ('p16877coll5', '03/13/2019 10:43:36'), ('p16877coll4', '03/13/2019 10:31:06'), ('p16877coll3',
             '03/13/2019 10:28:36'), ('p16877coll2', '03/13/2019 10:25:36'), ('p16877coll1', '03/13/2019 10:20:51'),
             ('p15138coll33', '03/12/2019 11:49:30'), ('rhodes_farnsworth', '03/12/2019 11:43:45'), ('rhodes_sternberg',
              '03/12/2019 11:43:30'), ('utk_emancip', '03/07/2019 11:11:16'), ('utk_druid', '03/07/2019 10:17:31'),
              ('utk_indtruth', '03/07/2019 10:13:46'), ('utk_brehm', '03/07/2019 10:03:46'), ('utk_phoenix',
              '03/07/2019 09:18:31'), ('utk_3d', '03/07/2019 09:01:00'), ('utk_vanvactor', '03/07/2019 08:37:00'),
              ('utc_p16877coll31', '03/07/2019 08:19:45'), ('utk_wderfilms', '03/05/2019 09:21:24')]

        """
        providers = self.get_list_of_providers(aggregator_id)
        all_sets = []
        for provider in providers:
            provider_sets = self.get_recently_ingested_sets_by_provider(
                provider, since
            )
            for dataset in provider_sets:
                all_sets.append(dataset)
        all_sets.sort(key=operator.itemgetter(1), reverse=True)
        return all_sets
