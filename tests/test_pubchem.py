import asyncio
import pytest

from pyMSPannotator.libs.services.PubChem import PubChem
from frozendict import frozendict

from tests.utils import wrap_with_session


INCHI = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
WRONG_INCHI = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'


@pytest.mark.parametrize('arg, value, expected, method', [
    ['inchikey', INCHI, 'DHVXXNFWDPJSOI-UHFFFAOYSA-N', 'inchi_to_inchikey'],
    ['inchi', '3-Methyl-5-[p-fluorophenyl]-2H-1,3-[3H]-oxazine-2,6-dione', INCHI, 'name_to_inchi'],
    ['iupac_name', INCHI, '5-(4-fluorophenyl)-3-methyl-1,3-oxazine-2,6-dione', 'inchi_to_iupac_name'],
    ['formula', INCHI, 'C11H8FNO3', 'inchi_to_formula'],
    ['smiles', INCHI, 'CN1C=C(C(=O)OC1=O)C2=CC=C(C=C2)F', 'inchi_to_smiles']
])
def test_correct_behavior(arg, value, expected, method):
    assert asyncio.run(wrap_with_session(PubChem, method, [value]))[arg] == expected


@pytest.mark.parametrize('arg, value, method', [
    ['inchikey', WRONG_INCHI, 'inchi_to_inchikey'],
    ['inchi', 'L-Alanne', 'name_to_inchi'],
    ['iupac_name', WRONG_INCHI, 'inchi_to_iupac_name'],
    ['formula', WRONG_INCHI, 'inchi_to_formula'],
    ['smiles', WRONG_INCHI, 'inchi_to_smiles']
])
def test_incorrect_behavior(arg, value, method):
    assert len(asyncio.run(wrap_with_session(PubChem, method, [value]))) == 0


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

    response = asyncio.run(wrap_with_session(PubChem, 'query_the_service',
                                             ['PubChem', '', 'POST', frozendict(data),
                                              frozendict({"Accept": "application/sparql-results+json"})]))
    response_json = eval(response)
    assert 'results' in response_json
    assert 'bindings' in response_json['results']
    assert len(response_json['results']['bindings']) > 1
