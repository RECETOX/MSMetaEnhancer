import asyncio
import mock
import pytest
from aiohttp import ServerDisconnectedError
from aiohttp import web

from libs.services.Converter import Converter
from libs.utils.Errors import DataNotRetrieved, ConversionNotSupported


def test_query_the_service():
    converter = Converter(mock.Mock())
    converter.services = {'CTS': 'what a service'}
    converter.loop_request = mock.AsyncMock(return_value={'smiles': '$SMILES'})

    result = asyncio.run(converter.query_the_service('CTS', 'arg'))
    assert result == {'smiles': '$SMILES'}
    converter.loop_request.assert_called()

    # test wrong arg type
    result = asyncio.run(converter.query_the_service('CTS', 10))
    assert result is None

    # test lru_cache
    converter.executed = False
    converter.loop_request = mock.AsyncMock()

    result = asyncio.run(converter.query_the_service('CTS', 'arg'))
    assert result == {'smiles': '$SMILES'}
    converter.loop_request.assert_not_called()


async def test_loop_request(test_client):
    response = {'smiles': '$SMILES'}

    async def fake_request(request):
        return web.Response(body=response)

    def create_app(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', fake_request)
        return app

    session = await test_client(create_app)
    converter = Converter(session)
    converter.process_request = mock.AsyncMock(return_value=response)

    result = await converter.loop_request('/', 'GET', None)
    assert result == response


async def test_loop_request_fail(test_client):
    async def fake_request(request):
        raise ServerDisconnectedError()

    def create_app(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', fake_request)
        return app

    session = await test_client(create_app)
    converter = Converter(session)

    result = await converter.loop_request('/', 'GET', None)
    assert result is None


@pytest.mark.parametrize('ok, expected, status', [
    [True, 'this is response', 200],
    [False, None, 503],
    [False, None, 500]
])
def test_process_request(ok, expected, status):
    converter = Converter(mock.Mock())
    converter.loop_request = mock.AsyncMock(return_value=None)

    response = mock.AsyncMock()
    response.status = status
    response.text = mock.AsyncMock(return_value='this is response')
    response.ok = ok
    result = asyncio.run(converter.process_request(response, '/', 'GET', None, 10))
    assert result == expected


def test_convert():
    converter = Converter(mock.Mock())
    converter.A_to_B = mock.AsyncMock()
    converter.A_to_B.side_effect = ['value']

    result = asyncio.run(converter.convert('A', 'B', None))
    assert result == 'value'

    converter.A_to_B.side_effect = [None]
    with pytest.raises(DataNotRetrieved):
        _ = asyncio.run(converter.convert('A', 'B', None))

    with pytest.raises(ConversionNotSupported):
        _ = asyncio.run(converter.convert('B', 'C', None))
