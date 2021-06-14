import requests


class Converter:
    def connect_to_service(self, service, args):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :return: obtained response
        """
        try:
            return requests.get(self.services[service] + args)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Service {} is not available'.format(service))
