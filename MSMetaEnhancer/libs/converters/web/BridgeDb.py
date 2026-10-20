from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class BridgeDb(WebConverter):
    """
    BridgeDb is a framework to map identifiers between various biological databases. These mappings are provided for
    genes, proteins, genetic variants, metabolites, and metabolic reactions

    More info about the available conversions: https://bridgedb.github.io/
    """

    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {
            "BridgeDb": "https://webservice.bridgedb.org/Human/xrefs/",
            "BridgeDbSearch": "https://webservice.bridgedb.org/Human/search/",
        }

        self.codes = {
            "hmdbid": "Ch",
            "pubchemid": "Cpc",
            "chemspiderid": "Cs",
            "wikidataid": "Wd",
            "chebiid": "Ce",
            "keggid": "Ck",
            "casno": "Ca",
            "inchikey": "Ik",
        }
        self.identifiers = {
            "PubChem-compound": "pubchemid",
            "Cpc": "pubchemid",
            "Chemspider": "chemspiderid",
            "Cs": "chemspiderid",
            "ChEBI": "chebiid",
            "Ce": "chebiid",
            "HMDB": "hmdbid",
            "Ch": "hmdbid",
            "Wikidata": "wikidataid",
            "Wd": "wikidataid",
            "KEGG Compound": "keggid",
            "Ck": "keggid",
            "CAS": "casno",
            "Ca": "casno",
            "InChIKey": "inchikey",
            "Ik": "inchikey",
        }

        # generate top level methods defining allowed conversions
        conversion_sources = list(self.codes.keys())
        conversions = [
            (source, target, f"from_{source}")
            for source in conversion_sources
            for target in conversion_sources
            if source != target
        ]
        conversions.extend(
            [
                ("compound_name", target, "from_name")
                for target in conversion_sources
            ]
        )
        self.create_top_level_conversion_methods(conversions)

    async def from_hmdbid(self, hmdbid):
        """
        Convert HMDB ID to all possible IDs using BridgeDb web service

        :param hmdbid: given HMDB ID number
        :return: obtained IDs
        """
        args = f"{self.codes['hmdbid']}/{hmdbid}"
        return await self.call_service(args)

    async def from_pubchemid(self, pubchemid):
        """
        Convert PubChem ID to all possible IDs using BridgeDb web service

        :param pubchemid: given PubChem ID number
        :return: obtained IDs
        """
        args = f"{self.codes['pubchemid']}/{pubchemid}"
        return await self.call_service(args)

    async def from_chemspiderid(self, chemspiderid):
        """
        Convert ChemSpider ID to all possible IDs using BridgeDb web service

        :param chemspiderid: given ChemSpider ID number
        :return: obtained IDs
        """
        args = f"{self.codes['chemspiderid']}/{chemspiderid}"
        return await self.call_service(args)

    async def from_wikidataid(self, wikidataid):
        """
        Convert WikiData ID to all possible IDs using BridgeDb web service

        :param wikidataid: given WikiData ID number
        :return: obtained IDs
        """
        args = f"{self.codes['wikidataid']}/{wikidataid}"
        return await self.call_service(args)

    async def from_chebiid(self, chebiid):
        """
        Convert ChEBI ID to all possible IDs using BridgeDb web service

        :param chebiid: given ChEBI ID number
        :return: obtained IDs
        """
        args = f"{self.codes['chebiid']}/{chebiid}"
        return await self.call_service(args)

    async def from_keggid(self, keggid):
        """
        Convert KEGG ID to all possible IDs using BridgeDb web service

        :param keggid: given KEGG ID number
        :return: obtained IDs
        """
        args = f"{self.codes['keggid']}/{keggid}"
        return await self.call_service(args)

    async def from_casno(self, casno):
        """
        Convert CAS number to all possible IDs using BridgeDb web service

        :param casno: given CAS number
        :return: obtained IDs
        """
        args = f"{self.codes['casno']}/{casno}"
        return await self.call_service(args)

    async def from_inchikey(self, inchikey):
        """
        Convert InChIKey to all possible IDs using BridgeDb web service

        :param inchikey: given InChIKey
        :return: obtained IDs
        """
        args = f"{self.codes['inchikey']}/{inchikey}"
        return await self.call_service(args)

    async def from_name(self, name):
        """
        Search identifiers by compound name using BridgeDb web service

        :param name: given compound name
        :return: obtained IDs
        """
        response = await self.query_the_service("BridgeDbSearch", name)
        if response:
            return self.parse_attributes(response)

    async def call_service(self, args):
        response = await self.query_the_service("BridgeDb", args)
        if response:
            return self.parse_attributes(response)

    def parse_attributes(self, response):
        """
        Parse all available attributes obtained using BridgeDb.

        :param response: BridgeDb response to given ID
        :return: all parsed data
        """
        result = dict()

        lines = response.split("\n")
        for line in lines:
            if line:
                value, identifier = line.split("\t")
                if identifier in self.identifiers.keys():
                    result[self.identifiers[identifier]] = value
        return result
