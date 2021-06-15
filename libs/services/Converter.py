import requests


class Converter:
    def __init__(self):
        # used to store individual API calls to avoid executing
        # the same query multiple times in single session
        self.cache = dict()

    def connect_to_service(self, service, args, method='GET'):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :param method: GET (default) or POST
        :return: obtained response
        """
        try:
            identification = service + ":" + str(args)
            cached_result = self.cache.get(identification, None)
            if cached_result:
                return cached_result
            result = self.execute_request(self.services[service], args, method)
            self.cache[identification] = result
            return result
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Service {} is not available'.format(service))

    def execute_request(self, url, args, method):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param args: given args - either url args for GET or dict for POST
        :param method: GET/POST
        :return: obtained response
        """
        if method == 'GET':
            return requests.get(url + args)
        else:
            return requests.post(url, data=args)
