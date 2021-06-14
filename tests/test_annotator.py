import unittest
import mock

from libs.Annotator import Annotator


class TestAnnotator(unittest.TestCase):
    def test_add_possible_annotations(self):
        self.annotator = Annotator(['inchi', 'inchikey', 'smiles', 'unknown-one'])

        self.annotator.add_inchi = mock.Mock()
        self.annotator.add_inchi.side_effect = [None, 'a InChi value']
        self.annotator.add_inchikey = mock.Mock(return_value='a InChiKey value')
        self.annotator.add_smiles = mock.Mock(return_value='a SMILES value')

        metadata = {'casno': 'a CAS number'}
        self.assertEqual(self.annotator.add_possible_annotations(metadata),
                         {'casno': 'a CAS number', 'inchikey': 'a InChiKey value',
                          'smiles': 'a SMILES value', 'inchi': 'a InChi value'})

    def test_add_inchikey(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        self.annotator = Annotator(['inchikey', 'smiles', 'unknown-one'])
        self.annotator.CTS.cas_to_inchikey = mock.Mock(return_value=None)
        self.annotator.CTS.name_to_inchikey = mock.Mock(return_value=None)
        self.annotator.NLM.name_to_inchikey = mock.Mock(return_value=inchikey)

        metadata = {'casno': '7783-89-3', 'name': 'this is a good name'}
        self.assertEqual(self.annotator.add_inchikey(metadata), inchikey)

        metadata = dict()
        self.assertIsNone(self.annotator.add_inchikey(metadata))

    def test_add_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        self.annotator = Annotator(['inchikey', 'smiles', 'unknown-one'])
        self.annotator.CIR.cas_to_smiles = mock.Mock(return_value=None)
        self.annotator.CIR.inchikey_to_smiles = mock.Mock(return_value=smiles)

        metadata = {'casno': '7783-89-3', 'inchikey': 'an InChiKey'}
        self.assertEqual(self.annotator.add_smiles(metadata), smiles)

        metadata = dict()
        self.assertIsNone(self.annotator.add_smiles(metadata))

    def test_add_inchi(self):
        inchi = '1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1'
        self.annotator = Annotator(['inchi', 'smiles', 'unknown-one'])
        self.annotator.CTS.inchikey_to_inchi = mock.Mock(return_value=inchi)

        metadata = {'inchikey': 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'}
        self.assertEqual(self.annotator.add_inchi(metadata), inchi)

        metadata = dict()
        self.assertIsNone(self.annotator.add_inchi(metadata))

    def test_add_name(self):
        name = 'L-Alanine'
        self.annotator = Annotator(['name', 'smiles', 'unknown-one'])
        self.annotator.CTS.inchikey_to_name = mock.Mock(return_value=None)
        self.annotator.NLM.inchikey_to_name = mock.Mock(return_value=name)

        metadata = {'inchikey': 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'}
        self.assertEqual(self.annotator.add_name(metadata), name)

        metadata = dict()
        self.assertIsNone(self.annotator.add_name(metadata))

    def test_add_IUPAC(self):
        iupac = 'L-Alanine'
        self.annotator = Annotator(['IUPAC', 'smiles', 'unknown-one'])
        self.annotator.CTS.inchikey_to_IUPAC_name = mock.Mock(return_value=iupac)

        metadata = {'inchikey': 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'}
        self.assertEqual(self.annotator.add_IUPAC(metadata), iupac)

        metadata = dict()
        self.assertIsNone(self.annotator.add_IUPAC(metadata))
