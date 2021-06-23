import unittest
import mock

from libs.Annotator import Annotator


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator()

    def test_annotate(self):
        jobs = [('name', 'inchi', 'PubChem')]

        pubchem = self.annotator.services['PubChem']
        pubchem.name_to_inchi = mock.Mock(return_value='a InChi value')
        self.annotator.services['PubChem'] = pubchem

        metadata = {'name': 'a good name'}
        expected_metadata = {'name': 'a good name', 'inchi': 'a InChi value'}
        self.assertEqual(self.annotator.annotate(metadata, jobs), expected_metadata)

    def test_service_unknown(self):
        jobs = [('name', 'inchi', 'Jumbo')]
        metadata = {'name': 'a good name'}
        self.assertEqual(self.annotator.annotate(metadata, jobs), metadata)

    def test_source_unknown(self):
        jobs = [('random_name', 'inchi', 'Jumbo')]
        metadata = {'name': 'a good name'}
        self.assertEqual(self.annotator.annotate(metadata, jobs), metadata)

    def test_target_unknown(self):
        jobs = [('name', 'random_name', 'CTS')]
        metadata = {'name': 'a good name'}
        self.assertEqual(self.annotator.annotate(metadata, jobs), metadata)

    def test_get_all_conversions(self):
        expected_result = [('cas', 'inchikey', 'CTS'), ('inchikey', 'inchi', 'CTS'), ('inchikey', 'iupac_name', 'CTS'),
                           ('inchikey', 'name', 'CTS'), ('name', 'inchikey', 'CTS'), ('cas', 'smiles', 'CIR'),
                           ('inchikey', 'cas', 'CIR'), ('inchikey', 'formula', 'CIR'), ('inchikey', 'inchi', 'CIR'),
                           ('inchikey', 'smiles', 'CIR'), ('smiles', 'inchikey', 'CIR'), ('inchikey', 'name', 'NLM'),
                           ('name', 'inchikey', 'NLM'), ('inchi', 'formula', 'PubChem'),
                           ('inchi', 'inchikey', 'PubChem'), ('inchi', 'iupac_name', 'PubChem'),
                           ('inchi', 'smiles', 'PubChem'), ('name', 'inchi', 'PubChem')]
        self.assertEqual(set(self.annotator.get_all_conversions()), set(expected_result))
