import json
from urllib.parse import urlencode

from frozendict import frozendict

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class Wikidata(WebConverter):
    """
    Convert compound names and CAS numbers using Wikidata.

    Wikidata Query Service: https://query.wikidata.org/
    """

    def __init__(self, session):
        super().__init__(session)
        self.endpoints = {"Wikidata": "https://query.wikidata.org/sparql?"}
        conversions = [
            ("compound_name", target, "from_name")
            for target in (
                "casno",
                "inchi",
                "inchikey",
                "canonical_smiles",
                "pubchemid",
            )
        ]
        conversions.extend(
            [
                ("casno", target, "from_casno")
                for target in (
                    "compound_name",
                    "inchi",
                    "inchikey",
                    "canonical_smiles",
                    "pubchemid",
                )
            ]
        )
        self.create_top_level_conversion_methods(conversions)

    async def from_name(self, name):
        query = f"""
            PREFIX bd: <http://www.bigdata.com/rdf#>
            PREFIX mwapi: <https://www.mediawiki.org/ontology#API/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wikibase: <http://wikiba.se/ontology#>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT ?compound_name ?casno ?inchi ?inchikey
                   ?canonical_smiles ?pubchemid WHERE {{
              SERVICE wikibase:mwapi {{
                bd:serviceParam wikibase:api "EntitySearch" ;
                  wikibase:endpoint "www.wikidata.org" ;
                  mwapi:search {self.sparql_literal(name)} ;
                  mwapi:language "en" ;
                  mwapi:limit "1" .
                ?item wikibase:apiOutputItem mwapi:item .
              }}
              ?item rdfs:label ?compound_name .
              FILTER(LANG(?compound_name) = "en")
              OPTIONAL {{ ?item wdt:P231 ?casno . }}
              OPTIONAL {{ ?item wdt:P234 ?inchi . }}
              OPTIONAL {{ ?item wdt:P235 ?inchikey . }}
              OPTIONAL {{ ?item wdt:P233 ?canonical_smiles . }}
              OPTIONAL {{ ?item wdt:P662 ?pubchemid . }}
            }}
            LIMIT 1
        """
        return await self.call_service(query)

    async def from_casno(self, casno):
        query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT ?compound_name ?casno ?inchi ?inchikey
                   ?canonical_smiles ?pubchemid WHERE {{
              ?item wdt:P231 ?casno .
              ?item rdfs:label ?compound_name .
              FILTER(?casno = {self.sparql_literal(casno)})
              FILTER(LANG(?compound_name) = "en")
              OPTIONAL {{ ?item wdt:P234 ?inchi . }}
              OPTIONAL {{ ?item wdt:P235 ?inchikey . }}
              OPTIONAL {{ ?item wdt:P233 ?canonical_smiles . }}
              OPTIONAL {{ ?item wdt:P662 ?pubchemid . }}
            }}
            LIMIT 1
        """
        return await self.call_service(query)

    async def call_service(self, query):
        args = urlencode({"query": query, "format": "json"})
        response = await self.query_the_service(
            "Wikidata",
            args,
            headers=frozendict(
                {
                    "User-Agent": (
                        "MSMetaEnhancer (https://github.com/RECETOX/MSMetaEnhancer)"
                    )
                }
            ),
        )
        if response:
            return self.parse_attributes(response)
        return {}

    @staticmethod
    def sparql_literal(value):
        return json.dumps(str(value), ensure_ascii=False)

    @staticmethod
    def parse_attributes(response):
        bindings = json.loads(response).get("results", {}).get("bindings", [])
        if not bindings:
            return {}

        attributes = (
            "compound_name",
            "casno",
            "inchi",
            "inchikey",
            "canonical_smiles",
            "pubchemid",
        )
        return {
            attribute: bindings[0][attribute]["value"]
            for attribute in attributes
            if attribute in bindings[0]
        }
