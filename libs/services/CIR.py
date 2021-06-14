from libs import Converter


class CIR(Converter):
    def __init__(self):
        # service URLs
        self.services = {'CIR': 'https://cactus.nci.nih.gov/chemical/structure/'}

    def cas_to_smiles(self, cas_number):
        """
        Convert CAS number to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param cas_number: given CAS number
        :return: obtained SMILES
        """
        args = "{}/smiles?resolver=cas_number".format(cas_number)
        response = self.connect_to_service('CIR', args)
        if response.status_code == 200:
            return response.text
        return None
