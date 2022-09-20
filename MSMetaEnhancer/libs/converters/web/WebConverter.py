from typing import Any, Union
import aiohttp
from asyncstdlib import lru_cache
from multidict import MultiDict

from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectorError
from asyncio.exceptions import TimeoutError
from aiocircuitbreaker import circuit

from MSMetaEnhancer.libs.Converter import Converter
from MSMetaEnhancer.libs.utils.Errors import ServiceNotAvailable, UnknownResponse, TargetAttributeNotRetrieved


class WebConverter(Converter):
    """
    General class for web conversions.
    """
    FAILURE_THRESHOLD: int = 10
    """Number of consecutive failures before circuit breaker is opened."""

    def __init__(self, session: aiohttp.ClientSession):
        """Constructor for Webconverter.

        Args:
            session (aiohttp.ClientSession): Session to use for web IO.
        """
        super().__init__()
        self.session: aiohttp.ClientSession = session
        self.endpoints = dict()

    async def convert(self, source: str, target: str, data: Union[str, int, float]):
        """Convert data from source attribute to target attribute.

        Args:
            source (str): Source attribute name.
            target (str): Target attribute name.
            data (Union[str, int, float]): Data to use for the conversion

        Raises:
            TargetAttributeNotRetrieved: Exception raised if the target attribute is not retrieved from the converter.

        Returns:
            _type_: Data retrieved from the service.
        """
        result = await getattr(self, f'{source}_to_{target}')(data)
        if result:
            return result
        else:
            raise TargetAttributeNotRetrieved(f'No data retrieved.')

    @lru_cache
    async def query_the_service(self, service: str, args: str, method: str = 'GET', data=None, headers=None) -> str:
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
            raise TypeError(f'Incorrect argument {args} for converter {service}.')

    @circuit(failure_threshold=FAILURE_THRESHOLD,
             expected_exception=Union[TimeoutError, ServerDisconnectedError, ClientConnectorError].__args__,
             fallback_function=ServiceNotAvailable.raise_circuitbreaker)
    async def make_request(self, url, method, data, headers):
        """
        Enter a circuit breaker loop and execute request with type depending on specified method.

        :param url: converter URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param headers: optional headers for the request
        :return: obtained response
        """
        if headers is None:
            headers = dict()
        if method == 'GET':
            async with self.session.get(url, headers=headers) as response:
                return await self.process_request(response, url, method)
        else:
            data = MultiDict(data)
            async with self.session.post(url, data=data, headers=headers) as response:
                return await self.process_request(response, url, method)

    async def loop_request(self, url: str, method: str, data: Any, headers: dict) -> str:
        """
        Execute request in a circuit breaker loop. If the request fails multiple times in a row,
        the circuit breaker is opened and ServiceNotAvailable exception is raised.

        :param url: converter URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param headers: optional headers for the request
        :return: obtained response
        """
        try:
            return await self.make_request(url, method, data, headers)
        except (ServerDisconnectedError, ClientConnectorError, TimeoutError):
            return await self.loop_request(url, method, data, headers)

    async def process_request(self, response: aiohttp.ClientResponse, url: str, method: str) -> str:
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
