import asyncio
from io import StringIO
import pandas as pd
import pytest

from MSMetaEnhancer.libs.services.NLM import NLM
from tests.utils import wrap_with_session


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(NLM, 'inchikey_to_compound_name', ['QNAYBMKLOCPYGJ-REOHCLBHSA-N']))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
    args = 'inchikey/equals/{}?data=summary&format=tsv'.format(inchikey)
    response = asyncio.run(wrap_with_session(NLM, 'query_the_service', ['NLM', args]))

    table = pd.read_csv(StringIO(response), sep='\t')
    assert not table.empty


def test_get_conversions():
    jobs = NLM(None).get_conversion_functions()
    assert ("compound_name", "inchikey", "NLM") in jobs
