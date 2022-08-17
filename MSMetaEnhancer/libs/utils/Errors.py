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
    async def raise_exception(*args, **kwargs):
        raise ServiceNotAvailable('Service not available.')


class UnknownResponse(Exception):
    pass


class InvalidAttributeFormat(Exception):
    pass


class DataAlreadyPresent(Exception):
    pass
