import asyncio
import mock
import pytest

from MSMetaEnhancer.libs.converters.web import BridgeDb
from tests.utils import wrap_with_session


HMDBID = "HMDB0000001"


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(BridgeDb, "hmdbid_to_pubchemid", ["HMDB0000001"]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_format():
    args = f"Ch/{HMDBID}"
    response = asyncio.run(
        wrap_with_session(BridgeDb, "query_the_service", ["BridgeDb", args])
    )

    assert isinstance(response, str)
    lines = response.split("\n")
    assert len(lines) != 0
    assert "\t" in response


def test_get_conversions():
    jobs = BridgeDb(None).get_conversion_functions()
    assert ("wikidataid", "pubchemid", "BridgeDb") in jobs
    assert ("casno", "inchikey", "BridgeDb") in jobs
    assert ("compound_name", "pubchemid", "BridgeDb") in jobs


def test_parse_attributes_supports_system_codes():
    converter = BridgeDb(None)
    response = (
        "HMDB0000001\tCh\n"
        "962\tCpc\n"
        "CHEBI:15365\tCe\n"
        "50-78-2\tCa\n"
        "BSYNRYMUTXBXSQ-UHFFFAOYSA-N\tIk\n"
    )

    assert converter.parse_attributes(response) == {
        "hmdbid": "HMDB0000001",
        "pubchemid": "962",
        "chebiid": "CHEBI:15365",
        "casno": "50-78-2",
        "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    }


def test_from_name_uses_search_endpoint():
    converter = BridgeDb(None)
    converter.query_the_service = mock.AsyncMock(
        return_value="HMDB0000001\tCh\n962\tCpc\n"
    )

    result = asyncio.run(converter.from_name("aspirin"))

    converter.query_the_service.assert_called_once_with("BridgeDbSearch", "aspirin")
    assert result == {"hmdbid": "HMDB0000001", "pubchemid": "962"}
