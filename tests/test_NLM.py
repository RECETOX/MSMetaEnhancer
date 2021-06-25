import unittest
from io import StringIO
import pandas as pd

from libs.services.NLM import NLM


class TestNLM(unittest.TestCase):
    def setUp(self):
        self.converter = NLM()

    def test_connect_to_service(self):
        # test basic NLM service
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        args = 'inchikey/equals/{}?data=summary&format=tsv'.format(inchikey)
        response = self.converter.query_the_service('NLM', args)
        self.assertEqual(response.status_code, 200)

        table = pd.read_csv(StringIO(response.text), sep='\t')
        self.assertFalse(table.empty)

    def test_inchikey_to_name(self):
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        name = 'Alanine [USAN:INN]'
        self.assertEqual(self.converter.inchikey_to_name(inchikey), name)

        inchikey = 'QNAYBMLOXXXXGJ-REOHCLBHSA-N'
        self.assertIsNone(self.converter.inchikey_to_name(inchikey))

        inchikey = 'QNAYMLGJ-REOLBHSA-N'
        self.assertIsNone(self.converter.inchikey_to_name(inchikey))

    def test_name_to_inchikey(self):
        name = 'L-Alanine'
        inchikey = 'QNAYBMKLOCPYGJ-REOHCLBHSA-N'
        self.assertEqual(self.converter.name_to_inchikey(name), inchikey)

        name = 'L-Alanne'
        self.assertIsNone(self.converter.name_to_inchikey(name))
