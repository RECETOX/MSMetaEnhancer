import asyncio
from io import StringIO
import pandas as pd
import pytest

from MSMetaEnhancer.libs.services.NLM import NLM
from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
from tests.utils import wrap_with_session


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(NLM, 'inchikey_to_name', ['QNAYBMKLOCPYGJ-REOHCLBHSA-N']))


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('arg, value, expected, method', [
    ['name', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', 'Alanine [USAN:INN]', 'inchikey_to_name'],
    ['inchikey', 'L-Alanine', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', 'name_to_inchikey'],
    ['formula', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', 'C3-H7-N-O2', 'inchikey_to_formula'],
    ['casno', 'QNAYBMKLOCPYGJ-REOHCLBHSA-N', '56-41-7', 'inchikey_to_casno'],
    ['formula', 'L-Alanine', 'C3-H7-N-O2', 'name_to_formula'],
    ['casno', 'L-Alanine', '56-41-7', 'name_to_casno']
])
def test_correct_behavior(arg, value, expected, method):
    assert asyncio.run(wrap_with_session(NLM, method, [value]))[arg] == expected


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('arg, value, method', [
    ['name', 'QNAYBMLOXXXXGJ-REOHCLBHSA-N', 'inchikey_to_name'],
    ['inchikey', 'L-Alanne', 'name_to_inchikey'],
    ['formula', 'L-Alanne', 'name_to_formula'],
    ['casno', 'L-Alanne', 'name_to_casno']
])
def test_incorrect_behavior_exception(arg, value, method):
    with pytest.raises(UnknownResponse):
        asyncio.run(wrap_with_session(NLM, method, [value]))


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('arg, value, method', [
    ['name', 'QNAYMLGJ-REOLBHSA-N', 'inchikey_to_name'],
    ['formula', 'QNAYMLGJ-REOLBHSA-N', 'inchikey_to_formula'],
    ['casno', 'QNAYMLGJ-REOLBHSA-N', 'inchikey_to_casno']
])
def test_incorrect_behavior_none(arg, value, method):
    assert asyncio.run(wrap_with_session(NLM, method, [value])) is None


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
    args = 'inchikey/equals/{}?data=summary&format=tsv'.format(inchikey)
    response = asyncio.run(wrap_with_session(NLM, 'query_the_service', ['NLM', args]))

    table = pd.read_csv(StringIO(response), sep='\t')
    assert not table.empty


def test_get_conversions():
    jobs = NLM(None).get_conversions()
    assert ("name", "inchikey", "NLM") in jobs
