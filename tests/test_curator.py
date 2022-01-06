import pytest

from MSMetaEnhancer.libs.Curator import Curator


def test_fix_cas_number():
    curator = Curator()
    assert curator.fix_cas_number('7783893') == '7783-89-3'
    assert curator.fix_cas_number('7783-89-3') == '7783-89-3'


@pytest.mark.parametrize('metadata, validated_metadata', [
    [{'formula': 'CH4', 'smiles': 'C', 'iupac_name': 'methane', 'inchi': 'InChI=1S/CH4/h1H4'},
     {'formula': 'CH4', 'iupac_name': 'methane', 'inchi': 'InChI=1S/CH4/h1H4'}],
    [{'inchikey': '<html>random content</html>'}, {}],
    [{'smiles': 'CC(NC(C)=O)C#N'}, {'smiles': 'CC(NC(C)=O)C#N'}]
])
def test_filter_invalid_metadata(metadata, validated_metadata):
    curator = Curator()
    assert curator.filter_invalid_metadata(metadata) == validated_metadata
