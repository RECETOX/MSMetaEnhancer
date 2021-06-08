import requests


class Converter:
    def __init__(self):
        # service URLs
        self.cts = "https://cts.fiehnlab.ucdavis.edu/rest/convert/"
        self.cir = "https://cactus.nci.nih.gov/chemical/structure/"

    @staticmethod
    def connect_to_service(url):
        """
        Make get request to given URL.
        Returns (None?) if service is not available.

        :param url: given full URL for get request
        :return: obtained response
        """
        try:
            return requests.get(url)
        except requests.exceptions.ConnectionError:
            return None  # TODO improve

    def cas_to_inchikey(self, cas_number):
        """
        Convert CAS number to InChiKey using CTS web service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        The method returns first found hit.

        :param cas_number: given CAS number
        :return: obtained InChiKey
        """
        url = self.cts + "CAS/InChIKey/{}".format(cas_number)
        response = self.connect_to_service(url).json()[0]
        return response['results'][0] if response['results'] else None

    def cas_to_smiles(self, cas_number):
        """
        Convert CAS number to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param cas_number: given CAS number
        :return: obtained SMILES
        """
        url = self.cir + "{}/smiles?resolver=cas_number".format(cas_number)
        response = self.connect_to_service(url)
        return response.text if response.status_code == 200 else None
