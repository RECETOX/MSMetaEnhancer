import math


NA_STRING_VALUES = {"na", "n/a", "nan", "none", ""}
USER_AGENT = "MSMetaEnhancer (https://github.com/RECETOX/MSMetaEnhancer)"

def is_na_value(value) -> bool:
    """Check if a value should be treated as NA/missing (e.g. empty, None, NaN, 'NA')."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip().lower() in NA_STRING_VALUES:
        return True
    return False


CAS_MIN_DIGITS = 5
CAS_MAX_DIGITS = 10


def fix_cas_number(cas_number):
    """
    Add dashes to an unhyphenated CAS number.

    '50782' becomes '50-78-2'. Anything that cannot be a CAS number is returned
    unchanged: values that are not strings, that already contain dashes, or that
    are not made up of the 5-10 digits a CAS RN contains (2-7 digits, 2 digits,
    1 check digit).

    :param cas_number: given CAS number
    :return: CAS number enriched by dashes (if needed)
    """
    if isinstance(cas_number, str):
        digits = cas_number.strip()
        if digits.isdigit() and CAS_MIN_DIGITS <= len(digits) <= CAS_MAX_DIGITS:
            return f"{digits[:-3]}-{digits[-3:-1]}-{digits[-1]}"
    return cas_number


def escape_single_quotes(f):
    async def wrapper(self, arg):
        return await f(self, arg.replace("'", "\\'"))

    return wrapper


def string_to_seconds(string):
    """
    Convert generic H:M:S string to seconds.
    """
    return sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
