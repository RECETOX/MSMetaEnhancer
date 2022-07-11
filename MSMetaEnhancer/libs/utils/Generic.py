def escape_single_quotes(f):
    async def wrapper(self, arg):
        return await f(self, arg.replace("'", "\\'"))
    return wrapper
