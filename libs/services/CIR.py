from libs.services.Converter import Converter


class CIR(Converter):
    def __init__(self):
        super().__init__()
        # service URLs
        self.services = {'CIR': 'https://cactus.nci.nih.gov/chemical/structure/'}

    def cas_to_smiles(self, cas_number):
        """
        Convert CAS number to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param cas_number: given CAS number
        :return: obtained SMILES
        """
        args = f"{cas_number}/smiles?resolver=cas_number"
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text

    def inchikey_to_smiles(self, inchikey):
        """
        Convert InChiKey to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained SMILES
        """
        args = f'{inchikey}/smiles'
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text.split('\n')[0]

    def inchikey_to_inchi(self, inchikey):
        """
        Convert InChiKey to InCHi using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained InCHi
        """
        args = f'{inchikey}/stdinchi'
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text[6:]

    def inchikey_to_cas(self, inchikey):
        """
        Convert InChiKey to CAS number using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained CAS number
        """
        args = f'{inchikey}/cas'
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text

    def inchikey_to_formula(self, inchikey):
        """
        Convert InChiKey to chemical formula using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained chemical formula
        """
        args = f'{inchikey}/formula'
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text

    def smiles_to_inchikey(self, smiles):
        """
        Convert SMILES to InChiKey using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param smiles: given SMILES
        :return: obtained InChiKey
        """
        args = f'{smiles}/stdinchikey'
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text[9:]
