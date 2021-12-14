import asyncio
import json
import pytest

from MSMetaEnhancer.libs.services.CTS import CTS
from tests.utils import wrap_with_session


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(CTS, 'casno_to_inchikey', ['7783-89-3']))


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('value, size', [
    ['7783-89-3', 1],
    ['7783893', 0]
])
def test_format(value, size):
    args = 'CAS/InChIKey/{}'.format(value)
    response = asyncio.run(wrap_with_session(CTS, 'query_the_service', ['CTS', args]))
    response_json = json.loads(response)
    assert type(response_json) == list
    assert len(response_json) == 1
    assert 'results' in response_json[0]
    assert len(response_json[0]['results']) == size


def test_get_conversions():
    jobs = CTS(None).get_conversion_functions()
    assert ("inchikey", "name", "CTS") in jobs
