import unittest

from libs.services.CTS import CTS


class TestCTS(unittest.TestCase):
    def setUp(self):
        self.converter = CTS()

    def test_connect_to_service(self):
        # test basic CTS service
        cas_number = '7783-89-3'
        args = 'CAS/InChIKey/{}'.format(cas_number)
        response = self.converter.query_the_service('CTS', args)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertTrue(type(json == list))
        self.assertEqual(len(json), 1)
        self.assertIn('results', json[0])
        self.assertEqual(len(json[0]['results']), 1)

        # incorrect CAS number
        cas_number = '7783893'
        args = 'CAS/InChIKey/{}'.format(cas_number)
        response = self.converter.query_the_service('CTS', args)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertTrue(type(json == list))
        self.assertEqual(len(json), 1)
        self.assertIn('results', json[0])
        self.assertEqual(len(json[0]['results']), 0)

        # test incorrect service (simulates unavailable service)
        self.converter.services['random'] = 'https://random_strange_url.com'
        self.assertRaises(ConnectionError, self.converter.query_the_service, 'random', '')

    def test_cas_to_inchikey(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        cas_number = '7783-89-3'
        self.assertEqual(self.converter.cas_to_inchikey(cas_number), inchikey)

        cas_number = '7783893'
        self.assertIsNone(self.converter.cas_to_inchikey(cas_number))

    def test_inchikey_to_inchi(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        inchi = 'InChI=1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1'
        self.assertEqual(self.converter.inchikey_to_inchi(inchikey), inchi)

        inchikey = 'XQLMNMQIKR-UHFFFAOYSA-M'
        self.assertIsNone(self.converter.inchikey_to_inchi(inchikey))

    def test_name_to_inchikey(self):
        name = 'L-Alanine'
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        self.assertEqual(self.converter.name_to_inchikey(name), inchikey)

        name = 'L-Alalalalanine'
        self.assertIsNone(self.converter.name_to_inchikey(name))

    def test_inchikey_to_name(self):
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        name = 'L-2-Aminopropanoic acid'
        self.assertEqual(self.converter.inchikey_to_name(inchikey), name)

        inchikey = 'XQLMNMQIKR-UHFFFAOYSA-M'
        self.assertIsNone(self.converter.inchikey_to_name(inchikey))

    def test_inchikey_to_IUPAC_name(self):
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        uipac_name = '(2S)-2-aminopropanoic acid'
        self.assertEqual(self.converter.inchikey_to_iupac_name(inchikey), uipac_name)

        inchikey = 'XQLMNMQIKR-UHFFFAOYSA-M'
        self.assertIsNone(self.converter.inchikey_to_iupac_name(inchikey))

    def test_cache(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        identification = 'CTS_compound:' + inchikey
        _ = self.converter.inchikey_to_inchi(inchikey)

        self.assertIn(identification, self.converter.cache)

        _ = self.converter.inchikey_to_name(inchikey)
        _ = self.converter.inchikey_to_iupac_name(inchikey)

        self.assertIn(identification, self.converter.cache)
