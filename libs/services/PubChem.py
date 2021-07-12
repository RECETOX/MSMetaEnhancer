import json

from libs.services.Converter import Converter


class PubChem(Converter):
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'}

    async def name_to_inchi(self, name):
        """
        Convert Chemical name to InChi using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param name: given Chemical name
        :return: found InChi
        """
        args = f'name/{name}/JSON'
        response = await self.query_the_service('PubChem', args)
        if response:
            response_json = json.loads(response)
            for prop in response_json['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'InChI':
                    return prop['value']['sval']

    async def inchi_to_inchikey(self, inchi):
        """
        Convert InChi to InChiKey using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found InChiKey
        """
        props = await self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'InChIKey':
                    return prop['value']['sval']

    async def inchi_to_iupac_name(self, inchi):
        """
        Convert InChi to IUPAC name using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found IUPAC name
        """
        props = await self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'IUPAC Name' and prop['urn']['name'] == 'Preferred':
                    return prop['value']['sval']

    async def inchi_to_formula(self, inchi):
        """
        Convert InChi to chemical formula using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found chemical formula
        """
        props = await self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'Molecular Formula':
                    return prop['value']['sval']

    async def inchi_to_smiles(self, inchi):
        """
        Convert InChi to SMILES using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found SMILES
        """
        props = await self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'SMILES' and prop['urn']['name'] == 'Canonical':
                    return prop['value']['sval']

    async def get_props_from_inchi(self, inchi):
        """
        General methods to obtain all possible data based on InChi.

        :param inchi: given InChi
        :return: obtained properties associated to the given InChi
        """
        args = "inchi/JSON"
        response = await self.query_the_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response:
            response_json = json.loads(response)
            return response_json['PC_Compounds'][0]['props']
