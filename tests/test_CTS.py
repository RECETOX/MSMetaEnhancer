import asyncio
import json
import pytest

from pyMSPannotator.libs.services.CTS import CTS
from pyMSPannotator.libs.utils.Errors import UnknownResponse
from tests.utils import wrap_with_session


@pytest.mark.parametrize('arg, value, expected, method', [
    ['inchikey', '7783-89-3', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', 'casno_to_inchikey'],
    ['inchi', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', 'InChI=1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1', 'inchikey_to_inchi'],
    ['inchikey', 'L-Alanine', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', 'name_to_inchikey'],
    ['name', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', 'L-ALANINE', 'inchikey_to_name'],
    ['iupac_name', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', '(2S)-2-azaniumylpropanoate', 'inchikey_to_iupac_name']
])
def test_correct_behavior(arg, value, expected, method):
    assert asyncio.run(wrap_with_session(CTS, method, [value]))[arg] == expected


@pytest.mark.parametrize('arg, value, method', [
    ['inchi', 'XQLMNMQIKR-UHFFFAOYSA-M', 'inchikey_to_inchi'],
    ['name', 'XQLMNMQIKR-UHFFFAOYSA-M', 'inchikey_to_name'],
    ['iupac_name', 'XQLMNMQIKR-UHFFFAOYSA-M', 'inchikey_to_iupac_name']
])
def test_incorrect_behavior_exception(arg, value, method):
    with pytest.raises(UnknownResponse):
        asyncio.run(wrap_with_session(CTS, method, [value]))


@pytest.mark.parametrize('arg, value, method', [
    ['inchikey', '7783893', 'casno_to_inchikey'],
    ['inchikey', 'L-Alalalalanine', 'name_to_inchikey']
])
def test_incorrect_behavior_none(arg, value, method):
    assert asyncio.run(wrap_with_session(CTS, method, [value])) is None


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
