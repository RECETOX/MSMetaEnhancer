from libs.services.Converter import Converter


class CIR(Converter):
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'CIR': 'https://cactus.nci.nih.gov/chemical/structure/'}

    async def cas_to_smiles(self, cas_number):
        """
        Convert CAS number to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param cas_number: given CAS number
        :return: obtained SMILES
        """
        args = f"{cas_number}/smiles?resolver=cas_number"
        response = await self.query_the_service('CIR', args)
        if response:
            return response

    async def inchikey_to_smiles(self, inchikey):
        """
        Convert InChiKey to SMILES using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained SMILES
        """
        args = f'{inchikey}/smiles'
        response = await self.query_the_service('CIR', args)
        if response:
            return response.split('\n')[0]

    async def inchikey_to_inchi(self, inchikey):
        """
        Convert InChiKey to InCHi using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained InCHi
        """
        args = f'{inchikey}/stdinchi'
        response = await self.query_the_service('CIR', args)
        if response:
            return response

    async def inchikey_to_cas(self, inchikey):
        """
        Convert InChiKey to CAS number using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained CAS number
        """
        args = f'{inchikey}/cas'
        response = await self.query_the_service('CIR', args)
        if response:
            return response

    async def inchikey_to_formula(self, inchikey):
        """
        Convert InChiKey to chemical formula using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param inchikey: given InChiKey
        :return: obtained chemical formula
        """
        args = f'{inchikey}/formula'
        response = await self.query_the_service('CIR', args)
        if response:
            return response

    async def smiles_to_inchikey(self, smiles):
        """
        Convert SMILES to InChiKey using CIR web service
        More info: https://cactus.nci.nih.gov/chemical/structure_documentation

        :param smiles: given SMILES
        :return: obtained InChiKey
        """
        args = f'{smiles}/stdinchikey'
        response = await self.query_the_service('CIR', args)
        if response:
            return response[9:]
