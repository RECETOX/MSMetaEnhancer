import json
from urllib.parse import quote

from frozendict import frozendict

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class ChEBI(WebConverter):
    """
    ChEBI (Chemical Entities of Biological Interest) is a freely available dictionary of
    molecular entities focused on small chemical compounds.

    ChEBI service: https://www.ebi.ac.uk/chebi/
    API documentation: https://www.ebi.ac.uk/chebi/backend/api/docs/

    Identifiers and names are resolved by the `es_search` endpoint, structures by the
    `structure_search` endpoint. Both only return the fields of a compound summary, so the
    obtained accession is used to retrieve the whole record from the `compound` endpoint,
    which is the only one reporting the IUPAC name.
    """

    SEARCH_SIZE = 15
    """Number of search results requested from the ChEBI search endpoints."""

    IDENTIFIER_FIELDS = ("chebi_accession", "inchikey", "inchi", "smiles")
    """Fields used to positively identify a search result by the searched identifier."""

    NAME_FIELDS = ("ascii_name", "name")
    """Fields used to positively identify a search result by the searched name."""

    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {
            "ChEBI": "https://www.ebi.ac.uk/chebi/backend/api/public/",
        }

        # attributes as reported by the compound endpoint
        self.attributes = [
            {"code": "chebiid", "paths": [("chebi_accession",)]},
            {"code": "compound_name", "paths": [("ascii_name",), ("name",)]},
            {"code": "formula", "paths": [("chemical_data", "formula")]},
            {"code": "smiles", "paths": [("default_structure", "smiles")]},
            {"code": "inchi", "paths": [("default_structure", "standard_inchi")]},
            {
                "code": "inchikey",
                "paths": [("default_structure", "standard_inchi_key")],
            },
        ]

        # generate top level methods defining allowed conversions
        conversions = [
            ("compound_name", "chebiid", "from_name"),
            ("compound_name", "iupac_name", "from_name"),
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

        Only compounds reported under the given name by ChEBI are accepted, common names
        present in ChEBI merely as synonyms are not resolved by the search endpoint.

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
        return await self._from_es_search(iupac_name, by_term=False)

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

        Only standard InChIs are accepted by the ChEBI search endpoint.

        :param inchi: given InChI string
        :return: all found data
        """
        return await self._from_es_search(inchi)

    async def _from_es_search(self, term, by_term=True):
        """
        Search ChEBI for the given term and return the attributes of the matching compound.

        :param term: search term (name, IUPAC name, InChIKey or InChI)
        :param by_term: whether the reported fields of a result are compared to the searched
            term; IUPAC names are not reported by the search endpoint, so searches by IUPAC
            name accept a single unambiguous result instead
        :return: all found data
        """
        args = f"es_search/?term={quote(term)}&page=1&size={self.SEARCH_SIZE}"
        response = await self.query_the_service("ChEBI", args)
        if not response:
            return None
        chebiid = self.extract_chebiid(response, term if by_term else None)
        if chebiid is None:
            return None
        return await self.from_chebiid(chebiid)

    async def from_smiles(self, smiles):
        """
        Convert SMILES to all possible attributes using ChEBI structure search service.

        ChEBI scores the submitted structure without re-canonicalising it, so the similarity
        threshold of 1 accepts structures that ChEBI reports in the submitted form.

        :param smiles: given SMILES string
        :return: all found data
        """
        data = frozendict({"structure": smiles, "type": "similarity", "similarity": 1})
        response = await self.query_the_service(
            "ChEBI", "structure_search/", method="POST", data=data
        )
        if not response:
            return None
        chebiid = self.extract_chebiid(response)
        if chebiid is None:
            return None
        return await self.from_chebiid(chebiid)

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
        Parse attributes from a single ChEBI compound response.

        :param response: JSON string from /compound/{chebiId}/ endpoint
        :return: dict of parsed attributes
        """
        return self._extract_attributes(json.loads(response))

    def extract_chebiid(self, response, term=None):
        """
        Obtain the ChEBI accession of the search result corresponding to the searched term.

        ChEBI searches are ranked by relevance and report related compounds first (searching
        for 'bapta' ranks '5,5'-dibromo-BAPTA above 'BAPTA'), so a result is accepted only
        when it can be positively identified - either its reported accession, identifier or
        name equals the searched term, or, when no term is given, the search returned a
        single compound.

        :param response: JSON string from a ChEBI search endpoint
        :param term: term that was used for the search, None to require a single result
        :return: ChEBI accession of the matching compound or None
        """
        entities = [
            result.get("_source", result)
            for result in json.loads(response).get("results", [])
            if isinstance(result, dict)
        ]
        entities = [entity for entity in entities if isinstance(entity, dict)]
        if not entities:
            return None
        if term is None:
            # structure searches are not ranked by a term, a single hit is required
            return entities[0].get("chebi_accession") if len(entities) == 1 else None
        searched = term.strip().casefold()
        for field in self.IDENTIFIER_FIELDS + self.NAME_FIELDS:
            for entity in entities:
                value = entity.get(field)
                if isinstance(value, str) and value.strip().casefold() == searched:
                    return entity.get("chebi_accession")
        return None

    def _extract_attributes(self, entity):
        """
        Extract known attributes from a ChEBI compound dict.

        :param entity: dict representing a ChEBI compound
        :return: dict of parsed attributes
        """
        if not isinstance(entity, dict):
            return None
        result = {}
        for att in self.attributes:
            value = self._get_first_value(entity, att["paths"])
            if value is not None:
                result[att["code"]] = value
        iupac_name = self._extract_iupac_name(entity)
        if iupac_name is not None:
            result["iupac_name"] = iupac_name
        return result if result else None

    @staticmethod
    def _extract_iupac_name(entity):
        """
        Extract the IUPAC name from the names of a ChEBI compound.

        :param entity: dict representing a ChEBI compound
        :return: IUPAC name string or None
        """
        names = entity.get("names")
        if not isinstance(names, dict):
            return None
        for entry in names.get("IUPAC NAME", []):
            if isinstance(entry, dict):
                value = entry.get("ascii_name") or entry.get("name")
                if value:
                    return value
        return None

    def _get_first_value(self, entity, paths):
        """
        Return the first non-empty value found in the given candidate paths.
        Paths that yield no value are skipped and the following ones are tried.

        :param entity: dict representing a ChEBI compound
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
            if value:
                return value
        return None
