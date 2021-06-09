import unittest
import mock

from libs.Annotator import Annotator


class TestAnnotator(unittest.TestCase):
    def test_add_possible_annotations(self):
        self.annotator = Annotator(['inchikey', 'smiles', 'casno', 'unknown-one'])

        self.annotator.add_inchikey = mock.Mock()
        self.annotator.add_inchikey.side_effect = [None, 'a InChiKey value']
        self.annotator.add_smiles = mock.Mock()
        self.annotator.add_smiles.side_effect = [None, 'a SMILES value']
        self.annotator.add_casno = mock.Mock(return_value='a CAS number')
        
        metadata = dict()
        self.assertEqual(self.annotator.add_possible_annotations(metadata),
                         {'casno': 'a CAS number', 'inchikey': 'a InChiKey value', 'smiles': 'a SMILES value'})

    def test_add_inchikey(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        self.annotator = Annotator(['inchikey', 'smiles', 'unknown-one'])
        self.annotator.converter.fix_cas_number = mock.Mock(return_value='7783-89-3')
        self.annotator.converter.cas_to_inchikey = mock.Mock(return_value=inchikey)

        metadata = {'casno': '7783893'}
        self.assertEqual(self.annotator.add_inchikey(metadata), inchikey)

        metadata = dict()
        self.assertIsNone(self.annotator.add_inchikey(metadata))

    def test_add_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        self.annotator = Annotator(['inchikey', 'smiles', 'unknown-one'])
        self.annotator.converter.fix_cas_number = mock.Mock(return_value='7783-89-3')
        self.annotator.converter.add_smiles = mock.Mock(return_value=smiles)

        metadata = {'casno': '7783893'}
        self.assertEqual(self.annotator.add_smiles(metadata), smiles)

        metadata = dict()
        self.assertIsNone(self.annotator.add_smiles(metadata))
