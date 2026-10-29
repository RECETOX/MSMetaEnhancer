import json
from urllib.parse import urlencode

from frozendict import frozendict

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter


class Wikidata(WebConverter):
    """
    Convert compound names, identifiers, and structures using Wikidata.

    Wikidata Query Service: https://query.wikidata.org/
    """

    attributes = (
        "compound_name",
        "casno",
        "inchi",
        "inchikey",
        "canonical_smiles",
        "pubchemid",
        "wikidataid",
    )
    identifier_properties = {
        "pubchemid": "P662",
        "inchi": "P234",
        "inchikey": "P235",
    }

    def __init__(self, session):
        super().__init__(session)
        self.endpoints = {"Wikidata": "https://query.wikidata.org/sparql?"}
        source_methods = {
            "compound_name": "from_name",
            "casno": "from_casno",
            "wikidataid": "from_wikidataid",
            "pubchemid": "from_pubchemid",
            "inchi": "from_inchi",
            "inchikey": "from_inchikey",
        }
        conversions = [
            (source, target, method)
            for source, method in source_methods.items()
            for target in self.attributes
            if source != target
        ]
        self.create_top_level_conversion_methods(conversions)

    @staticmethod
    def result_variables():
        return " ".join(f"?{attribute}" for attribute in Wikidata.attributes)

    @staticmethod
    def item_attributes_query():
        return """
              OPTIONAL {
                ?item rdfs:label ?compound_name .
                FILTER(LANG(?compound_name) = "en")
              }
              OPTIONAL { ?item wdt:P231 ?casno . }
              OPTIONAL { ?item wdt:P234 ?inchi . }
              OPTIONAL { ?item wdt:P235 ?inchikey . }
              OPTIONAL { ?item wdt:P233 ?canonical_smiles . }
              OPTIONAL { ?item wdt:P662 ?pubchemid . }
              BIND(STRAFTER(STR(?item), "http://www.wikidata.org/entity/")
                   AS ?wikidataid)
        """

    async def from_name(self, name):
        query = f"""
            PREFIX bd: <http://www.bigdata.com/rdf#>
            PREFIX mwapi: <https://www.mediawiki.org/ontology#API/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wikibase: <http://wikiba.se/ontology#>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT {self.result_variables()} WHERE {{
              SERVICE wikibase:mwapi {{
                bd:serviceParam wikibase:api "EntitySearch" ;
                  wikibase:endpoint "www.wikidata.org" ;
                  mwapi:search {self.sparql_literal(name)} ;
                  mwapi:language "en" ;
                  mwapi:limit "1" .
                ?item wikibase:apiOutputItem mwapi:item .
              }}
              {self.item_attributes_query()}
            }}
            LIMIT 1
        """
        return await self.call_service(query)

    async def from_casno(self, casno):
        query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT {self.result_variables()} WHERE {{
              ?item wdt:P231 ?casno .
              FILTER(?casno = {self.sparql_literal(casno)})
              {self.item_attributes_query()}
            }}
            LIMIT 1
        """
        return await self.call_service(query)

    async def from_wikidataid(self, wikidataid):
        if not wikidataid.startswith("Q") or not wikidataid[1:].isdigit():
            return {}

        query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT {self.result_variables()} WHERE {{
              BIND(wd:{wikidataid} AS ?item)
              {self.item_attributes_query()}
            }}
            LIMIT 1
        """
        return await self.call_service(query)

    async def from_pubchemid(self, pubchemid):
        return await self.from_identifier("pubchemid", pubchemid)

    async def from_inchi(self, inchi):
        return await self.from_identifier("inchi", inchi)

    async def from_inchikey(self, inchikey):
        return await self.from_identifier("inchikey", inchikey)

    async def from_identifier(self, attribute, value):
        property_id = self.identifier_properties[attribute]
        query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>

            SELECT {self.result_variables()} WHERE {{
              ?item wdt:{property_id} ?identifier .
              FILTER(STR(?identifier) = {self.sparql_literal(value)})
              {self.item_attributes_query()}
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

        return {
            attribute: bindings[0][attribute]["value"]
            for attribute in Wikidata.attributes
            if attribute in bindings[0]
        }
