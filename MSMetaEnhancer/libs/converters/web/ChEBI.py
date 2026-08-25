import json
from urllib.parse import quote

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
            "ChEBI": "https://www.ebi.ac.uk/chebi/backend/api/public/",
        }

        self.attributes = [
            {"code": "chebiid", "paths": [("chebi_accession",), ("chebiId",)]},
            {
                "code": "compound_name",
                "paths": [("ascii_name",), ("name",), ("chebiAsciiName",)],
            },
            {
                "code": "iupac_name",
                "paths": [("iupac_names",), ("iupacName",)],
            },
            {
                "code": "inchikey",
                "paths": [
                    ("default_structure", "standard_inchi_key"),
                    ("inchikey",),
                    ("standard_inchi_key",),
                    ("inchiKey",),
                ],
            },
            {
                "code": "inchi",
                "paths": [("default_structure", "standard_inchi"), ("inchi",)],
            },
            {"code": "smiles", "paths": [("default_structure", "smiles"), ("smiles",)]},
            {
                "code": "formula",
                "paths": [("chemical_data", "formula"), ("formula",)],
            },
        ]

        # generate top level methods defining allowed conversions
        conversions = [
            ("compound_name", "chebiid", "from_name"),
            ("compound_name", "inchikey", "from_name"),
            ("compound_name", "inchi", "from_name"),
            ("compound_name", "smiles", "from_name"),
            ("compound_name", "formula", "from_name"),
            ("iupac_name", "chebiid", "from_iupac_name"),
            ("iupac_name", "compound_name", "from_iupac_name"),
            ("iupac_name", "inchikey", "from_iupac_name"),
            ("iupac_name", "inchi", "from_iupac_name"),
            ("iupac_name", "smiles", "from_iupac_name"),
            ("iupac_name", "formula", "from_iupac_name"),
            ("inchikey", "chebiid", "from_inchikey"),
            ("inchikey", "compound_name", "from_inchikey"),
            ("inchikey", "iupac_name", "from_inchikey"),
            ("inchikey", "inchi", "from_inchikey"),
            ("inchikey", "smiles", "from_inchikey"),
            ("inchikey", "formula", "from_inchikey"),
            ("inchi", "chebiid", "from_inchi"),
            ("inchi", "compound_name", "from_inchi"),
            ("inchi", "iupac_name", "from_inchi"),
            ("inchi", "inchikey", "from_inchi"),
            ("inchi", "smiles", "from_inchi"),
            ("inchi", "formula", "from_inchi"),
            ("smiles", "chebiid", "from_smiles"),
            ("smiles", "compound_name", "from_smiles"),
            ("smiles", "iupac_name", "from_smiles"),
            ("smiles", "inchikey", "from_smiles"),
            ("smiles", "inchi", "from_smiles"),
            ("smiles", "formula", "from_smiles"),
            ("chebiid", "compound_name", "from_chebiid"),
            ("chebiid", "iupac_name", "from_chebiid"),
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
        return await self._from_es_search(name)

    async def from_iupac_name(self, iupac_name):
        """
        Convert IUPAC name to all possible attributes using ChEBI service.

        :param iupac_name: given IUPAC name
        :return: all found data
        """
        return await self._from_es_search(iupac_name)

    async def _from_es_search(self, term):
        """
        Search ChEBI by a given term and return parsed attributes.

        :param term: search term (name, InChIKey, InChI, SMILES, or IUPAC name)
        :return: all found data
        """
        args = f"es_search/?term={quote(term)}&page=1&size=15"
        response = await self.query_the_service("ChEBI", args)
        if response:
            return self.parse_search_results(response)

    async def from_inchikey(self, inchikey):
        """
        Convert InChIKey to all possible attributes using ChEBI service.

        :param inchikey: given InChIKey
        :return: all found data
        """
        return await self._from_es_search(inchikey)

    async def from_inchi(self, inchi):
        """
        Convert InChI to all possible attributes using ChEBI service.

        :param inchi: given InChI string
        :return: all found data
        """
        return await self._from_es_search(inchi)

    async def from_smiles(self, smiles):
        """
        Convert SMILES to all possible attributes using ChEBI service.

        :param smiles: given SMILES string
        :return: all found data
        """
        return await self._from_es_search(smiles)

    async def from_chebiid(self, chebiid):
        """
        Convert ChEBI ID to all possible attributes using ChEBI service.

        :param chebiid: given ChEBI ID (e.g. 'CHEBI:60888')
        :return: all found data
        """
        args = f"compound/{chebiid}/"
        response = await self.query_the_service("ChEBI", args)
        if response:
            return self.parse_entity(response)

    def parse_entity(self, response):
        """
        Parse attributes from a single ChEBI entity response.

        :param response: JSON string from /compound/{chebiId}/ endpoint
        :return: dict of parsed attributes
        """
        entity = json.loads(response)
        return self._extract_attributes(entity)

    def parse_search_results(self, response):
        """
        Parse attributes from the first result of a ChEBI search response.

        :param response: JSON string from /es_search/ endpoint
        :return: dict of parsed attributes from the first result
        """
        response_json = json.loads(response)
        results = response_json.get("results", [])
        if not results:
            return None
        entity = results[0]
        if isinstance(entity, dict):
            entity = entity.get("_source", entity)
        return self._extract_attributes(entity)

    def _extract_attributes(self, entity):
        """
        Extract known attributes from a ChEBI entity dict.

        :param entity: dict representing a ChEBI entity
        :return: dict of parsed attributes
        """
        if not isinstance(entity, dict):
            return None
        result = {}
        for att in self.attributes:
            value = self._get_first_value(entity, att["paths"])
            if value is not None:
                result[att["code"]] = value
        # Extract IUPAC name from synonyms list (entity endpoint)
        if "iupac_name" not in result:
            iupac_name = self._extract_iupac_from_synonyms(entity)
            if iupac_name is not None:
                result["iupac_name"] = iupac_name
        return result if result else None

    def _extract_iupac_from_synonyms(self, entity):
        """
        Extract IUPAC name from the synonyms list in a ChEBI entity response.

        :param entity: dict representing a ChEBI entity
        :return: IUPAC name string or None
        """
        synonyms = entity.get("synonyms", [])
        if isinstance(synonyms, list):
            for syn in synonyms:
                if isinstance(syn, dict) and syn.get("type") == "IUPAC NAME":
                    return syn.get("data")
        return None

    def _get_first_value(self, entity, paths):
        """
        Return the first non-empty value found in the given candidate paths.
        If the resolved value is a list, the first element is returned.

        :param entity: dict representing a ChEBI entity
        :param paths: candidate key paths to try
        :return: first non-empty value or None
        """
        for path in paths:
            value = entity
            for key in path:
                if not isinstance(value, dict):
                    value = None
                    break
                value = value.get(key)
            if value is not None:
                if isinstance(value, list):
                    return value[0] if value else None
                return value
        return None
