import asyncio
import json

import pytest

from libs.services.PubChem import PubChem
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
    assert asyncio.run(wrap_with_session(PubChem, method, [value])) is None


def test_format():
    inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
    args = "inchi/JSON"
    response = asyncio.run(wrap_with_session(PubChem, 'query_the_service',
                                             ['PubChem', args, 'POST', frozendict({'inchi': inchi})]))
    response_json = json.loads(response)
    assert 'PC_Compounds' in response_json
    assert len(response_json['PC_Compounds']) == 1
    assert 'props' in response_json['PC_Compounds'][0]
    assert type(response_json['PC_Compounds'][0]['props']) == list
