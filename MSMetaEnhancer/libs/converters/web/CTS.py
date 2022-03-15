import json

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class CTS(WebConverter):
    """
    Chemical Translation WebConverter performs batch conversions of the most common compound identifiers.

    Available online at: http://cts.fiehnlab.ucdavis.edu

    More info about the available conversions: http://cts.fiehnlab.ucdavis.edu/services
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {'CTS': 'https://cts.fiehnlab.ucdavis.edu/rest/convert/',
                          'CTS_compound': 'http://cts.fiehnlab.ucdavis.edu/service/compound/'
                          }

        # generate top level methods defining allowed conversions
        conversions = [('inchikey', 'inchi', 'from_inchikey'),
                       ('inchikey', 'compound_name', 'from_inchikey'),
                       ('inchikey', 'iupac_name', 'from_inchikey')]
        self.create_top_level_conversion_methods(conversions)

    # top level methods defining allowed conversions

    async def casno_to_inchikey(self, cas_number):
        """
        Convert CAS number to InChiKey using CTS web service

        The method returns first found hit.

        :param cas_number: given CAS number
        :return: obtained InChiKey
        """
        args = f'CAS/InChIKey/{cas_number}'
        response = await self.query_the_service('CTS', args)
        if response:
            return self.parse_inchikey(response)

    async def compound_name_to_inchikey(self, name):
        """
        Convert Chemical name to InChiKey using CTS service

        :param name: given Chemical name
        :return: obtained InChiKey
        """
        args = f'Chemical%20Name/InChIKey/{name}'
        response = await self.query_the_service('CTS', args)
        if response:
            return self.parse_inchikey(response)

    async def from_inchikey(self, inchikey):
        """
        Convert InChiKey to all possible attributes using CTS compound service

        :param inchikey: given InChiKey value
        :return: all found data
        """
        args = inchikey
        response = await self.query_the_service('CTS_compound', args)
        if response:
            return self.parse_attributes(response)

    def parse_inchikey(self, response):
        """
        Parse InChiKey attribute obtained from given key.

        :param response: CTS conversion response to given key
        :return: parsed InChiKey
        """
        response_json = json.loads(response)
        if len(response_json[0]['results']) != 0:
            return {'inchikey': response_json[0]['results'][0]}

    def parse_attributes(self, response):
        """
        Parse all available attributes obtained from InChiKey.

        :param response: CTS compound response to given InChiKey
        :return: all parsed data
        """
        response_json = json.loads(response)
        result = dict()

        if 'inchicode' in response_json:
            result['inchi'] = response_json['inchicode']

        if 'formula' in response_json:
            result['formula'] = response_json['formula']

        if 'synonyms' in response_json:
            synonyms = response_json['synonyms']

            names = [item['name'] for item in synonyms if item['type'] == 'Synonym']
            if names:
                result['compound_name'] = names[0]

            names = [item['name'] for item in synonyms if item['type'] == 'IUPAC Name (Preferred)']
            if names:
                result['iupac_name'] = names[0]
        return result
