import unittest

from libs.services.PubChem import PubChem


class TestCTS(unittest.TestCase):
    def setUp(self):
        self.converter = PubChem()

    def test_connect_to_service(self):
        inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        args = "inchi/JSON"
        response = self.converter.connect_to_service('PubChem', args, method='POST', data={'inchi': inchi})
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertIn('PC_Compounds', json)
        self.assertTrue(len(json['PC_Compounds']) == 1)
        self.assertIn('props', json['PC_Compounds'][0])
        self.assertTrue(type(json['PC_Compounds'][0]['props']) == list)

    def test_inchi_to_inchikey(self):
        inchi = 'InChI=1S/C9H10O4/c10-7-3-1-6(2-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        inchikey = 'JVGVDSSUAVXRDY-UHFFFAOYSA-N'
        self.assertEqual(self.converter.inchi_to_inchikey(inchi), inchikey)

        # clear the cache
        self.converter.cache = dict()

        wrong_inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)9(12)13/h1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(self.converter.inchi_to_inchikey(wrong_inchi))

    def test_name_to_inchi(self):
        name = '3-Methyl-5-[p-fluorophenyl]-2H-1,3-[3H]-oxazine-2,6-dione'
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        self.assertEqual(self.converter.name_to_inchi(name), inchi)

        name = 'HYDROXYPHENYLLACTATE M-H'
        self.assertIsNone(self.converter.name_to_inchi(name))

    def test_inchi_to_IUPAC_name(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        IUPAC_name = '5-(4-fluorophenyl)-3-methyl-1,3-oxazine-2,6-dione'
        self.assertEqual(self.converter.inchi_to_IUPAC_name(inchi), IUPAC_name)

        # clear the cache
        self.converter.cache = dict()

        wrong_inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(self.converter.inchi_to_IUPAC_name(wrong_inchi))

    def test_inchi_to_formula(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        formula = 'C11H8FNO3'
        self.assertEqual(self.converter.inchi_to_formula(inchi), formula)

        # clear the cache
        self.converter.cache = dict()

        wrong_inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(self.converter.inchi_to_formula(wrong_inchi))

    def test_inchi_to_smiles(self):
        inchi = 'InChI=1S/C11H8FNO3/c1-13-6-9(10(14)16-11(13)15)7-2-4-8(12)5-3-7/h2-6H,1H3'
        smiles = 'CN1C=C(C(=O)OC1=O)C2=CC=C(C=C2)F'
        self.assertEqual(self.converter.inchi_to_smiles(inchi), smiles)

        # clear the cache
        self.converter.cache = dict()

        wrong_inchi = 'InChI=1S/C9H10O4/c102-4-7)5-8(11)93/1-4,8,10-11H,5H2,(H,12,13)'
        self.assertIsNone(self.converter.inchi_to_smiles(wrong_inchi))
