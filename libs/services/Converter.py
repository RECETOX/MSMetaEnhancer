from aiohttp.client_exceptions import ServerDisconnectedError
from libs.utils.Errors import DataNotRetrieved, ConversionNotSupported


class Converter:
    async def query_the_service(self, service, args, session, method='GET', data=None):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :param session: current aiohttp session
        :param method: GET (default) or POST
        :param data: data for POST request
        :return: obtained response
        """
        try:
            result = await self.loop_request(self.services[service] + args, method, data, session)
            return result
        except TypeError:
            pass  # TODO: log - probably given argument is incorrect

    async def loop_request(self, url, method, data, session, depth=10):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param session: current aiohttp session
        :param depth: allowed recursion depth for unsuccessful requests
        :return: obtained response
        """
        try:
            if method == 'GET':
                async with session.get(url=url) as response:
                    return await self.process_request(response, url, method, data, session, depth)
            else:
                async with session.post(url=url, data=data) as response:
                    return await self.process_request(response, url, method, data, session, depth)
        except ServerDisconnectedError:
            if depth > 0:
                return await self.loop_request(url, method, data, session, depth - 1)

    async def process_request(self, response, url, method, data, session, depth):
        """
        Method to wrap response handling (same for POST and GET requests).

        :param response: given async response
        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :param session: current aiohttp session
        :param depth: allowed recursion depth for unsuccessful requests
        :return: processed response
        """
        result = await response.text()
        if response.ok:
            return result
        elif response.status == 503:
            if depth > 0:
                return await self.loop_request(url, method, data, session, depth - 1)
        else:
            pass  # TODO: log - other error responses

    async def convert(self, source, target, data, session):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :param session: current aiohttp session
        :return: obtained value of target attribute
        """
        try:
            result = await getattr(self, f'{source}_to_{target}')(data, session)
            if result:
                return result
            raise DataNotRetrieved(f'Target attribute {target} not available.')
        except AttributeError:
            raise ConversionNotSupported(f'Target attribute {target} is not supported.')
