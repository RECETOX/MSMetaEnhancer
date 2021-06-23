import requests


class Converter:
    def __init__(self):
        # used to store individual API calls to avoid executing
        # the same query multiple times in single session
        self.cache = dict()

    def connect_to_service(self, service, args, method='GET', data=None):
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
