import asyncio
import unittest
import mock

from libs.Annotator import Annotator
from libs.utils.Job import Job


class TestAnnotator(unittest.TestCase):
    def test_annotate(self):
        jobs = [Job(('name', 'inchi', 'PubChem'))]
        pubchem = mock.AsyncMock()
        pubchem.convert = mock.AsyncMock(return_value='a InChi value')

        services = {'PubChem': pubchem}
        annotator = Annotator(services)

        spectra = mock.Mock()
        spectra.metadata = {'name': 'a good name'}
        annotator.spectra = spectra

        expected_metadata = {'name': 'a good name', 'inchi': 'a InChi value'}
        asyncio.run(annotator.annotate(spectra, jobs))

        self.assertEqual(annotator.spectra.metadata, expected_metadata)
