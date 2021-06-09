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
        self.assertEqual(json[0]['results'][0], 'XQLMNMQWVCXIKR-UHFFFAOYSA-M')

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
        self.assertEqual(response.text, '[Ag+].[O-][Br](=O)=O')

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
        fake_result = mock.Mock()
        fake_result.status_code = 200

        fake_result.json = mock.Mock(return_value=[{'results': [inchikey]}])
        self.converter.connect_to_service = mock.Mock(return_value=fake_result)
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_inchikey(cas_number), inchikey)

        fake_result.json = mock.Mock(return_value=[{'results': []}])
        self.converter.connect_to_service = mock.Mock(return_value=fake_result)
        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_inchikey(cas_number))

    def test_cas_to_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        fake_result = mock.Mock()
        fake_result.text = smiles

        fake_result.status_code = 200
        self.converter.connect_to_service = mock.Mock(return_value=fake_result)
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_smiles(cas_number), smiles)

        fake_result.status_code = 500
        self.converter.connect_to_service = mock.Mock(return_value=fake_result)
        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_smiles(cas_number))
