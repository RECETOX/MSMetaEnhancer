import asyncio

from MSMetaEnhancer.libs.services.Converter import Converter
from frozendict import frozendict


class PubChem(Converter):
    """
    PubChem is the world's largest collection of freely accessible chemical information.

    Available online at: https://pubchem.ncbi.nlm.nih.gov/

    To improve the performance, we use IDSM service: https://idsm.elixir-czech.cz/
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.services = {'PubChem': 'https://idsm.elixir-czech.cz/sparql/endpoint/idsm'}
        self.header = frozendict({"Accept": "application/sparql-results+json"})

        self.attributes = [{'code': 'inchi', 'label': 'CHEMINF_000396'},
                           {'code': 'iupac_name', 'label': 'CHEMINF_000382'},
                           {'code': 'inchikey', 'label': 'CHEMINF_000399'},
                           {'code': 'formula', 'label': 'CHEMINF_000335'},
                           {'code': 'canonical_smiles', 'label': 'CHEMINF_000376'},
                           {'code': 'isomeric_smiles', 'label': 'CHEMINF_000379'}]

        # generate top level methods defining allowed conversions
        conversions = [('name', 'inchi', 'from_name'),
                       ('name', 'iupac_name', 'from_name'),
                       ('name', 'formula', 'from_name'),
                       ('name', 'canonical_smiles', 'from_name'),
                       ('name', 'isomeric_smiles', 'from_name'),
                       ('inchi', 'iupac_name', 'from_inchi'),
                       ('inchi', 'formula', 'from_inchi'),
                       ('inchi', 'canonical_smiles', 'from_inchi'),
                       ('inchi', 'isomeric_smiles', 'from_inchi')]
        self.create_top_level_conversion_methods(conversions)

        # used to limit the maximal number of simultaneous requests being processed
        self.semaphore = asyncio.Semaphore(10)

    async def name_to_inchikey(self, name):
        """
        Convert Chemical name to InChIKey using IDSM service

        :param name: given Chemical name
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?type ?value
        WHERE
        {{
          ?inchikey sio:has-value ?value.
          ?inchikey rdf:type ?type.
          ?inchikey sio:is-attribute-of ?compound.
          ?synonym sio:is-attribute-of ?compound.
          ?synonym sio:has-value "{name.lower()}"@en.
        }}
        """
        return await self.call_service(query)

    async def inchi_to_inchikey(self, inchi):
        """
        Convert InChi to InChIKey using IDSM service

        :param inchi: given InChi
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?type ?value
        WHERE
        {{
          ?inchikey sio:has-value ?value.
          ?inchikey rdf:type ?type.
          ?inchikey sio:is-attribute-of ?compound.
          ?compound sio:has-attribute ?inchi.
          ?inchi sio:has-value "{inchi}"@en.
        }}
        """
        return await self.call_service(query)

    async def from_name(self, name):
        """
        Convert Chemical name to all possible attributes using IDSM service

        :param name: given Chemical name
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?value ?type
        WHERE
        {{
          ?attribute rdf:type ?type.
          ?attribute sio:has-value ?value.
          ?compound sio:has-attribute ?attribute.
          ?synonym sio:is-attribute-of ?compound.
          ?synonym sio:has-value "{name.lower()}"@en.
        }}
        """
        return await self.call_service(query)

    async def from_inchi(self, inchi):
        """
        Convert InChi to to all possible attributes using IDSM service

        :param inchi: given InChi
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?value ?type
        WHERE
        {{
          ?attribute rdf:type ?type.
          ?attribute sio:has-value ?value.
          ?compound sio:has-attribute ?attribute.
          ?compound sio:has-attribute ?inchi.
          ?inchi sio:has-value "{inchi}"@en.
        }}
        """
        return await self.call_service(query)

    async def call_service(self, query):
        """
        General method to call PubChem service.

        Uses semaphore to control maximal number of simultaneous requests being processed.
        Limited to 10 as required by IDSM service.

        :param query: given SPARQL query
        :return: obtained attributes
        """
        data = frozendict({"query": query})
        async with self.semaphore:
            response = await self.query_the_service('PubChem', '', method='POST', data=data, headers=self.header)
        if response:
            return self.parse_attributes(response)

    def parse_attributes(self, response):
        """
        Parse all available attributes (specified in self.attributes) from given response.

        Method does not return anything, instead stores data in local cache.

        :param response: given JSON
        :return: all parsed data
        """
        response_json = eval(response)
        result = dict()

        for prop in response_json['results']['bindings']:
            identifier = prop['type']['value'].rsplit('/', 1)[-1]
            value = prop['value']['value']
            for att in self.attributes:
                if identifier == att['label']:
                    result[att['code']] = value
        return result
