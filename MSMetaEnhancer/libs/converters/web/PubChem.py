import json

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter
from frozendict import frozendict

from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
from MSMetaEnhancer.libs.utils.Throttler import Throttler


class PubChem(WebConverter):
    """
    PubChem is the world's largest collection of freely accessible chemical information.

    PubChem service: https://pubchem.ncbi.nlm.nih.gov/
    """
    def __init__(self, session):
        super().__init__(session)
        # service URLs
        self.endpoints = {'PubChem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'}

        self.attributes = [{'code': 'inchi', 'label': 'InChI', 'extra': None},
                           {'code': 'inchikey', 'label': 'InChIKey', 'extra': None},
                           {'code': 'iupac_name', 'label': 'IUPAC Name', 'extra': 'Preferred'},
                           {'code': 'formula', 'label': 'Molecular Formula', 'extra': None},
                           {'code': 'canonical_smiles', 'label': 'SMILES', 'extra': 'Canonical'},
                           {'code': 'isomeric_smiles', 'label': 'SMILES', 'extra': 'Isomeric'}]

        # generate top level methods defining allowed conversions
        conversions = [('compound_name', 'inchi', 'from_name'),
                       ('compound_name', 'inchikey', 'from_name'),
                       ('compound_name', 'iupac_name', 'from_name'),
                       ('compound_name', 'formula', 'from_name'),
                       ('compound_name', 'canonical_smiles', 'from_name'),
                       ('compound_name', 'isomeric_smiles', 'from_name'),
                       ('inchi', 'inchikey', 'from_inchi'),
                       ('inchi', 'iupac_name', 'from_inchi'),
                       ('inchi', 'formula', 'from_inchi'),
                       ('inchi', 'canonical_smiles', 'from_inchi'),
                       ('inchi', 'isomeric_smiles', 'from_inchi'),
                       ('inchi', 'pubchemid', 'from_inchi'),
                       ('pubchemid', 'inchi', 'from_pubchemid')]
        self.create_top_level_conversion_methods(conversions)

        self.throttler = Throttler(rate_limit=4)

    async def pubchemid_to_hmdbid(self, pubchemid):
        """
        Obtain HMDB ID identifier based on given PubChem ID using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param pubchemid: given Chemical name
        :return: all found data
        """
        args = f'cid/{pubchemid}/xrefs/RegistryID/JSON'
        async with self.throttler:
            response = await self.query_the_service('PubChem', args)
        response_json = json.loads(response)

        registry_ids = response_json['InformationList']['Information'][0]['RegistryID']
        hmdbids = [item for item in registry_ids if item.startswith('HMDB')]

        if len(hmdbids) != 0:
            return {'hmdbid': hmdbids[0]}
        return dict()

    async def from_pubchemid(self, pubchemid):
        """
        Obtain chemical identifiers based on given PubChem ID using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param pubchemid: given Chemical name
        :return: all found data
        """
        args = f'cid/{pubchemid}/JSON'
        return await self.call_service(args, 'GET', None)

    async def from_name(self, name):
        """
        Convert Chemical name to all possible attributes using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param name: given Chemical name
        :return: all found data
        """
        args = f'name/{name}/JSON'
        return await self.call_service(args, 'GET', None)

    async def from_inchi(self, inchi):
        """
        Convert InChi to to all possible attributes using PubChem service
        More info: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

        :param inchi: given InChi
        :return: all found data
        """
        args = "inchi/JSON"
        return await self.call_service(args, 'POST', frozendict({'inchi': inchi}))

    async def call_service(self, args, method, data):
        """
        General method to call PubChem service.

        Uses a throttler to control maximal number of simultaneous requests being processed per second.
        Limited to 5 requests per second, can be dynamically lowered at times of excessive load.

        More info: https://pubchemdocs.ncbi.nlm.nih.gov/programmatic-access$_requestvolumelimitations

        :param args: additional url suffix
        :param method: POST of GET
        :param data: source data for POST request
        :return: obtained attributes
        """
        async with self.throttler:
            response = await self.query_the_service('PubChem', args, method=method, data=data)
        if response:
            return self.parse_attributes(response)

    async def process_request(self, response, url, method):
        """
        Redefined parent method with additional adjustment of throttling.

        :param response: given async response
        :param url: service URL
        :param method: GET/POST
        :return: processed response
        """
        result = await response.text()
        if 'X-Throttling-Control' in response.headers:
            self.adjust_throttling(response.headers['X-Throttling-Control'])
        if response.ok:
            return result
        else:
            raise UnknownResponse(f'Unknown response {response.status}:{result} for {method} request on {url}.')

    def adjust_throttling(self, throttling_header):
        """
        Adjust current requests rate based on Dynamic Request Throttling provided by PubChem.

        More info: https://pubchemdocs.ncbi.nlm.nih.gov/dynamic-request-throttling

        :param throttling_header: header containing current service load info
        """
        def parse_status(part):
            value = part.split(': ')[1]
            return int(value.split(' (')[1][:-2])

        def parse_pubchem_info(header):
            """
            Parse PubChem header regarding Dynamic Request Throttling.

            It has the following form of three indicators:
            Request Count status: Green (0%), Request Time status: Green (0%), WebConverter status: Green (20%)

            :param header: given PubChem header with Throttling info
            :return: most critical indicator value (maximum of three) with possible complete blacklist indicator
            """
            indicators = header.split(',')
            blocked = False
            if 'too many requests per second or blacklisted' in indicators[-1]:
                blocked = True
            return {'load': max([parse_status(indicator) for indicator in indicators[:3]]), 'blocked': blocked}

        status = parse_pubchem_info(throttling_header)
        if status['blocked'] or status['load'] > 75:
            self.throttler.decrease_limit()
        elif status['load'] < 25:
            self.throttler.increase_limit()

    def parse_attributes(self, response):
        """
        Parse all available attributes (specified in self.attributes) from given response.

        Method does not return anything, instead stores data in local cache.

        :param response: given JSON
        :return: all parsed data
        """
        response_json = json.loads(response)
        result = dict()

        if 'PC_Compounds' in response_json:
            if len(response_json['PC_Compounds']) > 0:
                first_hit = response_json['PC_Compounds'][0]

                pubchemid = first_hit.get('id', {}).get('id', {}).get('cid', None)
                if pubchemid:
                    result['pubchemid'] = pubchemid

                for prop in first_hit.get('props', {}):
                    label = prop['urn']['label']
                    for att in self.attributes:
                        if label == att['label']:
                            if att['extra']:
                                if prop['urn']['name'] == att['extra']:
                                    result[att['code']] = prop['value']['sval']
                            else:
                                result[att['code']] = prop['value']['sval']
        return result
