import pytest

from MSMetaEnhancer.libs.converters.compute import RDKit


INCHI = "InChI=1S/C19H28O2/c1-18-9-7-13(20)11-12(18)3-4-14-15-5-6-17(21)19(15,2)10-8-16(14)18/h11,14-17,21H,3-10H2,1-2H3/t14-,15-,16-,17-,18-,19-/m0/s1"
CANONICAL_SMILES = "CC12CCC(=O)C=C1CCC1C2CCC2(C)C(O)CCC12"
ISOMERIC_SMILES = "C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@@]43C)[C@@H]1CC[C@@H]2O"
CANONICAL_INCHI = "InChI=1S/C19H28O2/c1-18-9-7-13(20)11-12(18)3-4-14-15-5-6-17(21)19(15,2)10-8-16(14)18/h11,14-17,21H,3-10H2,1-2H3"
INCHIKEY = "MUMGGOZAMZWBJJ-DYKIIFRCSA-N"
CANONICAL_INCHIKEY = "MUMGGOZAMZWBJJ-UHFFFAOYSA-N"


@pytest.mark.parametrize(
    "method, input, expected",
    [
        ["inchi_to_canonical_smiles", INCHI, {"canonical_smiles": CANONICAL_SMILES}],
        [
            "inchi_to_isomeric_smiles",
            INCHI,
            {"isomeric_smiles": ISOMERIC_SMILES},
        ],
        ["from_smiles", CANONICAL_SMILES, {"mw": 288.208930136}],
        ["formula_to_mw", "C9H15N4O8P", {"mw": 338.21299999999997}],
        ["smiles_to_formula", CANONICAL_SMILES, {"formula": "C19H28O2"}],
        ["canonical_smiles_to_formula", CANONICAL_SMILES, {"formula": "C19H28O2"}],
        ["isomeric_smiles_to_formula", ISOMERIC_SMILES, {"formula": "C19H28O2"}],
        ["inchi_to_formula", INCHI, {"formula": "C19H28O2"}],
        ["smiles_to_inchi", CANONICAL_SMILES, {"inchi": CANONICAL_INCHI}],
        ["canonical_smiles_to_inchi", CANONICAL_SMILES, {"inchi": CANONICAL_INCHI}],
        ["isomeric_smiles_to_inchi", ISOMERIC_SMILES, {"inchi": INCHI}],
        ["smiles_to_inchikey", CANONICAL_SMILES, {"inchikey": CANONICAL_INCHIKEY}],
        ["canonical_smiles_to_inchikey", CANONICAL_SMILES, {"inchikey": CANONICAL_INCHIKEY}],
        ["isomeric_smiles_to_inchikey", ISOMERIC_SMILES, {"inchikey": INCHIKEY}],
        ["inchi_to_inchikey", INCHI, {"inchikey": INCHIKEY}],
    ],
)
def test_convert_methods(method, input, expected):
    func = getattr(RDKit(), method)
    actual = func(input)
    assert actual == expected
