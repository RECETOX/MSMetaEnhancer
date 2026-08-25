import json

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class ChEBI(WebConverter):
    """
    ChEBI (Chemical Entities of Biological Interest) is a freely available dictionary of
    molecular entities focused on small chemical compounds.

    ChEBI service: https://www.ebi.ac.uk/chebi/
    API documentation: https://www.ebi.ac.uk/chebi/backend/api/docs/
    """

    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {
            "ChEBI": "https://www.ebi.ac.uk/chebi/backend/api/",
        }

        self.attributes = [
            {"code": "chebiid", "label": "chebiId"},
            {"code": "compound_name", "label": "chebiAsciiName"},
            {"code": "inchikey", "label": "inchiKey"},
            {"code": "inchi", "label": "inchi"},
            {"code": "smiles", "label": "smiles"},
            {"code": "formula", "label": "formula"},
        ]

        # generate top level methods defining allowed conversions
        conversions = [
            ("compound_name", "chebiid", "from_name"),
            ("compound_name", "inchikey", "from_name"),
            ("compound_name", "inchi", "from_name"),
            ("compound_name", "smiles", "from_name"),
            ("compound_name", "formula", "from_name"),
            ("inchikey", "chebiid", "from_inchikey"),
            ("inchikey", "compound_name", "from_inchikey"),
            ("inchikey", "inchi", "from_inchikey"),
            ("inchikey", "smiles", "from_inchikey"),
            ("inchikey", "formula", "from_inchikey"),
            ("inchi", "chebiid", "from_inchi"),
            ("inchi", "compound_name", "from_inchi"),
            ("inchi", "inchikey", "from_inchi"),
            ("inchi", "smiles", "from_inchi"),
            ("inchi", "formula", "from_inchi"),
            ("smiles", "chebiid", "from_smiles"),
            ("smiles", "compound_name", "from_smiles"),
            ("smiles", "inchikey", "from_smiles"),
            ("smiles", "inchi", "from_smiles"),
            ("smiles", "formula", "from_smiles"),
            ("chebiid", "compound_name", "from_chebiid"),
            ("chebiid", "inchikey", "from_chebiid"),
            ("chebiid", "inchi", "from_chebiid"),
            ("chebiid", "smiles", "from_chebiid"),
            ("chebiid", "formula", "from_chebiid"),
        ]
        self.create_top_level_conversion_methods(conversions)

    async def from_name(self, name):
        """
        Convert compound name to all possible attributes using ChEBI service.

        :param name: given compound name
        :return: all found data
        """
        args = f"search?query={name}&searchCategory=CHEBI_NAME&maximumResults=10&stars=ALL"
        return await self.call_service(args)

    async def from_inchikey(self, inchikey):
        """
        Convert InChIKey to all possible attributes using ChEBI service.

        :param inchikey: given InChIKey
        :return: all found data
        """
        args = f"search?query={inchikey}&searchCategory=INCHI_KEY&maximumResults=10&stars=ALL"
        return await self.call_service(args)

    async def from_inchi(self, inchi):
        """
        Convert InChI to all possible attributes using ChEBI service.

        :param inchi: given InChI string
        :return: all found data
        """
        args = f"search?query={inchi}&searchCategory=INCHI&maximumResults=10&stars=ALL"
        return await self.call_service(args)

    async def from_smiles(self, smiles):
        """
        Convert SMILES to all possible attributes using ChEBI service.

        :param smiles: given SMILES string
        :return: all found data
        """
        args = f"search?query={smiles}&searchCategory=SMILES&maximumResults=10&stars=ALL"
        return await self.call_service(args)

    async def from_chebiid(self, chebiid):
        """
        Convert ChEBI ID to all possible attributes using ChEBI service.

        :param chebiid: given ChEBI ID (e.g. 'CHEBI:15422')
        :return: all found data
        """
        args = f"chemicalentity/{chebiid}"
        response = await self.query_the_service("ChEBI", args)
        if response:
            return self.parse_entity(response)

    async def call_service(self, args):
        """
        General method to call ChEBI search service.

        :param args: URL suffix with query arguments
        :return: obtained attributes from the first result
        """
        response = await self.query_the_service("ChEBI", args)
        if response:
            return self.parse_search_results(response)

    def parse_entity(self, response):
        """
        Parse attributes from a single ChEBI entity response.

        :param response: JSON string from /chemicalentity/{chebiId} endpoint
        :return: dict of parsed attributes
        """
        entity = json.loads(response)
        return self._extract_attributes(entity)

    def parse_search_results(self, response):
        """
        Parse attributes from the first result of a ChEBI search response.

        :param response: JSON string from /search endpoint
        :return: dict of parsed attributes from the first result
        """
        response_json = json.loads(response)
        results = response_json.get("priceSearchList", [])
        if not results:
            return None
        return self._extract_attributes(results[0])

    def _extract_attributes(self, entity):
        """
        Extract known attributes from a ChEBI entity dict.

        :param entity: dict representing a ChEBI entity
        :return: dict of parsed attributes
        """
        result = {}
        for att in self.attributes:
            value = entity.get(att["label"])
            if value:
                result[att["code"]] = value
        return result if result else None
