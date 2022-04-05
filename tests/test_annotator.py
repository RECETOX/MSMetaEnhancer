import asyncio
import pytest
import mock

from MSMetaEnhancer.libs.Annotator import Annotator
from MSMetaEnhancer.libs.utils.Errors import TargetAttributeNotRetrieved
from MSMetaEnhancer.libs.utils.Job import Job


@pytest.mark.parametrize('data, expected, repeat, mocked', [
    [{'compound_name': '$NAME'}, {'compound_name': '$NAME', 'inchi': '$InChi'}, False,
     [({'compound_name': '$NAME', 'inchi': '$InChi'}, None)]],
    [{'compound_name': '$NAME'}, {'compound_name': '$NAME', 'inchi': '$InChi', 'smiles': '$SMILES'}, True,
     [({'compound_name': '$NAME', 'inchi': '$InChi'}, None),
      ({'compound_name': '$NAME', 'inchi': '$InChi', 'smiles': '$SMILES'}, None)]]
])
def test_annotate(data, expected, repeat, mocked):
    jobs = [Job(('inchi', 'smiles', 'IDSM')),
            Job(('name', 'inchi', 'IDSM'))]

    annotator = Annotator()
    annotator.set_converters(dict())
    annotator.execute_job_with_cache = mock.AsyncMock()
    annotator.execute_job_with_cache.side_effect = mocked

    spectra = mock.Mock()
    spectra.metadata = data

    asyncio.run(annotator.annotate(spectra, jobs, repeat))

    assert spectra.metadata == expected


def test_execute_job_with_cache():
    warning = mock.Mock()
    curator = mock.Mock()
    curator.filter_invalid_metadata = mock.MagicMock(side_effect=lambda a, b, c: a)

    idsm = mock.Mock()
    idsm.convert = mock.AsyncMock(return_value={'smiles': '$SMILES'})

    job = Job(('inchi', 'smiles', 'IDSM'))
    job.validate = mock.Mock(return_value=(idsm, None))

    annotator = Annotator()
    annotator.set_converters({'IDSM': idsm})
    annotator.curator = curator
    metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'inchi': '$InChi'}, dict(), warning))
    assert metadata == {'inchi': '$InChi', 'smiles': '$SMILES'}

    # already cached

    cts = mock.Mock()
    cts.convert = mock.AsyncMock(return_value=dict())

    job = Job(('smiles', 'formula', 'CTS'))
    job.validate = mock.Mock(return_value=(cts, None))

    cache = {job.converter: {'formula': '$FORMULA'}}

    annotator = Annotator()
    annotator.set_converters({'CTS': cts})
    annotator.curator = curator
    metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'smiles': '$SMILES'}, cache, warning))
    assert metadata == {'smiles': '$SMILES', 'formula': '$FORMULA'}

    # no data retrieved

    cir = mock.Mock()
    cir.convert = mock.AsyncMock(return_value=dict())

    annotator = Annotator()
    annotator.set_converters({'CIR': cir})
    annotator.curator = curator

    with pytest.raises(TargetAttributeNotRetrieved):
        metadata, cache = asyncio.run(annotator.execute_job_with_cache(job, {'smiles': '$SMILES'}, dict(), warning))
