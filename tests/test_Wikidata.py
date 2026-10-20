import asyncio
import json
from urllib.parse import parse_qs

import mock
import pytest

from MSMetaEnhancer.libs.converters.web import Wikidata
from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
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
    assert ("wikidataid", "casno", "Wikidata") in conversions
    assert ("pubchemid", "inchi", "Wikidata") in conversions
    assert ("inchi", "inchikey", "Wikidata") in conversions
    assert ("inchikey", "compound_name", "Wikidata") in conversions


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


@pytest.mark.parametrize(
    "method, identifier, query_fragment",
    [
        ("from_wikidataid", "Q18216", "BIND(wd:Q18216 AS ?item)"),
        (
            "from_pubchemid",
            "2244",
            'wdt:P662 ?identifier',
        ),
        (
            "from_inchi",
            "InChI=1S/C9H8O4",
            "wdt:P234 ?identifier",
        ),
        (
            "from_inchikey",
            "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
            "wdt:P235 ?identifier",
        ),
    ],
)
def test_identifier_lookups(method, identifier, query_fragment):
    converter = Wikidata(None)
    converter.query_the_service = mock.AsyncMock(
        return_value=json.dumps(
            {
                "results": {
                    "bindings": [
                        {
                            "compound_name": {"value": "aspirin"},
                            "pubchemid": {"value": "2244"},
                            "wikidataid": {"value": "Q18216"},
                        }
                    ]
                }
            }
        )
    )

    result = asyncio.run(getattr(converter, method)(identifier))

    query = parse_qs(converter.query_the_service.call_args.args[1])["query"][0]
    assert query_fragment in query
    if method != "from_wikidataid":
        assert f'FILTER(STR(?identifier) = "{identifier}")' in query
    assert result == {
        "compound_name": "aspirin",
        "pubchemid": "2244",
        "wikidataid": "Q18216",
    }


def test_from_wikidataid_rejects_invalid_ids():
    converter = Wikidata(None)
    converter.query_the_service = mock.AsyncMock()

    result = asyncio.run(converter.from_wikidataid("Q1 } SERVICE"))

    assert result == {}
    converter.query_the_service.assert_not_called()


@pytest.mark.dependency()
def test_aspirin_name_lookup_live():
    result = asyncio.run(wrap_with_session(Wikidata, "from_name", ["aspirin"]))

    assert result["casno"] == "50-78-2"
    assert result["canonical_smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
    assert result["pubchemid"] == "2244"


@pytest.mark.dependency(depends=["test_aspirin_name_lookup_live"])
def test_aspirin_cas_lookup_live():
    result = asyncio.run(wrap_with_session(Wikidata, "from_casno", ["50-78-2"]))

    assert result["compound_name"].casefold() == "aspirin"


@pytest.mark.dependency(depends=["test_aspirin_name_lookup_live"])
@pytest.mark.xfail(raises=UnknownResponse)
@pytest.mark.parametrize(
    "method, identifier",
    [
        ("from_wikidataid", "Q18216"),
        ("from_pubchemid", "2244"),
        (
            "from_inchi",
            "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
        ),
        ("from_inchikey", "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"),
    ],
)
def test_aspirin_identifier_lookup_live(method, identifier):
    result = asyncio.run(wrap_with_session(Wikidata, method, [identifier]))

    assert result["casno"] == "50-78-2"
    assert result["canonical_smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
