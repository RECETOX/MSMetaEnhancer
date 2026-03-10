from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter
from MSMetaEnhancer.libs.converters.compute.ComputeConverter import ComputeConverter
from MSMetaEnhancer.libs.utils.Errors import UnknownConverter


class ConverterBuilder:
    converters: dict[str, type] = {}

    @staticmethod
    def register(converters: list[type]):
        for converter in converters:
            ConverterBuilder.converters[converter.__name__] = converter

    @staticmethod
    def validate_converters(converters):
        """
        Check if converters do exist.
        Raises UnknownConverter if a converter does not exist.

        :param converters: given list of converters names
        """
        for converter in converters:
            if ConverterBuilder.converters.get(converter) is None:
                raise UnknownConverter(f"Converter {converter} unknown.")

    @staticmethod
    def build_converters(session, converters: list[str]):
        """
        Create provided converters.

        :param session: given aiohttp session
        :param converters: list of converters to be built
        :return: built converters
        """
        web_converters, compute_converters = {}, {}
        for converter in converters:
            if issubclass(ConverterBuilder.converters[converter], WebConverter):
                web_converters[converter] = ConverterBuilder.converters[converter](
                    session
                )
            elif issubclass(ConverterBuilder.converters[converter], ComputeConverter):
                compute_converters[converter] = ConverterBuilder.converters[converter]()
        return compute_converters, web_converters
