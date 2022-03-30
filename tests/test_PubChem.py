import asyncio
import json
import pytest

from MSMetaEnhancer.libs.converters.web import PubChem
from frozendict import frozendict

from tests.utils import wrap_with_session


INCHI = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(PubChem, 'inchi_to_inchikey', [INCHI]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
    data = frozendict({'inchi': inchi})

    response = asyncio.run(wrap_with_session(PubChem, 'query_the_service',
                                             ['PubChem', 'inchi/JSON', 'POST', frozendict(data)]))
    response_json = json.loads(response)
    assert 'PC_Compounds' in response_json
    assert len(response_json['PC_Compounds']) > 0
    assert 'props' in response_json['PC_Compounds'][0]


def test_get_conversions():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    jobs = PubChem(None).get_conversion_functions()
    loop.close()

    assert ('inchi', 'iupac_name', 'PubChem') in jobs


@pytest.mark.parametrize('response, expected', [
    [{"PC_Compounds": [{"id": {"id": {"cid": "123"}},
                        "props": [{"urn": {"label": "InChI"}, "value": {"sval": "random_inchi"}}]}]},
     {"pubchemid": "123", "inchi": "random_inchi"}],
    [{"PC_Compounds": [{"id": {}, "props": []}]}, dict()]
])
def test_parse_attributes(response, expected):
    actual = PubChem(None).parse_attributes(json.dumps(response))
    assert actual == expected
