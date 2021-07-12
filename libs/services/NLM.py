from io import StringIO

import pandas as pd

from libs.services.Converter import Converter


class NLM(Converter):
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'NLM': 'https://chem.nlm.nih.gov/api/data/'}

        self.attributes = [{'code': 'casno', 'label': 'RN / ID'},
                           {'code': 'inchikey', 'label': 'InChIKey'},
                           {'code': 'name', 'label': 'Name'},
                           {'code': 'formula', 'label': 'Formula'}]

        # generate top level methods defining allowed conversions
        conversions = [('inchikey', 'name', 'from_inchikey'),
                       ('inchikey', 'formula', 'from_inchikey'),
                       ('inchikey', 'casno', 'from_inchikey'),
                       ('name', 'inchikey', 'from_name'),
                       ('name', 'formula', 'from_name'),
                       ('name', 'casno', 'from_name')]
        self.create_top_level_conversion_methods(conversions)

    async def from_inchikey(self, inchikey):
        """
        Convert InChiKey to all possible attributes using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param inchikey: given InChiKey
        :return: all found data
        """
        args = f'inchikey/equals/{inchikey}?data=summary&format=tsv'
        response = await self.query_the_service('NLM', args)
        if response:
            return self.parse_attributes(response)

    async def from_name(self, name):
        """
        Convert Chemical name to all possible attributes using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param name: given Chemical name
        :return: all found data
        """
        args = f'name/equals/{name}?data=summary&format=tsv'
        response = await self.query_the_service('NLM', args)
        if response:
            return self.parse_attributes(response)

    def parse_attributes(self, response):
        """
        Parse all available attributes obtained from given key.

        :param response: NLM compound response to given given key
        :return: all parsed data
        """
        result = dict()

        if response != 'EXPRESSION_INVALID':
            table = pd.read_csv(StringIO(response), sep='\t')
            if not table.empty:
                for att in self.attributes:
                    value = table[att['label']][0]
                    if type(value) == str:
                        result[att['code']] = value
        return result
