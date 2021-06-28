import asyncio
import unittest
import json

from libs.services.PubChem import PubChem
from tests.utils import run_in_session


class TestPubChem(unittest.TestCase):
    def setUp(self):
        self.converter = PubChem()

    def test_connect_to_service(self):
        inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        args = "inchi/JSON"
        response = asyncio.run(run_in_session(self.converter, 'query_the_service',
                                              ['PubChem', args, 'POST', {'inchi': inchi}]))
        response_json = json.loads(response)
        self.assertIn('PC_Compounds', response_json)
        self.assertTrue(len(response_json['PC_Compounds']) == 1)
        self.assertIn('props', response_json['PC_Compounds'][0])
        self.assertTrue(type(response_json['PC_Compounds'][0]['props']) == list)

    def test_inchi_to_inchikey(self):
        inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        inchikey = 'JVGVDSSUAVXRDY-UHFFFAOYSA-N'

        self.assertEqual(asyncio.run(run_in_session(self.converter, 'inchi_to_inchikey', [inchi])), inchikey)

        inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(asyncio.run(run_in_session(self.converter, 'inchi_to_inchikey', [inchi])))

    def test_name_to_inchi(self):
        name = '3-Methyl-5-[p-fluorophenyl]-2H-1,3-[3H]-oxazine-2,6-dione'
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'

        self.assertEqual(asyncio.run(run_in_session(self.converter, 'name_to_inchi', [name])), inchi)

        name = 'HYDROXYPHENYLLACTATE M-H'
        self.assertIsNone(asyncio.run(run_in_session(self.converter, 'name_to_inchi', [name])))

    def test_inchi_to_IUPAC_name(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        IUPAC_name = '5-(4-fluorophenyl)-3-methyl-1,3-oxazine-2,6-dione'

        self.assertEqual(asyncio.run(run_in_session(self.converter, 'inchi_to_iupac_name', [inchi])), IUPAC_name)

        inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(asyncio.run(run_in_session(self.converter, 'inchi_to_iupac_name', [inchi])))

    def test_inchi_to_formula(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        formula = 'C11H8FNO3'

        self.assertEqual(asyncio.run(run_in_session(self.converter, 'inchi_to_formula', [inchi])), formula)

        inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(asyncio.run(run_in_session(self.converter, 'inchi_to_formula', [inchi])))

    def test_inchi_to_smiles(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        smiles = 'CN1C=C(C(=O)OC1=O)C2=CC=C(C=C2)F'

        self.assertEqual(asyncio.run(run_in_session(self.converter, 'inchi_to_smiles', [inchi])), smiles)

        inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(asyncio.run(run_in_session(self.converter, 'inchi_to_smiles', [inchi])))
