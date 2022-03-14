from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class CIR(WebConverter):
    """
    Chemical Identifier Resolver allows one to convert a given structure identifier
    into another representation or structure identifier.

    Available online at: https://cactus.nci.nih.gov/chemical/structure

    More info about the available conversions: https://cactus.nci.nih.gov/chemical/structure_documentation
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {'CIR': 'https://cactus.nci.nih.gov/chemical/structure/'}

    async def casno_to_smiles(self, cas_number):
        """
        Convert CAS number to SMILES using CIR web service

        :param cas_number: given CAS number
        :return: obtained SMILES
        """
        args = f'{cas_number}/smiles?resolver=cas_number'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'smiles': self.retrieve_first(response)}

    async def inchikey_to_smiles(self, inchikey):
        """
        Convert InChiKey to SMILES using CIR web service

        :param inchikey: given InChiKey
        :return: obtained SMILES
        """
        args = f'{inchikey}/smiles'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'smiles': self.retrieve_first(response)}

    async def inchikey_to_inchi(self, inchikey):
        """
        Convert InChiKey to InCHi using CIR web service

        :param inchikey: given InChiKey
        :return: obtained InCHi
        """
        args = f'{inchikey}/stdinchi'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'inchi': self.retrieve_first(response)}

    async def inchikey_to_casno(self, inchikey):
        """
        Convert InChiKey to CAS number using CIR web service

        :param inchikey: given InChiKey
        :return: obtained CAS number
        """
        args = f'{inchikey}/cas'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'casno': self.retrieve_first(response)}

    async def inchikey_to_formula(self, inchikey):
        """
        Convert InChiKey to chemical formula using CIR web service

        :param inchikey: given InChiKey
        :return: obtained chemical formula
        """
        args = f'{inchikey}/formula'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'formula': self.retrieve_first(response)}

    async def smiles_to_inchikey(self, smiles):
        """
        Convert SMILES to InChiKey using CIR web service

        :param smiles: given SMILES
        :return: obtained InChiKey
        """
        args = f'{smiles}/stdinchikey'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'inchikey': self.retrieve_first(response)[9:]}

    async def inchi_to_smiles(self, inchi):
        """
        Convert InChi to SMILES using CIR web service

        :param inchi: given InChi
        :return: obtained SMILES
        """
        args = f'{inchi}/smiles'
        response = await self.query_the_service('CIR', args)
        if response:
            return {'smiles': self.retrieve_first(response)}

    @staticmethod
    def retrieve_first(response):
        """
        CIR often returns multiple hits separated by a newline.
        This method takes the first hit only.

        :param response: given response from CIR
        :return: only first hit
        """
        return response.split('\n')[0]
