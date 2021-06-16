import unittest

from libs.Curator import Curator


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.curator = Curator()

    def test_fix_cas_number(self):
        self.assertEqual(self.curator.fix_cas_number('7783893'), '7783-89-3')
        self.assertEqual(self.curator.fix_cas_number('7783-89-3'), '7783-89-3')
