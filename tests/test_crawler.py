import os
import unittest

from tests import TEST_FILE_PATH
import crawler


class TestExtraction(unittest.TestCase):
    def test_extract_from_hypnose(self):
        expected = {'product_name': 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml',
                    'page_title': 'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos'}
        html = open(os.path.join(TEST_FILE_PATH, 'hypnose-eau-de-toilette-lancome-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_attributes(html))