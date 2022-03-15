import aiohttp
from asyncstdlib import lru_cache
from multidict import MultiDict


from aiohttp.client_exceptions import ServerDisconnectedError
from asyncio.exceptions import TimeoutError

from MSMetaEnhancer.libs.Converter import Converter
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import ServiceNotAvailable, UnknownResponse, TargetAttributeNotRetrieved


class WebConverter(Converter):
    """
    General class for web conversions.
    """
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def convert(self, source, target, data):
        result = await getattr(self, f'{source}_to_{target}')(data)
        if result:
            return result
        else:
            raise TargetAttributeNotRetrieved(f'{self.converter_name}: {source} -> {target} '
                                              f'- conversion retrieved no data.')

    @lru_cache
    async def query_the_service(self, service, args, method='GET', data=None, headers=None):
        """
        Make get request to given converter with arguments.
        Raises ConnectionError if converter is not available.

        :param service: requested converter to be queried
        :param args: additional query arguments
        :param method: GET (default) or POST
        :param data: data for POST request
        :param headers: optional headers for the request
        :return: obtained response
        """
        try:
            result = await self.loop_request(self.endpoints[service] + args, method, data, headers)
            return result
        except TypeError:
            logger.error(TypeError(f'Incorrect argument {args} for converter {service}.'))

    async def loop_request(self, url, method, data, headers, depth=10):
        """
        Execute request with type depending on specified method.

        :param url: converter URL
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
                data = MultiDict(data)
                async with self.session.post(url, data=data, headers=headers) as response:
                    return await self.process_request(response, url, method)
        except (ServerDisconnectedError, aiohttp.client_exceptions.ClientConnectorError, TimeoutError):
            if depth > 0:
                logger.error(ServiceNotAvailable(f'Service {self.converter_name} '
                                                 f'temporarily unavailable, trying again...'))
                return await self.loop_request(url, method, data, headers, depth - 1)
            raise ServiceNotAvailable

    async def process_request(self, response, url, method):
        """
        Method to wrap response handling (same for POST and GET requests).

        :param response: given async response
        :param url: converter URL
        :param method: GET/POST
        :return: processed response
        """
        result = await response.text()
        if response.ok:
            return result
        else:
            raise UnknownResponse(f'Unknown response {response.status}:{result} for {method} request on {url}.')
