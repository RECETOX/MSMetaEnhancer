import asyncio
import pytest

from MSMetaEnhancer.libs.converters.web import IDSM
from frozendict import frozendict

from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
from tests.utils import wrap_with_session


INCHI = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'


@pytest.mark.xfail(raises=UnknownResponse)
@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(IDSM, 'inchi_to_inchikey', [INCHI]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    query = f"""
    SELECT DISTINCT ?value ?type
    FROM pubchem:compound FROM pubchem:inchikey FROM descriptor:compound
    WHERE
    {{
      ?compound sio:SIO_000008 [
        rdf:type ?type;
        sio:SIO_000300 ?value ].
      ?compound sio:SIO_000008 [
        rdf:type sio:CHEMINF_000396;
        sio:SIO_000300 '{INCHI}'@en ].
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
