from libs.services.Converter import Converter


class PubChem(Converter):
    def __init__(self):
        super().__init__()
        # service URLs
        self.services = {'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'}

    def inchi_to_inchikey(self, inchi):
        args = "inchi/JSON"
        response = self.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'InChIKey':
                    return prop['value']['sval']

    def name_to_inchi(self, name):
        args = 'name/{}/JSON'.format(name)
        response = self.connect_to_service('PubChem', args)
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'InChI':
                    return prop['value']['sval']

    def inchi_to_IUPAC_name(self, inchi):
        args = "inchi/JSON"
        response = self.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'IUPAC Name' and prop['urn']['name'] == 'Preferred':
                    return prop['value']['sval']

    def inchi_to_formula(self, inchi):
        args = "inchi/JSON"
        response = self.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'Molecular Formula':
                    return prop['value']['sval']

    def inchi_to_smiles(self, inchi):
        args = "inchi/JSON"
        response = self.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        if response.status_code == 200:
            for prop in response.json()['PC_Compounds'][0]['props']:
                if prop['urn']['label'] == 'SMILES' and prop['urn']['name'] == 'Canonical':
                    return prop['value']['sval']
