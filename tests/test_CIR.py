import unittest

from libs.services.CIR import CIR


class TestCIR(unittest.TestCase):
    def setUp(self):
        self.converter = CIR()

    def test_connect_to_service(self):
        # test basic CIR service
        cas_number = '7783-89-3'
        args = '{}/smiles?resolver=cas_number'.format(cas_number)
        response = self.converter.connect_to_service('CIR', args)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.text) == str)

        # incorrect CAS number
        cas_number = '7783893'
        args = '{}/smiles?resolver=cas_number'.format(cas_number)
        response = self.converter.connect_to_service('CIR', args)
        self.assertEqual(response.status_code, 500)

    def test_cas_to_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_smiles(cas_number), smiles)

        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_smiles(cas_number))
