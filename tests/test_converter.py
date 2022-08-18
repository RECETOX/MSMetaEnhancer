import asyncio

import mock
import pytest
from aiohttp import web
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp import ClientConnectorError
from asyncio.exceptions import TimeoutError
import os

from MSMetaEnhancer.libs.converters.web.WebConverter import WebConverter
from MSMetaEnhancer.libs.utils.Errors import TargetAttributeNotRetrieved, UnknownResponse, ServiceNotAvailable


def test_query_the_service():
    converter = WebConverter(mock.Mock())
    converter.endpoints = {'CTS': 'what a converter'}
    converter.loop_request = mock.AsyncMock(return_value={'smiles': '$SMILES'})

    result = asyncio.run(converter.query_the_service('CTS', 'arg'))
    assert result == {'smiles': '$SMILES'}
    converter.loop_request.assert_called()

    # test wrong arg type
    with pytest.raises(TypeError):
        _ = asyncio.run(converter.query_the_service('CTS', 10))

    # test lru_cache
    converter.executed = False
    converter.loop_request = mock.AsyncMock()

    result = asyncio.run(converter.query_the_service('CTS', 'arg'))
    assert result == {'smiles': '$SMILES'}
    converter.loop_request.assert_not_called()


async def test_loop_request(aiohttp_client):
    response = {'smiles': '$SMILES'}

    async def fake_request(request):
        return web.Response(body=response)

    def create_app(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', fake_request)
        return app

    session = await aiohttp_client(create_app)
    converter = WebConverter(session)
    converter.process_request = mock.AsyncMock(return_value=response)

    result = await converter.loop_request('/', 'GET', None, None)
    assert result == response


async def test_loop_request_fail(aiohttp_client):
    async def fake_request(request):
        raise ServerDisconnectedError()

    def create_app(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', fake_request)
        return app

    session = await aiohttp_client(create_app)
    converter = WebConverter(session)

    with pytest.raises(UnknownResponse):
        await converter.loop_request('/', 'GET', None, None)


@pytest.fixture(params=[TimeoutError, ServerDisconnectedError, ClientConnectorError(None, OSError())])
def failing_session_mock(request):
    session = mock.AsyncMock()
    session.get = mock.Mock(side_effect=request.param)
    session.post = mock.Mock(side_effect=request.param)
    yield session


async def test_loop_request_circuit_breaker_get(failing_session_mock):
    converter = WebConverter(failing_session_mock)

    with pytest.raises(ServiceNotAvailable):
        await converter.loop_request('/', 'GET', None, None)


async def test_loop_request_circuit_breaker_post(failing_session_mock):
    converter = WebConverter(failing_session_mock)
    data = {'inchi': 'inchi'}

    with pytest.raises(ServiceNotAvailable):
        await converter.loop_request('/', 'POST', data, None)


def test_process_request():
    converter = WebConverter(mock.Mock())
    converter.loop_request = mock.AsyncMock(return_value=None)

    response = mock.AsyncMock()
    response.status = 200
    response.text = mock.AsyncMock(return_value='this is response')
    response.ok = True

    result = asyncio.run(converter.process_request(response, '/', 'GET'))
    assert result == 'this is response'


@pytest.mark.parametrize('ok, status', [
    [False, 500],
    [False, 503]
])
def test_process_request_exception(ok, status):
    converter = WebConverter(mock.Mock())
    converter.loop_request = mock.AsyncMock(return_value=None)

    response = mock.AsyncMock()
    response.status = status
    response.text = mock.AsyncMock(return_value='this is response')
    response.ok = ok

    with pytest.raises(UnknownResponse):
        asyncio.run(converter.process_request(response, '/', 'GET'))


def test_convert():
    converter = WebConverter(mock.Mock())
    converter.A_to_B = mock.AsyncMock()
    converter.A_to_B.side_effect = ['value']

    result = asyncio.run(converter.convert('A', 'B', None))
    assert result == 'value'

    converter.A_to_B.side_effect = [None]
    with pytest.raises(TargetAttributeNotRetrieved):
        _ = asyncio.run(converter.convert('A', 'B', None))

    with pytest.raises(AttributeError):
        _ = asyncio.run(converter.convert('B', 'C', None))


async def test_lru_cache(aiohttp_client):
    def create_app(loop):
        app = web.Application(loop=loop)
        return app

    session = await aiohttp_client(create_app)
    converter = WebConverter(session)
    converter.endpoints = {'/': '/'}
    converter.loop_request = mock.AsyncMock(return_value=(1, 2, 3))

    converter.query_the_service.cache_clear()

    _ = await converter.query_the_service('/', '')
    assert converter.query_the_service.cache_info().hits == 0

    _ = await converter.query_the_service('/', '')
    assert converter.query_the_service.cache_info().hits == 1

    _ = await converter.query_the_service('/', '')
    assert converter.query_the_service.cache_info().hits == 2
