import os
import unittest
import csv

from tests import TEST_FILE_PATH
from crawler import crawler


class TestExtraction(unittest.TestCase):
    """Tests the extraction of the sought attributes from the test html files"""
    def test_extract_from_ladymillion(self):
        expected = {'product_name': 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                    'page_title': 'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos'}
        html = open(os.path.join(TEST_FILE_PATH, 'lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_values(html))

    def test_extract_from_hypnose(self):
        expected = {'product_name': 'Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'page_title': 'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos'}
        html = open(os.path.join(TEST_FILE_PATH, 'hypnose-eau-de-toilette-lancome-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_values(html))


class TestIsProductPage(unittest.TestCase):
    """Tests for checking if a page is a prodcutd page"""
    def test_is_product_page(self):
        self.assertTrue(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'))

    def test_is_not_product_page(self):
        self.assertFalse(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino'))

    def test_invalid_value(self):
        self.assertRaises(ValueError, crawler.is_product_page, 123)


class TestArgParsing(unittest.TestCase):
    """Tests for checking the correct parsing of the CLI arguments"""
    def test_depth_0_output_testecsv_valid_url(self):
        config = crawler.parse_args(['--output', 'teste.csv', 'http://www.epocacosmeticos.com.br'])
        self.assertEqual('teste.csv', config.output)
        self.assertEqual('http://www.epocacosmeticos.com.br', config.url)

    def test_invalid_url(self):
        """URLS for domains other than http://www.epocacosmeticos.com.br/ should raise an exception"""
        self.assertRaises(ValueError, crawler.parse_args, ['invalid_url!'])


class TextExtractLinks(unittest.TestCase):
    """Tests the link extraction from the pages"""
    def test_links_from_home(self):
        home_page = open(os.path.join(TEST_FILE_PATH, 'home_page.html')).read()
        self.assertEqual(263, len(crawler.extract_links(home_page)))

    def test_links_hypnose(self):
        home_page = open(os.path.join(TEST_FILE_PATH, 'hypnose-eau-de-toilette-lancome-perfume-feminino.html')).read()
        self.assertEqual(116, len(crawler.extract_links(home_page)))


class TestMainFunction(unittest.TestCase):
    """Tests the main funtion in a white box manner"""
    def setUp(self):
        if os.path.exists('teste.csv'):
            os.remove('teste.csv')

    def load_result_csv(self):
        with open('teste.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            return [row for row in csvreader]

    def test_crawl_lady_million(self):
        url = 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                     'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                     url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose(self):
        url = 'http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_0(self):
        url = 'http://www.epocacosmeticos.com.br/'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_1(self):
        url = 'http://www.epocacosmeticos.com.br/'
        crawler.main(['-d', '2', '-o', 'teste.csv', url])
        expected = []
        self.assertLess(30, len(self.load_result_csv()))
