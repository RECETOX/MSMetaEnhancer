import aiohttp
from asyncstdlib import lru_cache


from aiohttp.client_exceptions import ServerDisconnectedError
from asyncio.exceptions import TimeoutError

from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import TargetAttributeNotRetrieved, ServiceNotAvailable, UnknownResponse


class Converter:
    """
    General class for conversion services.
    """
    def __init__(self, session):
        self.session = session
        self.is_available = True

    @property
    def service_name(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(self.service_name)

    @lru_cache
    async def query_the_service(self, service, args, method='GET', data=None, headers=None):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :param method: GET (default) or POST
        :param data: data for POST request
        :param headers: optional headers for the request
        :return: obtained response
        """
        try:
            result = await self.loop_request(self.services[service] + args, method, data, headers)
            return result
        except TypeError:
            logger.error(TypeError(f'Incorrect argument {args} for service {service}.'))

    async def loop_request(self, url, method, data, headers, depth=10):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param depth: allowed recursion depth for unsuccessful requests
        :param headers: optional headers for the request
        :return: obtained response
        """
        if headers is None:
            headers = dict()
        try:
            if method == 'GET':
                async with self.session.get(url, headers=headers) as response:
                    return await self.process_request(response, url, method)
            else:
                async with self.session.post(url, data=data, headers=headers) as response:
                    return await self.process_request(response, url, method)
        except (ServerDisconnectedError, aiohttp.client_exceptions.ClientConnectorError, TimeoutError):
            if depth > 0:
                logger.error(ServiceNotAvailable(f'Service {self.service_name} '
                                                 f'temporarily unavailable, trying again...'))
                return await self.loop_request(url, method, data, headers, depth - 1)
            raise ServiceNotAvailable

    async def process_request(self, response, url, method):
        """
        Method to wrap response handling (same for POST and GET requests).

        :param response: given async response
        :param url: service URL
        :param method: GET/POST
        :return: processed response
        """
        result = await response.text()
        if response.ok:
            return result
        else:
            raise UnknownResponse(f'Unknown response {response.status}:{result} for {method} request on {url}.')

    async def convert(self, source, target, data):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :return: obtained value of target attribute
        """
        result = await getattr(self, f'{source}_to_{target}')(data)
        if result:
            return result
        else:
            raise TargetAttributeNotRetrieved(f'{self.service_name}: {source} -> {target} '
                                              f'- conversion retrieved no data.')

    def create_top_level_conversion_methods(self, conversions):
        """
        Method to create and set dynamic methods defined in conversions

        :param conversions: triples of form (from, to, method)
        """
        for conversion in conversions:
            create_top_level_method(self, *conversion)

    def get_conversion_functions(self):
        """
        Method to compute all available conversion functions.

        Assumes that the functions always have from {source}_to_{target}

        :return: a list of available conversion functions
        """
        jobs = []
        methods = [method_name for method_name in dir(self) if '_to_' in method_name]
        for method in methods:
            jobs.append((*method.split('_to_'), self.service_name))
        return jobs


def create_top_level_method(obj, source, target, method):
    """
    Assign a new method to {obj} called {source}_to_{target} which calls {method}.

    :param obj: given object (typically a Converter)
    :param source: attribute name used as source of data
    :param target: attribute name obtained using this dynamic method
    :param method: method which is called in the object with single argument
    """
    async def conversion(key):
        return await getattr(obj, str(method))(key)

    conversion.__doc__ = f'Convert {source} to {target} using {obj.__class__.__name__} service'
    conversion.__name__ = f'{source}_to_{target}'

    setattr(obj, conversion.__name__, conversion)
