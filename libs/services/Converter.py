import requests
from libs.utils.Errors import DataNotRetrieved, ConversionNotSupported


class Converter:
    def __init__(self):
        # used to store individual API calls to avoid executing
        # the same query multiple times in single session
        self.cache = dict()

    def query_the_service(self, service, args, method='GET', data=None):
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
            identification = f'{service}:{args}'
            cached_result = self.cache.get(identification, None)
            if cached_result:
                return cached_result
            result = self.execute_request(self.services[service] + args, method, data)
            self.cache[identification] = result
            return result
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f'Service {service} is not available')

    def execute_request(self, url, method, data=None):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :return: obtained response
        """
        if method == 'GET':
            return requests.get(url)
        else:
            return requests.post(url, data=data)

    def convert(self, source, target, data):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :return: obtained value of target attribute
        """
        try:
            result = getattr(self, f'{source}_to_{target}')(data)
            if result:
                return result
            raise DataNotRetrieved(f'Target attribute {target} not available.')
        except AttributeError:
            raise ConversionNotSupported(f'Target attribute {target} is not supported.')
