import asyncio
import pytest

from MSMetaEnhancer.libs.converters.web import IDSM
from frozendict import frozendict

from tests.utils import wrap_with_session


INCHI = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(IDSM, 'inchi_to_inchikey', [INCHI]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'

    query = f"""
    SELECT DISTINCT ?value ?type
    WHERE
    {{
      ?attribute rdf:type ?type.
      ?attribute sio:has-value ?value.
      ?substance sio:has-attribute ?attribute.
      ?substance sio:has-attribute ?inchi.
      ?inchi sio:has-value "{inchi}"@en.
    }}
    """

    data = frozendict({"query": query})

    response = asyncio.run(wrap_with_session(IDSM, 'query_the_service',
                                             ['IDSM', '', 'POST', frozendict(data),
                                              frozendict({"Accept": "application/sparql-results+json"})]))
    response_json = eval(response)
    assert 'results' in response_json
    assert 'bindings' in response_json['results']
    assert len(response_json['results']['bindings']) > 1


def test_get_conversions():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    jobs = IDSM(None).get_conversion_functions()
    loop.close()

    assert ("inchi", "iupac_name", "IDSM") in jobs
