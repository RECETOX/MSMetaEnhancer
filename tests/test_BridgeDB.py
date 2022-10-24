import asyncio
import pytest

from MSMetaEnhancer.libs.converters.web import BridgeDb
from tests.utils import wrap_with_session


HMDBID = 'HMDB0000001'


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(BridgeDb, 'hmdbid_to_pubchemid', ['HMDB0000001']))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    args = f'Ch/{HMDBID}'
    response = asyncio.run(wrap_with_session(BridgeDb, 'query_the_service', ['BridgeDB', args]))

    assert type(response) == str
    lines = response.split('\n')
    assert len(lines) != 0
    assert '\t' in response


def test_get_conversions():
    jobs = BridgeDb(None).get_conversion_functions()
    assert ('wikidataid', 'pubchemid', 'BridgeDB') in jobs
