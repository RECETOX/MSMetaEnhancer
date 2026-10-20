import asyncio
import json
from urllib.parse import parse_qs

import mock
import pytest

from MSMetaEnhancer.libs.converters.web import Wikidata
from tests.utils import wrap_with_session


def test_get_conversions():
    conversions = Wikidata(None).get_conversion_functions()

    assert ("compound_name", "casno", "Wikidata") in conversions
    assert ("compound_name", "inchi", "Wikidata") in conversions
    assert ("compound_name", "inchikey", "Wikidata") in conversions
    assert ("compound_name", "canonical_smiles", "Wikidata") in conversions
    assert ("compound_name", "pubchemid", "Wikidata") in conversions
    assert ("casno", "compound_name", "Wikidata") in conversions
    assert ("casno", "inchi", "Wikidata") in conversions
    assert ("casno", "inchikey", "Wikidata") in conversions
    assert ("casno", "canonical_smiles", "Wikidata") in conversions
    assert ("casno", "pubchemid", "Wikidata") in conversions


def test_from_name_queries_wikidata_and_parses_attributes():
    converter = Wikidata(None)
    converter.query_the_service = mock.AsyncMock(
        return_value=json.dumps(
            {
                "results": {
                    "bindings": [
                        {
                            "compound_name": {"value": "Aspirin"},
                            "casno": {"value": "50-78-2"},
                            "inchi": {"value": "InChI=1S/C9H8O4"},
                            "inchikey": {"value": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"},
                            "canonical_smiles": {
                                "value": "CC(=O)OC1=CC=CC=C1C(=O)O"
                            },
                            "pubchemid": {"value": "2244"},
                        }
                    ]
                }
            }
        )
    )

    result = asyncio.run(converter.from_name("aspirin"))

    converter.query_the_service.assert_called_once()
    service, args = converter.query_the_service.call_args.args[:2]
    query_params = parse_qs(args)
    assert service == "Wikidata"
    assert query_params["format"] == ["json"]
    assert 'mwapi:search "aspirin"' in query_params["query"][0]
    assert result == {
        "compound_name": "Aspirin",
        "casno": "50-78-2",
        "inchi": "InChI=1S/C9H8O4",
        "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "canonical_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "pubchemid": "2244",
    }


def test_from_casno_queries_cas_property():
    converter = Wikidata(None)
    converter.query_the_service = mock.AsyncMock(
        return_value=json.dumps(
            {
                "results": {
                    "bindings": [
                        {
                            "compound_name": {"value": "Aspirin"},
                            "casno": {"value": "50-78-2"},
                        }
                    ]
                }
            }
        )
    )

    result = asyncio.run(converter.from_casno("50-78-2"))

    _, args = converter.query_the_service.call_args.args[:2]
    query = parse_qs(args)["query"][0]
    assert "?item wdt:P231 ?casno ." in query
    assert 'FILTER(?casno = "50-78-2")' in query
    assert result == {"compound_name": "Aspirin", "casno": "50-78-2"}


@pytest.mark.dependency()
def test_aspirin_name_lookup_live():
    result = asyncio.run(wrap_with_session(Wikidata, "from_name", ["aspirin"]))

    assert result["casno"] == "50-78-2"
    assert result["canonical_smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
    assert result["pubchemid"] == "2244"


@pytest.mark.dependency(depends=["test_aspirin_name_lookup_live"])
def test_aspirin_cas_lookup_live():
    result = asyncio.run(wrap_with_session(Wikidata, "from_casno", ["50-78-2"]))

    assert result["compound_name"] == "aspirin"
