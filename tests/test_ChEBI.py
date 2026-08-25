import asyncio
import json
import pytest

from MSMetaEnhancer.libs.converters.web import ChEBI
from tests.utils import wrap_with_session


CHEBI_ID = "CHEBI:60888"
INCHIKEY = "FTEDXVNDVHYDQW-UHFFFAOYSA-N"
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


def test_parse_entity_nested_response():
    response = json.dumps(
        {
            "chebi_accession": CHEBI_ID,
            "name": "bapta",
            "chemical_data": {"formula": "C22H22N2O10"},
            "default_structure": {
                "smiles": "C1=CC=C(C=C1)O",
                "standard_inchi": "InChI=1S/C6H6O/c7-6-4-2-1-3-5-6/h1-5,7H",
                "standard_inchi_key": INCHIKEY,
            },
        }
    )

    parsed = ChEBI(None).parse_entity(response)

    assert parsed == {
        "chebiid": CHEBI_ID,
        "compound_name": "bapta",
        "formula": "C22H22N2O10",
        "smiles": "C1=CC=C(C=C1)O",
        "inchi": "InChI=1S/C6H6O/c7-6-4-2-1-3-5-6/h1-5,7H",
        "inchikey": INCHIKEY,
    }


def test_parse_search_response_source():
    response = json.dumps(
        {
            "results": [
                {
                    "_source": {
                        "chebi_accession": CHEBI_ID,
                        "ascii_name": COMPOUND_NAME,
                        "formula": "C22H22N2O10",
                        "smiles": "NCCO",
                        "inchi": "InChI=1S/C2H7NO/c3-1-2-4/h4H,1-3H2",
                        "standard_inchi_key": INCHIKEY,
                    }
                }
            ]
        }
    )

    parsed = ChEBI(None).parse_search_results(response)

    assert parsed == {
        "chebiid": CHEBI_ID,
        "compound_name": COMPOUND_NAME,
        "formula": "C22H22N2O10",
        "smiles": "NCCO",
        "inchi": "InChI=1S/C2H7NO/c3-1-2-4/h4H,1-3H2",
        "inchikey": INCHIKEY,
    }


def test_get_conversions():
    jobs = ChEBI(None).get_conversion_functions()
    assert ("chebiid", "inchikey", "ChEBI") in jobs
    assert ("inchikey", "chebiid", "ChEBI") in jobs
    assert ("compound_name", "chebiid", "ChEBI") in jobs
