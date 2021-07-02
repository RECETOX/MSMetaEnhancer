import json

from libs.services.Converter import Converter


class CTS(Converter):
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'CTS': 'https://cts.fiehnlab.ucdavis.edu/rest/convert/',
                         'CTS_compound': 'http://cts.fiehnlab.ucdavis.edu/service/compound/'
                         }

    async def cas_to_inchikey(self, cas_number):
        """
        Convert CAS number to InChiKey using CTS web service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        The method returns first found hit.

        :param cas_number: given CAS number
        :return: obtained InChiKey
        """
        args = f'CAS/InChIKey/{cas_number}'
        response = await self.query_the_service('CTS', args)
        if response:
            response_json = json.loads(response)
            if len(response_json[0]['results']) != 0:
                return response_json[0]['results'][0]

    async def inchikey_to_inchi(self, inchikey):
        """
        Convert InChiKey to InChi using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained InChi
        """
        args = inchikey
        response = await self.query_the_service('CTS_compound', args)
        if response:
            response_json = json.loads(response)
            return response_json["inchicode"]

    async def name_to_inchikey(self, name):
        """
        Convert Chemical name to InChiKey using CTS service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param name: given Chemical name
        :return: obtained InChiKey
        """
        args = f'Chemical%20Name/InChIKey/{name}'
        response = await self.query_the_service('CTS', args)
        if response:
            response_json = json.loads(response)
            if len(response_json[0]['results']) != 0:
                return response_json[0]['results'][0]

    async def inchikey_to_name(self, inchikey):
        """
        Convert InChiKey to Chemical name using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained Chemical name
        """
        args = inchikey
        response = await self.query_the_service('CTS_compound', args)
        if response:
            response_json = json.loads(response)
            synonyms = response_json['synonyms']
            names = [item['name'] for item in synonyms if item['type'] == 'Synonym']
            if names:
                return names[0]

    async def inchikey_to_iupac_name(self, inchikey):
        """
        Convert InChiKey to IUPAC name using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained IUPAC name
        """
        args = inchikey
        response = await self.query_the_service('CTS_compound', args)
        if response:
            response_json = json.loads(response)
            synonyms = response_json['synonyms']
            names = [item['name'] for item in synonyms if item['type'] == 'IUPAC Name (Preferred)']
            if names:
                return names[0]
