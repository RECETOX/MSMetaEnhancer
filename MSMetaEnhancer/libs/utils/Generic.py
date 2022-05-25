def escape_arg(f):
    async def wrapper(self, arg):
        return await f(self, arg.replace("'", "\\'"))
    return wrapper
