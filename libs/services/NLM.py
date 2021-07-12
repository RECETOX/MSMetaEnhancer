from io import StringIO

import pandas as pd

from libs.services.Converter import Converter


class NLM(Converter):
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'NLM': 'https://chem.nlm.nih.gov/api/data/'}

    async def inchikey_to_name(self, inchikey):
        """
        Convert InChiKey to Chemical name using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param inchikey: given InChiKey
        :return: obtained Chemical name
        """
        args = f'inchikey/equals/{inchikey}?data=summary&format=tsv'
        response = await self.query_the_service('NLM', args)
        if response:
            if response != 'EXPRESSION_INVALID':
                table = pd.read_csv(StringIO(response), sep='\t')
                if not table.empty:
                    return table['Name'][0]

    async def name_to_inchikey(self, name):
        """
        Convert Chemical name to InChiKey using NLM service
        More info: https://chem.nlm.nih.gov/chemidplus/inchikey

        :param name: given Chemical name
        :return: obtained InChiKey
        """
        args = f'name/equals/{name}?data=summary&format=tsv'
        response = await self.query_the_service('NLM', args)
        if response:
            table = pd.read_csv(StringIO(response), sep='\t')
            if not table.empty:
                inchikey = table['InChIKey'][0]
                if type(inchikey) == str:
                    return inchikey
