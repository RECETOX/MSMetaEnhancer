from libs.services.Converter import Converter


class PubChem(Converter):
    def __init__(self):
        super().__init__()
        # service URLs
        self.services = {'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'}

    def name_to_inchi(self, name):
        """
        Convert Chemical name to InChi using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param name: given Chemical name
        :return: found InChi
        """
        args = 'name/{}/JSON'.format(name)
        response = self.connect_to_service('PubChem', args)
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'InChI':
                    return prop['value']['sval']

    def inchi_to_inchikey(self, inchi):
        """
        Convert InChi to InChiKey using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found InChiKey
        """
        props = self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'InChIKey':
                    return prop['value']['sval']

    def inchi_to_IUPAC_name(self, inchi):
        """
        Convert InChi to IUPAC name using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found IUPAC name
        """
        props = self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'IUPAC Name' and prop['urn']['name'] == 'Preferred':
                    return prop['value']['sval']

    def inchi_to_formula(self, inchi):
        """
        Convert InChi to chemical formula using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found chemical formula
        """
        props = self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'Molecular Formula':
                    return prop['value']['sval']

    def inchi_to_smiles(self, inchi):
        """
        Convert InChi to SMILES using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: found SMILES
        """
        props = self.get_props_from_inchi(inchi)
        if props:
            for prop in props:
                if prop['urn']['label'] == 'SMILES' and prop['urn']['name'] == 'Canonical':
                    return prop['value']['sval']

    def get_props_from_inchi(self, inchi):
        """
        General methods to obtain all possible data based on InChi.

        :param inchi: given InChi
        :return: obtained properties associated to the given InChi
        """
        args = "inchi/JSON"
        response = self.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response.status_code == 200:
            return response.json()['PC_Compounds'][0]['props']
