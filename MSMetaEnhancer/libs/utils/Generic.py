def escape_single_quotes(f):
    async def wrapper(self, arg):
        return await f(self, arg.replace("'", "\\'"))
    return wrapper


def string_to_seconds(string):
    """
    Convert generic H:M:S string to seconds.
    """
    return sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
