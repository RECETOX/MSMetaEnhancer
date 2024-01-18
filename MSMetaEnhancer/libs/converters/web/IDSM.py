import asyncio

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter
from frozendict import frozendict

from MSMetaEnhancer.libs.utils.Generic import escape_single_quotes


class IDSM(WebConverter):
    """
    IDSM provides unique source of fast similarity and structural search functionality
    in databases such as ChEMBL, ChEBI or PubChem.
    Currently, PubChem fragment is supported.

    IDSM service: https://idsm.elixir-czech.cz/
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {'IDSM': 'https://idsm.elixir-czech.cz/sparql/endpoint/idsm'}
        self.header = frozendict({"Accept": "application/sparql-results+json"})

        self.attributes = [{'code': 'inchi', 'label': 'CHEMINF_000396'},
                           {'code': 'iupac_name', 'label': 'CHEMINF_000382'},
                           {'code': 'inchikey', 'label': 'CHEMINF_000399'},
                           {'code': 'formula', 'label': 'CHEMINF_000335'},
                           {'code': 'canonical_smiles', 'label': 'CHEMINF_000376'},
                           {'code': 'isomeric_smiles', 'label': 'CHEMINF_000379'}]

        # generate top level methods defining allowed conversions
        conversions = [('compound_name', 'inchi', 'from_name'),
                       ('compound_name', 'iupac_name', 'from_name'),
                       ('compound_name', 'inchikey', 'from_name'),
                       ('compound_name', 'formula', 'from_name'),
                       ('compound_name', 'canonical_smiles', 'from_name'),
                       ('compound_name', 'isomeric_smiles', 'from_name'),
                       ('inchi', 'iupac_name', 'from_inchi'),
                       ('inchi', 'inchikey', 'from_inchi'),
                       ('inchi', 'formula', 'from_inchi'),
                       ('inchi', 'canonical_smiles', 'from_inchi'),
                       ('inchi', 'isomeric_smiles', 'from_inchi')]
        self.create_top_level_conversion_methods(conversions)

        # used to limit the maximal number of simultaneous requests being processed
        self.semaphore = asyncio.Semaphore(10)

    @escape_single_quotes
    async def iupac_name_to_inchi(self, iupac_name):
        """
        Convert IUPAC name to InChI using IDSM service

        :param iupac_name: given IUPAC name
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?value (sio:CHEMINF_000396 as ?type)
        FROM pubchem:compound FROM descriptor:compound
        WHERE
        {{
          ?compound sio:SIO_000008 [
            rdf:type sio:CHEMINF_000396;
            sio:SIO_000300 ?value ].
          ?compound sio:SIO_000008 [
            rdf:type sio:CHEMINF_000382;
            sio:SIO_000300 ?iupac_name ].
          filter(lcase(str(?iupac_name)) = '{iupac_name.lower()}')
        }}
        """
        return await self.call_service(query)

    @escape_single_quotes
    async def from_name(self, name):
        """
        Convert Chemical name to all possible attributes using IDSM service

        :param name: given Chemical name
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?value ?type
        FROM pubchem:compound FROM pubchem:inchikey FROM descriptor:compound
        FROM NAMED pubchem:synonym
        WHERE
        {{
          VALUES ?type {{
            sio:CHEMINF_000396 sio:CHEMINF_000382
            sio:CHEMINF_000399 sio:CHEMINF_000335
            sio:CHEMINF_000376 sio:CHEMINF_000379 }}
          ?compound sio:SIO_000008 [
            rdf:type ?type;
            sio:SIO_000300 ?value ].
          GRAPH pubchem:synonym {{
            ?compound sio:SIO_000008 [
              sio:SIO_000300 ?synonym ]
            FILTER(lcase(str(?synonym)) = '{name.lower()}')
          }}
        }}
        """
        return await self.call_service(query)

    @escape_single_quotes
    async def from_inchi(self, inchi):
        """
        Convert InChi to to all possible attributes using IDSM service

        :param inchi: given InChi
        :return: all found data
        """
        query = f"""
        SELECT DISTINCT ?value ?type
        FROM pubchem:compound FROM pubchem:inchikey FROM descriptor:compound
        WHERE
        {{
          VALUES ?type {{
            sio:CHEMINF_000396 sio:CHEMINF_000382
            sio:CHEMINF_000399 sio:CHEMINF_000335
            sio:CHEMINF_000376 sio:CHEMINF_000379 }}
          ?compound sio:SIO_000008 [
            rdf:type ?type;
            sio:SIO_000300 ?value ].
          ?compound sio:SIO_000008 [
            rdf:type sio:CHEMINF_000396;
            sio:SIO_000300 '{inchi}'@en ].
        }}
        """
        return await self.call_service(query)

    async def call_service(self, query):
        """
        General method to call IDSM service.

        Uses semaphore to control maximal number of simultaneous requests being processed.
        Limited to 10 as required by IDSM service.

        :param query: given SPARQL query
        :return: obtained attributes
        """
        data = frozendict({"query": query})
        async with self.semaphore:
            response = await self.query_the_service('IDSM', '', method='POST', data=data, headers=self.header)
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
