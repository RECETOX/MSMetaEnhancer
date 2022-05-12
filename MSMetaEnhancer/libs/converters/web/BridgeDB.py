from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class BridgeDB(WebConverter):
    """
    BridgeDb is a framework to map identifiers between various biological databases. These mappings are provided for
    genes, proteins, genetic variants, metabolites, and metabolic reactions

    More info about the available conversions: https://bridgedb.github.io/
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {'BridgeDB': 'https://webservice.bridgedb.org/Human/xrefs/'}

        self.codes = {'hmdbid': 'Ch', 'pubchemid': 'Cpc', 'chemspiderid': 'Cs', 'wikidataid': 'Wd', 'chebiid': 'Ce',
                      'keggid': 'Ck'}
        self.identifiers = {'PubChem-compound': 'pubchemid', 'Chemspider': 'chemspiderid', 'ChEBI': 'chebiid',
                            'HMDB': 'hmdbid', 'Wikidata': 'wikidataid', 'KEGG Compound': 'keggid'}

        # generate top level methods defining allowed conversions
        conversions = [('hmdbid', 'pubchemid', 'from_hmdbid'),
                       ('hmdbid', 'chemspiderid', 'from_hmdbid'),
                       ('hmdbid', 'wikidataid', 'from_hmdbid'),
                       ('hmdbid', 'chebiid', 'from_hmdbid'),
                       ('hmdbid', 'keggid', 'from_hmdbid'),
                       ('pubchemid', 'hmdbid', 'from_pubchemid'),
                       ('pubchemid', 'chemspiderid', 'from_pubchemid'),
                       ('pubchemid', 'wikidataid', 'from_pubchemid'),
                       ('pubchemid', 'chebiid', 'from_pubchemid'),
                       ('pubchemid', 'keggid', 'from_pubchemid'),
                       ('chemspiderid', 'hmdbid', 'from_chemspiderid'),
                       ('chemspiderid', 'pubchemid', 'from_chemspiderid'),
                       ('chemspiderid', 'wikidataid', 'from_chemspiderid'),
                       ('chemspiderid', 'chebiid', 'from_chemspiderid'),
                       ('chemspiderid', 'keggid', 'from_chemspiderid'),
                       ('wikidataid', 'hmdbid', 'from_wikidataid'),
                       ('wikidataid', 'pubchemid', 'from_wikidataid'),
                       ('wikidataid', 'chemspiderid', 'from_wikidataid'),
                       ('wikidataid', 'chebiid', 'from_wikidataid'),
                       ('wikidataid', 'keggid', 'from_wikidataid'),
                       ('chebiid', 'hmdbid', 'from_chebiid'),
                       ('chebiid', 'pubchemid', 'from_chebiid'),
                       ('chebiid', 'chemspiderid', 'from_chebiid'),
                       ('chebiid', 'wikidataid', 'from_chebiid'),
                       ('chebiid', 'keggid', 'from_chebiid'),
                       ('keggid', 'hmdbid', 'from_keggid'),
                       ('keggid', 'pubchemid', 'from_keggid'),
                       ('keggid', 'chemspiderid', 'from_keggid'),
                       ('keggid', 'wikidataid', 'from_keggid'),
                       ('keggid', 'chebiid', 'from_keggid'),
                       ]
        self.create_top_level_conversion_methods(conversions)

    async def from_hmdbid(self, hmdbid):
        """
        Convert HMDB ID to all possible IDs using BridgeDB web service

        :param hmdbid: given HMDB ID number
        :return: obtained IDs
        """
        args = f'{self.codes["hmdbid"]}/{hmdbid}'
        return await self.call_service(args)

    async def from_pubchemid(self, pubchemid):
        """
        Convert PubChem ID to all possible IDs using BridgeDB web service

        :param pubchemid: given PubChem ID number
        :return: obtained IDs
        """
        args = f'{self.codes["pubchemid"]}/{pubchemid}'
        return await self.call_service(args)

    async def from_chemspiderid(self, chemspiderid):
        """
        Convert ChemSpider ID to all possible IDs using BridgeDB web service

        :param chemspiderid: given ChemSpider ID number
        :return: obtained IDs
        """
        args = f'{self.codes["chemspiderid"]}/{chemspiderid}'
        return await self.call_service(args)

    async def from_wikidataid(self, wikidataid):
        """
        Convert WikiData ID to all possible IDs using BridgeDB web service

        :param wikidataid: given WikiData ID number
        :return: obtained IDs
        """
        args = f'{self.codes["wikidataid"]}/{wikidataid}'
        return await self.call_service(args)

    async def from_chebiid(self, chebiid):
        """
        Convert ChEBI ID to all possible IDs using BridgeDB web service

        :param chebiid: given ChEBI ID number
        :return: obtained IDs
        """
        args = f'{self.codes["chebiid"]}/{chebiid}'
        return await self.call_service(args)

    async def from_keggid(self, keggid):
        """
        Convert KEGG ID to all possible IDs using BridgeDB web service

        :param keggid: given KEGG ID number
        :return: obtained IDs
        """
        args = f'{self.codes["keggid"]}/{keggid}'
        return await self.call_service(args)

    async def call_service(self, args):
        response = await self.query_the_service('BridgeDB', args)
        if response:
            return self.parse_attributes(response)

    def parse_attributes(self, response):
        """
        Parse all available attributes obtained using BridgeDB.

        :param response: BridgeDB response to given ID
        :return: all parsed data
        """
        result = dict()

        lines = response.split('\n')
        for line in lines:
            if line:
                value, identifier = line.split('\t')
                if identifier in self.identifiers.keys():
                    result[self.identifiers[identifier]] = value
        return result
