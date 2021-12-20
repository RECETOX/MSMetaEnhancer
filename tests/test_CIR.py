import asyncio
import pytest

from MSMetaEnhancer.libs.services.CIR import CIR
from tests.utils import wrap_with_session


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(CIR, 'casno_to_smiles', ['7783-89-3']))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    casno = '7783-89-3'
    args = '{}/smiles?resolver=cas_number'.format(casno)
    response = asyncio.run(wrap_with_session(CIR, 'query_the_service', ['CIR', args]))

    assert type(response) == str


def test_get_conversions():
    jobs = CIR(None).get_conversion_functions()
    assert ("smiles", "inchikey", "CIR") in jobs
