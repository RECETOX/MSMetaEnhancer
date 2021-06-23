import unittest
import mock

from libs.Annotator import Annotator
from libs.utils.Job import Job


class TestAnnotator(unittest.TestCase):
    def test_annotate(self):
        self.annotator = Annotator([Job(('name', 'inchi', 'PubChem'))])

        pubchem = self.annotator.services['PubChem']
        pubchem.name_to_inchi = mock.Mock(return_value='a InChi value')
        self.annotator.services['PubChem'] = pubchem

        metadata = {'name': 'a good name'}
        expected_metadata = {'name': 'a good name', 'inchi': 'a InChi value'}
        self.assertEqual(self.annotator.annotate(metadata), expected_metadata)
