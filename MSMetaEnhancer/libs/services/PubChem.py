import json

from MSMetaEnhancer.libs.services.Converter import Converter
from frozendict import frozendict


class PubChem(Converter):
    """
    PubChem is the world's largest collection of freely accessible chemical information.

    PubChem service: https://pubchem.ncbi.nlm.nih.gov/
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'}

        self.attributes = [{'code': 'inchi', 'label': 'InChI', 'extra': None},
                           {'code': 'inchikey', 'label': 'InChIKey', 'extra': None},
                           {'code': 'iupac_name', 'label': 'IUPAC Name', 'extra': 'Preferred'},
                           {'code': 'formula', 'label': 'Molecular Formula', 'extra': None},
                           {'code': 'canonical_smiles', 'label': 'SMILES', 'extra': 'Canonical'},
                           {'code': 'isomeric_smiles', 'label': 'SMILES', 'extra': 'Isomeric'}]

        # generate top level methods defining allowed conversions
        conversions = [('compound_name', 'inchi', 'from_name'),
                       ('compound_name', 'inchikey', 'from_name'),
                       ('compound_name', 'iupac_name', 'from_name'),
                       ('compound_name', 'formula', 'from_name'),
                       ('compound_name', 'canonical_smiles', 'from_name'),
                       ('compound_name', 'isomeric_smiles', 'from_name'),
                       ('inchi', 'inchikey', 'from_inchi'),
                       ('inchi', 'iupac_name', 'from_inchi'),
                       ('inchi', 'formula', 'from_inchi'),
                       ('inchi', 'canonical_smiles', 'from_inchi'),
                       ('inchi', 'isomeric_smiles', 'from_inchi')]
        self.create_top_level_conversion_methods(conversions)

    async def from_name(self, name):
        """
        Convert Chemical name to all possible attributes using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param name: given Chemical name
        :return: all found data
        """
        args = f'name/{name}/JSON'
        response = await self.query_the_service('PubChem', args)
        if response:
            return self.parse_attributes(response)

    async def from_inchi(self, inchi):
        """
        Convert InChi to to all possible attributes using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: all found data
        """
        args = "inchi/JSON"
        response = await self.query_the_service('PubChem', args, method='POST', data=frozendict({'inchi': inchi}))
        if response:
            return self.parse_attributes(response)

    def parse_attributes(self, response):
        """
        Parse all available attributes (specified in self.attributes) from given response.

        Method does not return anything, instead stores data in local cache.

        :param response: given JSON
        :return: all parsed data
        """
        response_json = json.loads(response)
        result = dict()

        for prop in response_json['PC_Compounds'][0]['props']:
            label = prop['urn']['label']
            for att in self.attributes:
                if label == att['label']:
                    if att['extra']:
                        if prop['urn']['name'] == att['extra']:
                            result[att['code']] = prop['value']['sval']
                    else:
                        result[att['code']] = prop['value']['sval']
        return result
