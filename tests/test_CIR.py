import asyncio
import unittest

from libs.services.CIR import CIR
from tests.utils import wrap_with_session


class TestCIR(unittest.TestCase):
    def setUp(self):
        self.converter = CIR

    def test_connect_to_service(self):
        # test basic CIR service
        cas_number = '7783-89-3'
        args = '{}/smiles?resolver=cas_number'.format(cas_number)
        response = asyncio.run(wrap_with_session(self.converter, 'query_the_service', ['CIR', args]))
        self.assertTrue(type(response) == str)

        # incorrect CAS number
        cas_number = '7783893'
        args = '{}/smiles?resolver=cas_number'.format(cas_number)
        response = asyncio.run(wrap_with_session(self.converter, 'query_the_service', ['CIR', args]))
        self.assertIsNone(response)

    def test_cas_to_smiles(self):
        smiles = '[Ag+].[O-][Br](=O)=O'
        cas_number = '7783-89-3'
        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'cas_to_smiles', [cas_number])), smiles)

        cas_number = '7783893'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'cas_to_smiles', [cas_number])))

    def test_inchikey_to_smiles(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        smiles = '[Ag+].[O-][Br](=O)=O'
        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_smiles', [inchikey])), smiles)

        inchikey = 'XQLMNVCXIKR-UHFFFAOYSA-M'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_smiles', [inchikey])))

    def test_inchikey_to_inchi(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        inchi = 'InChI=1S/Ag.BrHO3/c;2-1(3)4/h;(H,2,3,4)/q+1;/p-1'

        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_inchi', [inchikey])), inchi)

        inchikey = 'XQLMNVCXIKR-UHFFFAOYSA-M'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_inchi', [inchikey])))

    def test_inchikey_to_cas(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        cas_number = '7783-89-3'

        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_cas', [inchikey])), cas_number)

        inchikey = 'XQLMNVCXIKR-UHFFFAOYSA-M'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_cas', [inchikey])))

    def test_inchikey_to_formula(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        formula = 'AgBrO3'

        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_formula', [inchikey])), formula)

        inchikey = 'XQLMNVCXIKR-UHFFFAOYSA-M'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'inchikey_to_formula', [inchikey])))

    def test_smiles_to_inchikey(self):
        inchikey = 'XQLMNMQWVCXIKR-UHFFFAOYSA-M'
        smiles = '[Ag+].[O-][Br](=O)=O'

        self.assertEqual(asyncio.run(wrap_with_session(self.converter, 'smiles_to_inchikey', [smiles])), inchikey)

        smiles = '[Ag+].O-][Br](=O)=O'
        self.assertIsNone(asyncio.run(wrap_with_session(self.converter, 'smiles_to_inchikey', [smiles])))
