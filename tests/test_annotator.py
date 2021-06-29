import asyncio
import unittest
import mock

from libs.Annotator import Annotator
from tests.utils import wrap_with_session


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator()

    def test_annotate(self):
        jobs = [('name', 'inchi', 'PubChem')]
        pubchem = self.annotator.services['PubChem']
        pubchem.name_to_inchi = mock.AsyncMock(return_value='a InChi value')
        self.annotator.services['PubChem'] = pubchem

        spectra = mock.Mock()
        spectra.metadata = {'name': 'a good name'}
        expected_spectra = mock.AsyncMock()
        expected_spectra.metadata = {'name': 'a good name', 'inchi': 'a InChi value'}
        self.assertEqual(asyncio.run(wrap_with_session(self.annotator, 'annotate', [spectra, jobs])).metadata,
                         expected_spectra.metadata)

    def test_service_unknown(self):
        jobs = [('name', 'inchi', 'Jumbo')]
        spectra = mock.Mock()
        spectra.metadata = {'name': 'a good name'}
        self.assertEqual(asyncio.run(wrap_with_session(self.annotator, 'annotate', [spectra, jobs])), spectra)

    def test_source_unknown(self):
        jobs = [('random_name', 'inchi', 'Jumbo')]
        spectra = mock.Mock()
        spectra.metadata = {'name': 'a good name'}
        self.assertEqual(asyncio.run(wrap_with_session(self.annotator, 'annotate', [spectra, jobs])), spectra)

    def test_target_unknown(self):
        jobs = [('name', 'random_name', 'CTS')]
        spectra = mock.Mock()
        spectra.metadata = {'name': 'a good name'}
        self.assertEqual(asyncio.run(wrap_with_session(self.annotator, 'annotate', [spectra, jobs])), spectra)

    def test_get_all_conversions(self):
        expected_result = [('cas', 'inchikey', 'CTS'), ('inchikey', 'inchi', 'CTS'), ('inchikey', 'iupac_name', 'CTS'),
                           ('inchikey', 'name', 'CTS'), ('name', 'inchikey', 'CTS'), ('cas', 'smiles', 'CIR'),
                           ('inchikey', 'cas', 'CIR'), ('inchikey', 'formula', 'CIR'), ('inchikey', 'inchi', 'CIR'),
                           ('inchikey', 'smiles', 'CIR'), ('smiles', 'inchikey', 'CIR'), ('inchikey', 'name', 'NLM'),
                           ('name', 'inchikey', 'NLM'), ('inchi', 'formula', 'PubChem'),
                           ('inchi', 'inchikey', 'PubChem'), ('inchi', 'iupac_name', 'PubChem'),
                           ('inchi', 'smiles', 'PubChem'), ('name', 'inchi', 'PubChem')]
        self.assertEqual(set(self.annotator.get_all_conversions()), set(expected_result))
