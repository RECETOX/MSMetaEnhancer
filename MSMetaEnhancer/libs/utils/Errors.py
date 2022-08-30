class ConversionNotSupported(Exception):
    pass


class TargetAttributeNotRetrieved(Exception):
    pass


class UnknownConverter(Exception):
    pass


class UnknownSpectraFormat(Exception):
    pass


class SourceAttributeNotAvailable(Exception):
    pass


class ServiceNotAvailable(Exception):
    @staticmethod
    async def raise_circuitbreaker(*args):
        converter_name = args[0].converter_name
        raise ServiceNotAvailable(f'Service {converter_name} not available.')


class UnknownResponse(Exception):
    pass


class InvalidAttributeFormat(Exception):
    pass


class DataAlreadyPresent(Exception):
    pass
