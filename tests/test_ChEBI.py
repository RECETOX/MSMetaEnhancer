import asyncio
import json
import pytest

from MSMetaEnhancer.libs.converters.web import ChEBI
from tests.utils import wrap_with_session


CHEBI_ID = "CHEBI:60888"
INCHIKEY = "RYYVLZVUVIJVGH-UHFFFAOYSA-N"
COMPOUND_NAME = "bapta"


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchikey", [CHEBI_ID]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_inchikey():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchikey", [CHEBI_ID]))
    assert result is not None
    assert "inchikey" in result
    assert result["inchikey"] == INCHIKEY


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_smiles():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_smiles", [CHEBI_ID]))
    assert result is not None
    assert "smiles" in result


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_inchi():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchi", [CHEBI_ID]))
    assert result is not None
    assert "inchi" in result


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_formula():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_formula", [CHEBI_ID]))
    assert result is not None
    assert "formula" in result


@pytest.mark.dependency(depends=["test_service_available"])
def test_inchikey_to_chebiid():
    result = asyncio.run(wrap_with_session(ChEBI, "inchikey_to_chebiid", [INCHIKEY]))
    assert result is not None
    assert "chebiid" in result
    assert result["chebiid"] == CHEBI_ID


@pytest.mark.dependency(depends=["test_service_available"])
def test_compound_name_to_chebiid():
    result = asyncio.run(
        wrap_with_session(ChEBI, "compound_name_to_chebiid", [COMPOUND_NAME])
    )
    assert result is not None
    assert "chebiid" in result


@pytest.mark.dependency(depends=["test_service_available"])
def test_format_search_response():
    args = f"es_search/?term={INCHIKEY}&page=1&size=15"
    response = asyncio.run(
        wrap_with_session(ChEBI, "query_the_service", ["ChEBI", args])
    )

    assert isinstance(response, str)
    data = json.loads(response)
    assert "results" in data


@pytest.mark.dependency(depends=["test_service_available"])
def test_format_entity_response():
    args = f"compound/{CHEBI_ID}/"
    response = asyncio.run(
        wrap_with_session(ChEBI, "query_the_service", ["ChEBI", args])
    )

    assert isinstance(response, str)
    data = json.loads(response)
    assert "chebi_accession" in data
    assert data["chebi_accession"] == CHEBI_ID


def test_get_conversions():
    jobs = ChEBI(None).get_conversion_functions()
    assert ("chebiid", "inchikey", "ChEBI") in jobs
    assert ("inchikey", "chebiid", "ChEBI") in jobs
    assert ("compound_name", "chebiid", "ChEBI") in jobs
