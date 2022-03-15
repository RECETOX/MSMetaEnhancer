from MSMetaEnhancer.libs.converters.web import *
from MSMetaEnhancer.libs.converters.web import __all__ as web_converters
from MSMetaEnhancer.libs.converters.compute import *
from MSMetaEnhancer.libs.converters.compute import __all__ as compute_converters
from MSMetaEnhancer.libs.utils.Errors import UnknownConverter


class ConverterBuilder:
    @staticmethod
    def validate_converters(converters):
        """
        Check if converters do exist.
        Raises UnknownConverter if a converter does not exist.

        :param converters: given list of converters names
        """
        for converter in converters:
            try:
                eval(converter)
            except NameError:
                raise UnknownConverter(f'Converter {converter} unknown.')

    @staticmethod
    def build_converters(session, converters: list):
        """
        Create provided converters.

        :param session: given aiohttp session
        :param converters: list of converters to be built
        :return: built converters
        """
        built_web_converters, built_converters = dict(), dict()
        for converter in converters:
            if converter in web_converters:
                built_web_converters[converter] = eval(converter)(session)
            elif converter in compute_converters:
                built_converters[converter] = eval(converter)()
        built_converters.update(built_web_converters)
        return built_converters, built_web_converters
