import pytest

from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.utils.Job import Job
from MSMetaEnhancer.libs.utils.LogRecord import LogRecord


def test_fix_cas_number():
    curator = Curator()
    assert curator.fix_cas_number('7783893') == '7783-89-3'
    assert curator.fix_cas_number('7783-89-3') == '7783-89-3'


@pytest.mark.parametrize('metadata, validated_metadata, logs_size', [
    [{'inchikey': '<html>random content</html>'}, {}, 1],
    [{'smiles': 'CC(NC(C)=O)C#N'}, {'smiles': 'CC(NC(C)=O)C#N'}, 0]
])
def test_filter_invalid_metadata(metadata, validated_metadata, logs_size):
    warning = LogRecord(dict())
    job = Job(('smiles', 'inchi', 'converter'))
    curator = Curator()
    assert curator.filter_invalid_metadata(metadata, warning, job) == validated_metadata
    assert len(warning.logs) == logs_size
