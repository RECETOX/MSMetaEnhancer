from MSMetaEnhancer.libs.Converter import Converter


class ComputeConverter(Converter):
    """
    General class for computation conversion.
    """
    async def convert(self, source, target, data):
        return getattr(self, f'{source}_to_{target}')(data)
