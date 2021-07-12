import aiohttp


async def wrap_with_session(converter, method, args):
    async with aiohttp.ClientSession() as session:
        converter = converter(session)
        return await getattr(converter, method)(*args)
