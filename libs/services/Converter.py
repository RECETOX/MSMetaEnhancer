import requests


class Converter:
    @staticmethod
    def fix_cas_number(cas_number):
        """
        Adds dashes to CAS number.

        :param cas_number: given CAS number without dashes
        :return: CAS number enriched by dashes
        """
        return cas_number[:-3] + "-" + cas_number[-3:-1] + "-" + cas_number[-1]

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
