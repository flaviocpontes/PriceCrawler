import csv
import os
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import crawler
from tests import TEST_FILE_PATH


class MockPageGenerator:
    """Generates the mock Web Pages for the tests based on the url path key"""
    def __init__(self, par_by_path):
        if not par_by_path and not type(par_by_path) == dict:
            raise AttributeError('Must be initialized with a parameter dict')
        self.par_by_path = par_by_path
        self.mock_page = open(os.path.join(TEST_FILE_PATH, 'mock_page.html')).read()

    def __call__(self, url):
        path = urlparse(url).path
        return self.mock_page.format(*self.par_by_path.get(path, ['Empty' for n in range(5)]))


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

    def test_extraction_from_synthetic_page(self):
        """Tests a synthetic page for value extraction"""
        expected = {'product_name': 'Fake Product 1',
                    'page_title': 'My first Fake Product'}
        fake_html = open(os.path.join(TEST_FILE_PATH, 'mock_page.html')).read()
        self.assertEqual(expected, crawler.extract_values(fake_html.format('My first Fake Product',
                                                                           'Fake Product 1',
                                                                           'page1/p',
                                                                           'page2/p',
                                                                           'page3/p')))


class TestIsProductPage(unittest.TestCase):
    """Tests for checking if a page is a prodcutd page"""
    def test_is_product_page(self):
        self.assertTrue(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'))

    def test_is_not_product_page(self):
        self.assertFalse(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino'))

    def test_fake_url(self):
        self.assertTrue(crawler.is_product_page('http://www.epocacosmeticos.com.br/fake-product/p'))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://www.epocacosmeticos.com.br/'

    def setUp(self):
        if os.path.exists('teste.csv'):
            os.remove('teste.csv')

    def load_result_csv(self):
        with open('teste.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            return [row for row in csvreader]

    def test_crawl_lady_million(self):
        url = self.base_url + 'lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        crawler.main(['-d', '1', '-o', 'teste.csv', url])
        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                     'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                     url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose(self):
        url = self.base_url + 'hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        crawler.main(['-d', '1', '-o', 'teste.csv', url])
        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_1(self):
        crawler.main(['-d', '1', '-o', 'teste.csv', self.base_url])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_2(self):
        crawler.main(['-d', '2', '-o', 'teste.csv', self.base_url])
        self.assertEqual(83, len(self.load_result_csv()))

    def test_crawl_home_page_depth_3(self):
        crawler.main(['-d', '3', '-o', 'teste.csv', self.base_url])
        self.assertEqual(83, len(self.load_result_csv()))

    def test_crawl_malformed_url(self):
        url = 'http://www.epocacosmeticos.com.br/cabelos/coloracao/tintura-para-cabelos/Sem Amônia'
        crawler.main(['-d', '1', '-o', 'teste.csv', url])
        self.assertEqual(0, len(self.load_result_csv()))

    def test_crawl_mock_pages_all_products_no_repetitions(self):
        mock_params = {'/produto_inicial/p': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'produto_2/p', 'produto_3/p'),
                       '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'produto_4/p', 'produto_5/p', 'produto_6/p'),
                       '/produto_2/p': ('Pagina Produto 2', 'Produto 2', 'produto_7/p', 'produto_8/p', 'produto_9/p'),
                       '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'produto_10/p', 'produto_11/p', 'produto_12/p')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '2', '-o', 'teste.csv', self.base_url + 'produto_inicial/p'])
        expected = [['Produto Inicial', 'Pagina Inicial', self.base_url + 'produto_inicial/p'],
                    ['Produto 1', 'Pagina Produto 1', self.base_url + 'produto_1/p'],
                    ['Produto 2', 'Pagina Produto 2', self.base_url + 'produto_2/p'],
                    ['Produto 3', 'Pagina Produto 3', self.base_url + 'produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_mock_pages_no_product(self):
        mock_params = {'/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'pagina_1', 'pagina_2', 'pagina_3'),
                       '/pagina_1': ('Pagina Produto 1', 'Produto 1', 'pagina_4', 'pagina_5', 'pagina_6'),
                       '/pagina_2': ('Pagina Produto 2', 'Produto 2', 'pagina_7', 'pagina_8', 'pagina_9'),
                       '/pagina_3': ('Pagina Produto 3', 'Produto 3', 'pagina_10', 'pagina_11', 'pagina_12')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '2', '-o', 'teste.csv', self.base_url + 'pagina_inicial'])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_mock_pages_mixed_no_repetitions(self):
        mock_params = {'/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'pagina_2', 'produto_3/p'),
                       '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'pagina_4', 'pagina_5', 'pagina_6'),
                       '/pagina_2': ('Pagina 2', 'Página 2', 'pagina_7', 'pagina_8', 'pagina_9'),
                       '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'pagina_10', 'pagina_11', 'pagina_12')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '2', '-o', 'teste.csv', self.base_url + 'pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', self.base_url + 'produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', self.base_url + 'produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_mock_pages_mixed_with_repetitions(self):
        mock_params = {
            '/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'pagina_2', 'produto_3/p'),
            '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'produto_3/p', 'pagina_5', 'pagina_6'),
            '/pagina_2': ('Pagina 2', 'Página 2', 'produto_1/p', 'pagina_5', 'produto_3/p'),
            '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'produto_1/p', 'pagina_5', 'pagina_6'),
            '/pagina_5': ('Pagina 5', 'Página 2', 'produto_1/p', 'pagina_5', 'produto_3/p'),
            '/pagina_6': ('Pagina 6', 'Página 2', 'produto_1/p', 'pagina_5', 'produto_3/p'),
        }
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '3', '-o', 'teste.csv', self.base_url + 'pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', self.base_url + 'produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', self.base_url + 'produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())


