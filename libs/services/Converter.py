from asyncstdlib import lru_cache


from aiohttp.client_exceptions import ServerDisconnectedError
from libs.utils.Errors import DataNotRetrieved, ConversionNotSupported


class Converter:
    def __init__(self, session):
        self.session = session

    @lru_cache
    async def query_the_service(self, service, args, method='GET', data=None):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :param method: GET (default) or POST
        :param data: data for POST request
        :return: obtained response
        """
        try:
            result = await self.loop_request(self.services[service] + args, method, data)
            return result
        except TypeError:
            pass  # TODO: log - probably given argument is incorrect

    async def loop_request(self, url, method, data, depth=10):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param depth: allowed recursion depth for unsuccessful requests
        :return: obtained response
        """
        try:
            if method == 'GET':
                async with self.session.get(url=url) as response:
                    return await self.process_request(response, url, method, data, depth)
            else:
                async with self.session.post(url=url, data=data) as response:
                    return await self.process_request(response, url, method, data, depth)
        except ServerDisconnectedError:
            if depth > 0:
                return await self.loop_request(url, method, data, depth - 1)

    async def process_request(self, response, url, method, data, depth):
        """
        Method to wrap response handling (same for POST and GET requests).

        :param response: given async response
        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param depth: allowed recursion depth for unsuccessful requests
        :return: processed response
        """
        result = await response.text()
        if response.ok:
            return result
        elif response.status == 503:
            if depth > 0:
                return await self.loop_request(url, method, data, depth - 1)
        else:
            pass  # TODO: log - other error responses

    async def convert(self, source, target, data):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :return: obtained value of target attribute
        """
        try:
            result = await getattr(self, f'{source}_to_{target}')(data)
            if result:
                return result
            raise DataNotRetrieved(f'Target attribute {target} not available.')
        except AttributeError:
            raise ConversionNotSupported(f'Conversion from {source} to {target} is not supported.')

    def create_top_level_conversion_methods(self, conversions):
        """
        Method to create and set dynamic methods defined in conversions

        :param conversions: triples of form (from, to, method)
        """
        for conversion in conversions:
            create_top_level_method(self, *conversion)


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
