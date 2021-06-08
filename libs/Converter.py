import requests


class Converter:
    def __init__(self):
        # service URLs
        self.services = {'CTS': 'https://cts.fiehnlab.ucdavis.edu/rest/convert/',
                         'CIR': 'https://cactus.nci.nih.gov/chemical/structure/'
                         }

    @staticmethod
    def fix_cas_number(cas_number):
        """
        Adds dashes to CAS number.

        :param cas_number: given CAS number without dashes
        :return: CAS number enriched by dashes
        """
        return cas_number[:-3] + "-" + cas_number[-3:-1] + "-" + cas_number[-1]

    def connect_to_service(self, service, args):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :return: obtained response
        """
        try:
            return requests.get(self.services[service] + args)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Service {} is not available'.format(service))

    def cas_to_inchikey(self, cas_number):
        """
        Convert CAS number to InChiKey using CTS web service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        The method returns first found hit.

        :param cas_number: given CAS number
        :return: obtained InChiKey
        """
        args = "CAS/InChIKey/{}".format(cas_number)
        response = self.connect_to_service('CTS', args)
        if len(response.json()[0]['results']) != 0:
            return response.json()[0]['results'][0]
        return None

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
