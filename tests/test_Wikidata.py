import asyncio
import json
from urllib.parse import parse_qs

import mock

from MSMetaEnhancer.libs.converters.web import Wikidata


def test_get_conversions():
    conversions = Wikidata(None).get_conversion_functions()

    assert ("compound_name", "casno", "Wikidata") in conversions
    assert ("compound_name", "inchi", "Wikidata") in conversions
    assert ("compound_name", "inchikey", "Wikidata") in conversions
    assert ("casno", "compound_name", "Wikidata") in conversions
    assert ("casno", "inchi", "Wikidata") in conversions
    assert ("casno", "inchikey", "Wikidata") in conversions


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
