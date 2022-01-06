import asyncio
import pytest
import mock

from MSMetaEnhancer.libs.Annotator import Annotator
from MSMetaEnhancer.libs.utils.Errors import TargetAttributeNotRetrieved
from MSMetaEnhancer.libs.utils.Job import Job


@pytest.mark.parametrize('data, expected, repeat, mocked', [
    [{'name': '$NAME'}, {'name': '$NAME', 'inchi': '$InChi'}, False, [({'name': '$NAME', 'inchi': '$InChi'}, None)]],
    [{'name': '$NAME'}, {'name': '$NAME', 'inchi': '$InChi', 'smiles': '$SMILES'}, True,
     [({'name': '$NAME', 'inchi': '$InChi'}, None), ({'name': '$NAME', 'inchi': '$InChi', 'smiles': '$SMILES'}, None)]]
])
def test_annotate(data, expected, repeat, mocked):
    jobs = [Job(('inchi', 'smiles', 'PubChem')),
            Job(('name', 'inchi', 'PubChem'))]

    annotator = Annotator(dict())
    annotator.execute_job_with_cache = mock.AsyncMock()
    annotator.execute_job_with_cache.side_effect = mocked

    spectra = mock.Mock()
    spectra.metadata = data

    asyncio.run(annotator.annotate(spectra, jobs, repeat))

    assert spectra.metadata == expected


def test_execute_job_with_cache():
    curator = mock.Mock()
    curator.filter_invalid_metadata = mock.MagicMock(side_effect=lambda a: a)

    pubchem = mock.Mock()
    pubchem.convert = mock.AsyncMock(return_value={'smiles': '$SMILES'})

    job = Job(('inchi', 'smiles', 'PubChem'))
    job.validate = mock.Mock(return_value=(pubchem, None))

    annotator = Annotator({'PubChem': pubchem})
    annotator.curator = curator
    metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'inchi': '$InChi'}, dict()))
    assert metadata == {'inchi': '$InChi', 'smiles': '$SMILES'}

    # already cached

    cts = mock.Mock()
    cts.convert = mock.AsyncMock(return_value=dict())

    job = Job(('smiles', 'formula', 'CTS'))
    job.validate = mock.Mock(return_value=(cts, None))

    cache = {job.service: {'formula': '$FORMULA'}}

    annotator = Annotator({'CTS': cts})
    annotator.curator = curator
    metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'smiles': '$SMILES'}, cache))
    assert metadata == {'smiles': '$SMILES', 'formula': '$FORMULA'}

    # no data retrieved

    cir = mock.Mock()
    cir.convert = mock.AsyncMock(return_value=dict())

    annotator = Annotator({'CIR': cir})
    annotator.curator = curator

    with pytest.raises(TargetAttributeNotRetrieved):
        metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'smiles': '$SMILES'}, dict()))
