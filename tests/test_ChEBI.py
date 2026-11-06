import asyncio
import json
import pytest

from rdkit.Chem import MolFromInchi, MolFromSmiles, MolToInchi, MolToSmiles
from rdkit.Chem.inchi import InchiToInchiKey

from MSMetaEnhancer.libs.converters.web import ChEBI
from MSMetaEnhancer.libs.utils.Errors import UnknownResponse
from tests.utils import wrap_with_session


CHEBI_ID = "CHEBI:60888"
INCHIKEY = "FTEDXVNDVHYDQW-UHFFFAOYSA-N"
INCHI = "InChI=1S/C22H24N2O10/c25-19(26)11-23(12-20(27)28)15-5-1-3-7-17(15)33-9-10-34-18-8-4-2-6-16(18)24(13-21(29)30)14-22(31)32/h1-8H,9-14H2,(H,25,26)(H,27,28)(H,29,30)(H,31,32)"
COMPOUND_NAME = "bapta"
CHEBI_NAME = "BAPTA"
IUPAC_NAME = (
    "2,2',2'',2'''-[ethane-1,2-diylbis(oxy-2,1-phenylenenitrilo)]tetraacetic acid"
)
SMILES = "O=C(O)CN(CC(=O)O)c1ccccc1OCCOc1ccccc1N(CC(=O)O)CC(=O)O"
FORMULA = "C22H24N2O10"


# Responses below were recorded from the ChEBI API on 2026-10-29 and shortened to the
# fields the converter reads, the reported keys and values were not altered.

ENTITY_RESPONSE = json.dumps(
    {
        "id": 60888,
        "chebi_accession": CHEBI_ID,
        "name": CHEBI_NAME,
        "stars": 3,
        "ascii_name": CHEBI_NAME,
        "names": {
            "SYNONYM": [
                {
                    "name": "1,2-Bis(2-aminophenoxy)ethane-N,N,N',N'-tetraacetic acid",
                    "status": "C",
                    "type": "SYNONYM",
                    "source": "ChemIDplus",
                    "ascii_name": "1,2-Bis(2-aminophenoxy)ethane-N,N,N',N'-tetraacetic acid",
                    "adapted": False,
                    "language_code": "en",
                }
            ],
            "IUPAC NAME": [
                {
                    "name": IUPAC_NAME,
                    "status": "C",
                    "type": "IUPAC NAME",
                    "source": "IUPAC",
                    "ascii_name": IUPAC_NAME,
                    "adapted": False,
                    "language_code": "en",
                }
            ],
        },
        "chemical_data": {
            "formula": FORMULA,
            "charge": 0,
            "mass": "476.438",
            "monoisotopic_mass": "476.14309",
        },
        "default_structure": {
            "id": 2706518,
            "smiles": SMILES,
            "standard_inchi": INCHI,
            "standard_inchi_key": INCHIKEY,
            "wurcs": None,
            "is_r_group": False,
        },
        "secondary_ids": [],
    }
)

SEARCH_BAPTA_RESPONSE = json.dumps(
    {
        "results": [
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60890",
                "_score": 67.00641,
                "_source": {
                    "chebi_accession": "CHEBI:60890",
                    "name": "5,5'-dibromo-BAPTA",
                    "ascii_name": "5,5'-dibromo-BAPTA",
                    "stars": 3,
                    "default_structure": 2706528,
                    "charge": 0,
                    "formula": "C22H22Br2N2O10",
                    "inchikey": "KCTRRYZOCJDOTC-UHFFFAOYSA-N",
                },
            },
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60889",
                "_score": 65.14058,
                "_source": {
                    "chebi_accession": "CHEBI:60889",
                    "name": "5,5'-dimethyl-BAPTA",
                    "ascii_name": "5,5'-dimethyl-BAPTA",
                    "stars": 3,
                    "default_structure": 2706524,
                    "charge": 0,
                    "formula": "C24H28N2O10",
                    "inchikey": "BOMWLYNXTGNSSE-UHFFFAOYSA-N",
                },
            },
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60888",
                "_score": 35.251152,
                "_source": {
                    "chebi_accession": CHEBI_ID,
                    "name": CHEBI_NAME,
                    "ascii_name": CHEBI_NAME,
                    "stars": 3,
                    "default_structure": 2706518,
                    "charge": 0,
                    "formula": FORMULA,
                    "inchikey": INCHIKEY,
                },
            },
        ],
        "total": 3,
        "number_pages": 1,
    }
)

SEARCH_INCHIKEY_RESPONSE = json.dumps(
    {
        "results": [
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60888",
                "_score": 11.740927,
                "_source": {
                    "chebi_accession": CHEBI_ID,
                    "name": CHEBI_NAME,
                    "ascii_name": CHEBI_NAME,
                    "stars": 3,
                    "default_structure": 2706518,
                    "charge": 0,
                    "formula": FORMULA,
                    "inchikey": INCHIKEY,
                    "inchi": INCHI,
                    "smiles": SMILES,
                },
            }
        ],
        "total": 1,
        "number_pages": 1,
    }
)

SEARCH_IUPAC_RESPONSE = json.dumps(
    {
        "results": [
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60888",
                "_score": 117.740105,
                "_source": {
                    "chebi_accession": CHEBI_ID,
                    "name": CHEBI_NAME,
                    "ascii_name": CHEBI_NAME,
                    "stars": 3,
                    "default_structure": 2706518,
                    "charge": 0,
                    "formula": FORMULA,
                    "inchikey": INCHIKEY,
                    "inchi": INCHI,
                    "smiles": SMILES,
                },
            }
        ],
        "total": 1,
        "number_pages": 1,
    }
)

STRUCTURE_SEARCH_RESPONSE = json.dumps(
    {
        "results": [
            {
                "_index": "chebi-prod-compounds-29102026",
                "_type": "_doc",
                "_id": "60888",
                "_score": 1.0,
                "_source": {
                    "chebi_accession": CHEBI_ID,
                    "name": CHEBI_NAME,
                    "ascii_name": CHEBI_NAME,
                    "stars": 3,
                    "default_structure": 2706518,
                    "charge": 0,
                    "formula": FORMULA,
                    "inchikey": INCHIKEY,
                    "inchi": INCHI,
                    "smiles": SMILES,
                },
            }
        ],
        "total": 1,
        "number_pages": 1,
    }
)


@pytest.mark.dependency()
def test_service_available():
    asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchikey", [CHEBI_ID]))


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_inchikey():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchikey", [CHEBI_ID]))
    assert result is not None
    assert result["inchikey"] == INCHIKEY


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_inchi():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_inchi", [CHEBI_ID]))
    assert result is not None
    assert result["inchi"] == INCHI


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_smiles():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_smiles", [CHEBI_ID]))
    assert result is not None
    assert result["smiles"] == SMILES


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_formula():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_formula", [CHEBI_ID]))
    assert result is not None
    assert result["formula"] == FORMULA


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_compound_name():
    result = asyncio.run(
        wrap_with_session(ChEBI, "chebiid_to_compound_name", [CHEBI_ID])
    )
    assert result is not None
    assert result["compound_name"] == CHEBI_NAME


@pytest.mark.dependency(depends=["test_service_available"])
def test_chebiid_to_iupac_name():
    result = asyncio.run(wrap_with_session(ChEBI, "chebiid_to_iupac_name", [CHEBI_ID]))
    assert result is not None
    assert result["iupac_name"] == IUPAC_NAME


@pytest.mark.dependency(depends=["test_service_available"])
def test_compound_name_to_chebiid():
    result = asyncio.run(
        wrap_with_session(ChEBI, "compound_name_to_chebiid", [COMPOUND_NAME])
    )
    assert result is not None
    assert result["chebiid"] == CHEBI_ID
    assert result["compound_name"] == CHEBI_NAME


@pytest.mark.dependency(depends=["test_service_available"])
def test_compound_name_to_iupac_name():
    result = asyncio.run(
        wrap_with_session(ChEBI, "compound_name_to_iupac_name", [COMPOUND_NAME])
    )
    assert result is not None
    assert result["iupac_name"] == IUPAC_NAME


@pytest.mark.dependency(depends=["test_service_available"])
def test_inchikey_to_chebiid():
    result = asyncio.run(wrap_with_session(ChEBI, "inchikey_to_chebiid", [INCHIKEY]))
    assert result is not None
    assert result["chebiid"] == CHEBI_ID


@pytest.mark.dependency(depends=["test_service_available"])
def test_inchikey_to_iupac_name():
    result = asyncio.run(wrap_with_session(ChEBI, "inchikey_to_iupac_name", [INCHIKEY]))
    assert result is not None
    assert result["iupac_name"] == IUPAC_NAME


@pytest.mark.dependency(depends=["test_service_available"])
def test_inchi_to_chebiid():
    result = asyncio.run(wrap_with_session(ChEBI, "inchi_to_chebiid", [INCHI]))
    assert result is not None
    assert result["chebiid"] == CHEBI_ID


@pytest.mark.dependency(depends=["test_service_available"])
def test_iupac_name_to_chebiid():
    result = asyncio.run(
        wrap_with_session(ChEBI, "iupac_name_to_chebiid", [IUPAC_NAME])
    )
    assert result is not None
    assert result["chebiid"] == CHEBI_ID


@pytest.mark.dependency(depends=["test_service_available"])
def test_smiles_to_chebiid():
    result = asyncio.run(wrap_with_session(ChEBI, "smiles_to_chebiid", [SMILES]))
    assert result is not None
    assert result["chebiid"] == CHEBI_ID
    assert result["inchikey"] == INCHIKEY


@pytest.mark.dependency(depends=["test_service_available"])
def test_unknown_compound_raises():
    with pytest.raises(UnknownResponse):
        asyncio.run(
            wrap_with_session(
                ChEBI, "from_name", ["not-a-compound-name-msmetaenhancer"]
            )
        )


@pytest.mark.dependency(depends=["test_service_available"])
def test_format_search_response():
    args = f"es_search/?term={INCHIKEY}&page=1&size=15"
    response = asyncio.run(
        wrap_with_session(ChEBI, "query_the_service", ["ChEBI", args])
    )

    assert isinstance(response, str)
    data = json.loads(response)
    assert {"results", "total", "number_pages"} <= data.keys()
    assert "_source" in data["results"][0]


@pytest.mark.dependency(depends=["test_service_available"])
def test_format_structure_search_response():
    from frozendict import frozendict

    data = frozendict({"structure": SMILES, "type": "similarity", "similarity": 1})
    response = asyncio.run(
        wrap_with_session(
            ChEBI, "query_the_service", ["ChEBI", "structure_search/", "POST", data]
        )
    )

    assert isinstance(response, str)
    data = json.loads(response)
    assert {"results", "total", "number_pages"} <= data.keys()
    assert data["results"][0]["_source"]["chebi_accession"] == CHEBI_ID


@pytest.mark.dependency(depends=["test_service_available"])
def test_format_entity_response():
    args = f"compound/{CHEBI_ID}/"
    response = asyncio.run(
        wrap_with_session(ChEBI, "query_the_service", ["ChEBI", args])
    )

    assert isinstance(response, str)
    data = json.loads(response)
    assert data["chebi_accession"] == CHEBI_ID
    assert data["names"]["IUPAC NAME"][0]["name"] == IUPAC_NAME


def test_parse_entity():
    parsed = ChEBI(None).parse_entity(ENTITY_RESPONSE)

    assert parsed == {
        "chebiid": CHEBI_ID,
        "compound_name": CHEBI_NAME,
        "iupac_name": IUPAC_NAME,
        "formula": FORMULA,
        "smiles": SMILES,
        "inchi": INCHI,
        "inchikey": INCHIKEY,
    }


def test_parse_entity_without_structures():
    response = json.dumps(
        {
            "id": 26649,
            "chebi_accession": "CHEBI:26649",
            "name": "serine derivative",
            "ascii_name": "serine derivative",
            "stars": 3,
            "names": {
                "SYNONYM": [
                    {
                        "name": "serine derivatives",
                        "status": "C",
                        "type": "SYNONYM",
                        "source": "ChEBI",
                        "ascii_name": "serine derivatives",
                        "adapted": False,
                        "language_code": "en",
                    }
                ]
            },
            "chemical_data": None,
            "default_structure": None,
            "secondary_ids": [],
        }
    )

    parsed = ChEBI(None).parse_entity(response)

    assert parsed == {
        "chebiid": "CHEBI:26649",
        "compound_name": "serine derivative",
    }


def test_extract_chebiid_prefers_matching_name():
    # ChEBI ranks '5,5'-dibromo-BAPTA highest for the term 'bapta'
    assert ChEBI(None).extract_chebiid(SEARCH_BAPTA_RESPONSE, COMPOUND_NAME) == CHEBI_ID


def test_extract_chebiid_matching_identifier():
    assert ChEBI(None).extract_chebiid(SEARCH_INCHIKEY_RESPONSE, INCHIKEY) == CHEBI_ID


def test_extract_chebiid_matching_identifier_from_multiple_results():
    assert ChEBI(None).extract_chebiid(SEARCH_BAPTA_RESPONSE, INCHIKEY) == CHEBI_ID


def test_extract_chebiid_rejects_unmatched_multiple_results():
    # related compounds are reported for terms ChEBI does not know as names
    assert ChEBI(None).extract_chebiid(SEARCH_BAPTA_RESPONSE, "bapta acid") is None


def test_extract_chebiid_rejects_other_identifier():
    assert (
        ChEBI(None).extract_chebiid(
            SEARCH_INCHIKEY_RESPONSE, "UNSRVVFXOFNFJF-UHFFFAOYSA-N"
        )
        is None
    )


def test_extract_chebiid_accepts_single_unmatched_result():
    # IUPAC names are not reported by the search endpoint, a single result identifies them
    assert ChEBI(None).extract_chebiid(SEARCH_IUPAC_RESPONSE) == CHEBI_ID


def test_extract_chebiid_without_term_requires_single_result():
    assert ChEBI(None).extract_chebiid(SEARCH_BAPTA_RESPONSE) is None


def test_extract_chebiid_from_structure_search_response():
    assert ChEBI(None).extract_chebiid(STRUCTURE_SEARCH_RESPONSE) == CHEBI_ID


def test_extract_chebiid_without_results():
    assert ChEBI(None).extract_chebiid(json.dumps({"results": [], "total": 0})) is None


def test_get_first_value_skips_unusable_paths():
    converter = ChEBI(None)
    entity = {"default_structure": 2706518, "name": CHEBI_NAME}
    paths = [("default_structure", "smiles"), ("name",)]

    assert converter._get_first_value(entity, paths) == CHEBI_NAME


def test_get_first_value_missing_paths():
    converter = ChEBI(None)

    assert (
        converter._get_first_value({"name": None}, [("name",), ("ascii_name",)]) is None
    )
    assert converter._get_first_value({}, [("default_structure", "smiles")]) is None


def test_reference_data_describes_single_compound():
    # the constants above are recorded from ChEBI and must describe one structure
    mol = MolFromSmiles(SMILES)
    assert MolToSmiles(mol) == MolToSmiles(MolFromInchi(INCHI))
    assert MolToInchi(MolFromSmiles(SMILES)) == INCHI
    assert InchiToInchiKey(INCHI) == INCHIKEY


def test_get_conversions():
    jobs = ChEBI(None).get_conversion_functions()
    assert ("chebiid", "inchikey", "ChEBI") in jobs
    assert ("inchikey", "chebiid", "ChEBI") in jobs
    assert ("compound_name", "chebiid", "ChEBI") in jobs
    assert ("compound_name", "iupac_name", "ChEBI") in jobs
    assert ("chebiid", "iupac_name", "ChEBI") in jobs
    assert ("inchikey", "iupac_name", "ChEBI") in jobs
    assert ("iupac_name", "chebiid", "ChEBI") in jobs
    assert ("inchi", "chebiid", "ChEBI") in jobs
    assert ("smiles", "chebiid", "ChEBI") in jobs
