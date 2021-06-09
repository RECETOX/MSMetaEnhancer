import unittest
import mock

from libs import Converter


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()

    def test_connect_to_service(self):
        # test basic CTS service
        cas_number = '7783-89-3'
        args = 'CAS/InChIKey/{}'.format(cas_number)
        response = self.converter.connect_to_service('CTS', args)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertTrue(type(json == list))
        self.assertEqual(len(json), 1)
        self.assertIn('results', json[0])
        self.assertEqual(len(json[0]['results']), 1)

        # incorrect CAS number
        cas_number = '7783893'
        args = 'CAS/InChIKey/{}'.format(cas_number)
        response = self.converter.connect_to_service('CTS', args)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertTrue(type(json == list))
        self.assertEqual(len(json), 1)
        self.assertIn('results', json[0])
        self.assertEqual(len(json[0]['results']), 0)

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

        # test incorrect service (simulates unavailable service)
        self.converter.services['random'] = 'https://random_strange_url.com'
        self.assertRaises(ConnectionError, self.converter.connect_to_service, 'random', '')

    def test_fix_cas_number(self):
        self.assertEqual(self.converter.fix_cas_number('7783893'), '7783-89-3')

    def test_cas_to_inchikey(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_inchikey(cas_number), inchikey)

        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_inchikey(cas_number))

    def test_cas_to_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_smiles(cas_number), smiles)

        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_smiles(cas_number))

    def test_inchikey_to_inchi(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        inchi = "1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1"
        self.assertEqual(self.converter.inchikey_to_inchi(inchikey), inchi)
