from io import StringIO
import pandas as pd

from libs import Converter


class NIH(Converter):
    def __init__(self):
        # service URLs
        self.services = {'NLM': 'https://chem.nlm.nih.gov/api/data/'}

    def inchikey_to_name(self, inchikey):
        """
        Convert InChiKey to Chemical name using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param inchikey: given InChiKey
        :return: obtained Chemical name
        """
        args = 'inchikey/equals/{}?data=summary&format=tsv'.format(inchikey)
        response = self.connect_to_service('NLM', args)
        table = pd.read_csv(StringIO(response.text), sep='\t')
        if not table.empty:
            return table['Name'][0]

    def name_to_inchikey(self, name):
        """
        Convert Chemical name to InChiKey using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param name: given Chemical name
        :return: obtained InChiKey
        """
        args = 'name/equals/{}?data=summary&format=tsv'.format(name)
        response = self.connect_to_service('NLM', args)
        table = pd.read_csv(StringIO(response.text), sep='\t')
        if not table.empty:
            return table['InChIKey'][0]
