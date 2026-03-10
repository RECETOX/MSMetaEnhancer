import math


NA_STRING_VALUES = {"na", "n/a", "nan", "none", ""}


def is_na_value(value) -> bool:
    """Check if a value should be treated as NA/missing (e.g. empty, None, NaN, 'NA')."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip().lower() in NA_STRING_VALUES:
        return True
    return False


def escape_single_quotes(f):
    async def wrapper(self, arg):
        return await f(self, arg.replace("'", "\\'"))

    return wrapper


def string_to_seconds(string):
    """
    Convert generic H:M:S string to seconds.
    """
    return sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
