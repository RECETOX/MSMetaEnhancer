from abc import ABC, abstractmethod


class Converter(ABC):
    """
    General class for conversions.
    """
    def __init__(self):
        self.is_available = True

    @property
    def converter_name(self):
        return self.__class__.__name__

    def __hash__(self):
        return hash(self.converter_name)

    @abstractmethod
    async def convert(self, source, target, data):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :return: obtained value of target attribute
        """
        pass

    def create_top_level_conversion_methods(self, conversions, asynch=True):
        """
        Method to create and set dynamic methods defined in conversions

        :param conversions: triples of form (from, to, method)
        :param asynch: whether to create asynchronous methods
        """
        for conversion in conversions:
            create_top_level_method(self, *conversion, asynch)

    def get_conversion_functions(self) -> list:
        """
        Method to compute all available conversion functions.

        Assumes that the functions always have from {source}_to_{target}

        :return: a list of available conversion functions
        """
        available_conversions = []
        methods = [method_name for method_name in dir(self) if '_to_' in method_name]
        for method in methods:
            available_conversions.append((*method.split('_to_'), self.converter_name))
        return available_conversions


def create_top_level_method(obj: Converter, source: str, target: str, method: str, asynch: bool = True):
    """
    Assign a new method to {obj} called {source}_to_{target} which calls {method}.

    :param obj: given object (typically a Converter)
    :param source: attribute name used as source of data
    :param target: attribute name obtained using this dynamic method
    :param method: method which is called in the object with single argument
    :param asynch: whether to create asynchronous methods
    """
    async def async_conversion(key):
        return await getattr(obj, str(method))(key)

    def sync_conversion(key):
        return getattr(obj, str(method))(key)

    doc = f'Convert {source} to {target} using {obj.__class__.__name__} converter'
    name = f'{source}_to_{target}'

    if asynch:
        async_conversion.__doc__ = doc
        async_conversion.__name__ = name
        setattr(obj, async_conversion.__name__, async_conversion)
    else:
        sync_conversion.__doc__ = doc
        sync_conversion.__name__ = name
        setattr(obj, sync_conversion.__name__, sync_conversion)
