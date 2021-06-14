import requests


class Converter:
    def __init__(self):
        # used to store individual API calls to avoid executing
        # the same query multiple times in single session
        self.cache = dict()

    def connect_to_service(self, service, args):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :return: obtained response
        """
        try:
            identification = service + ":" + args
            cached_result = self.cache.get(identification, None)
            if cached_result:
                return cached_result
            result = requests.get(self.services[service] + args)
            self.cache[identification] = result
            return result
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Service {} is not available'.format(service))
