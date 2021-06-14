from libs import Converter


class CTS(Converter):
    def __init__(self):
        # service URLs
        self.services = {'CTS': 'https://cts.fiehnlab.ucdavis.edu/rest/convert/',
                         'CTS_compound': 'http://cts.fiehnlab.ucdavis.edu/service/compound/'
                         }

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

    def inchikey_to_inchi(self, inchikey):
        """
        Convert InChiKey to InChi using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained InChi
        """
        args = inchikey
        response = self.connect_to_service('CTS_compound', args)
        if response.status_code == 200:
            return response.json()["inchicode"][6:]

    def name_to_inchikey(self, name):
        """
        Convert Chemical name to InChiKey using CTS service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param name: given Chemical name
        :return: obtained InChiKey
        """
        args = "Chemical%20Name/InChIKey/{}".format(name)
        response = self.connect_to_service('CTS', args)
        if len(response.json()[0]['results']) != 0:
            return response.json()[0]['results'][0]

    def inchikey_to_name(self, inchikey):
        """
        Convert InChiKey to Chemical name using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained Chemical name
        """
        args = inchikey
        response = self.connect_to_service('CTS_compound', args)
        if response.status_code == 200:
            synonyms = response.json()['synonyms']
            names = [item['name'] for item in synonyms if item['type'] == 'Synonym']
            if names:
                return names[0]

    def inchikey_to_IUPAC_name(self, inchikey):
        """
        Convert InChiKey to IUPAC name using CTS compound service
        More info: http://cts.fiehnlab.ucdavis.edu/services

        :param inchikey: given InChiKey value
        :return: obtained IUPAC name
        """
        args = inchikey
        response = self.connect_to_service('CTS_compound', args)
        if response.status_code == 200:
            synonyms = response.json()['synonyms']
            names = [item['name'] for item in synonyms if item['type'] == 'IUPAC Name (Preferred)']
            if names:
                return names[0]
