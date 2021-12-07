import asyncio
import pytest

from MSMetaEnhancer.libs.services.CIR import CIR
from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
from tests.utils import wrap_with_session


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(CIR, 'casno_to_smiles', ['7783-89-3']))


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('arg, value, expected, method', [
    ['smiles', '7783-89-3', '[Ag+].[O-][Br](=O)=O', 'casno_to_smiles'],
    ['smiles', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', '[Ag+].[O-][Br](=O)=O', 'inchikey_to_smiles'],
    ['inchi', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', 'InChI=1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1', 'inchikey_to_inchi'],
    ['casno', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', '7783-89-3', 'inchikey_to_casno'],
    ['formula', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', 'AgBrO3', 'inchikey_to_formula'],
    ['inchikey', '[Ag+].[O-][Br](=O)=O', 'XQLMNMQWVCXIKR-UHFFFAOYSA-M', 'smiles_to_inchikey']
])
def test_correct_behavior(arg, value, expected, method):
    assert asyncio.run(wrap_with_session(CIR, method, [value]))[arg] == expected


@pytest.mark.dependency(depends=["test_service_available"])
@pytest.mark.parametrize('arg, value, method', [
    ['smiles', '7783893', 'casno_to_smiles'],
    ['smiles', 'XQLMNVCXIKR-UHFFFAOYSA-M', 'inchikey_to_smiles'],
    ['inchi', 'XQLMNVCXIKR-UHFFFAOYSA-M', 'inchikey_to_inchi'],
    ['casno', 'XQLMNVCXIKR-UHFFFAOYSA-M', 'inchikey_to_casno'],
    ['formula', 'XQLMNVCXIKR-UHFFFAOYSA-M', 'inchikey_to_formula'],
    ['inchikey', '[Ag+].O-][Br](=O)=O', 'smiles_to_inchikey']
])
def test_incorrect_behavior(arg, value, method):
    with pytest.raises(UnknownResponse):
        asyncio.run(wrap_with_session(CIR, method, [value]))


def test_get_conversions():
    jobs = CIR(None).get_conversion_functions()
    assert ("smiles", "inchikey", "CIR") in jobs
