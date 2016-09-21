import csv
import os
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import crawler
from tests import TEST_FILE_PATH


class MockPageGenerator:
    """Generates the mock Web Pages for the tests based on the url path key

    Args:
        par_by_path (dict): {path: [parameters]}

    Returns:
        str: Mock page rendered with the parameter selected based on the path
    """
    def __init__(self, par_by_path):
        self.par_by_path = par_by_path
        self.mock_page = open(os.path.join(TEST_FILE_PATH, 'mock_page.html')).read()

    def __call__(self, url):
        class MockResponse:
            url = None
        path = urlparse(url).path
        MockResponse.url = url if self.par_by_path.get(path) \
            else 'http://www.epocacosmeticos.com.br/?ProductLinkNotFound=' + path
        return (self.mock_page.format(*self.par_by_path.get(path, ['Empty' for n in range(5)])), MockResponse)


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
        self.assertTrue(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p',
                                                'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'))

    def test_is_not_product_page(self):
        self.assertFalse(crawler.is_product_page('http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino',
                                                 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino'))

    def test_response_error_url(self):
        self.assertFalse(crawler.is_product_page('http://www.epocacosmeticos.com.br/fake-product/p',
                                                 'http://www.epocacosmeticos.com.br/?ProductLinkNotFound=fake-product/p'))

    def test_mock_url(self):
        self.assertTrue(crawler.is_product_page('http://www.epocacosmeticos.com.br/fake-product/p',
                                                'http://www.epocacosmeticos.com.br/fake-product/p'))

    def test_invalid_value(self):
        self.assertRaises(ValueError, crawler.is_product_page, 123, 256)


class TestArgParsing(unittest.TestCase):
    """Tests for checking the correct parsing of the CLI arguments"""
    def test_depth_0_output_testecsv_valid_url(self):
        config = crawler.parse_args(['--output', 'teste.csv', '/'])
        self.assertEqual('teste.csv', config.output)
        self.assertEqual('http://www.epocacosmeticos.com.br/', config.path)

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
        url = '/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                     'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                     'http://www.epocacosmeticos.com.br' + url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose(self):
        url = '/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                     'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                     'http://www.epocacosmeticos.com.br' + url]]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_eternity_product_link_not_found(self):
        url = '/eternity-25th-anniversary-edition-for-women-eau-de-toilette-calvin-klein-perfume-feminino/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_invalid_product(self):
        url = '/invalid-product/p'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_0(self):
        crawler.main(['-d', '0', '-o', 'teste.csv', '/'])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_home_page_depth_1(self):
        crawler.main(['-d', '1', '-o', 'teste.csv', '/'])
        self.assertEqual(80, len(self.load_result_csv()))

    def test_crawl_malformed_url(self):
        url = '/cabelos/coloracao/tintura-para-cabelos/Sem Amônia'
        crawler.main(['-d', '0', '-o', 'teste.csv', url])
        self.assertEqual(0, len(self.load_result_csv()))

    def test_crawl_doubled_id_page(self):
        url = '/mascara-reestruturadora-monoi-e-argan-nick-vick-mascara-para-cabelos-quimicamente-tratados/p'
        crawler.main(['-d', '2', '-o', 'teste.csv', url])
        self.assertEqual(0, len(self.load_result_csv()))

    def test_crawl_mock_pages_all_products_no_repetitions(self):
        mock_params = {'/produto_inicial/p': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'produto_2/p', 'produto_3/p'),
                       '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'produto_4/p', 'produto_5/p', 'produto_6/p'),
                       '/produto_2/p': ('Pagina Produto 2', 'Produto 2', 'produto_7/p', 'produto_8/p', 'produto_9/p'),
                       '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'produto_10/p', 'produto_11/p', 'produto_12/p')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '1', '-o', 'teste.csv', '/produto_inicial/p'])
        expected = [['Produto Inicial', 'Pagina Inicial', 'http://www.epocacosmeticos.com.br/produto_inicial/p'],
                    ['Produto 1', 'Pagina Produto 1', 'http://www.epocacosmeticos.com.br/produto_1/p'],
                    ['Produto 2', 'Pagina Produto 2', 'http://www.epocacosmeticos.com.br/produto_2/p'],
                    ['Produto 3', 'Pagina Produto 3', 'http://www.epocacosmeticos.com.br/produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_mock_pages_no_product(self):
        mock_params = {'/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'pagina_1', 'pagina_2', 'pagina_3'),
                       '/pagina_1': ('Pagina Produto 1', 'Produto 1', 'pagina_4', 'pagina_5', 'pagina_6'),
                       '/pagina_2': ('Pagina Produto 2', 'Produto 2', 'pagina_7', 'pagina_8', 'pagina_9'),
                       '/pagina_3': ('Pagina Produto 3', 'Produto 3', 'pagina_10', 'pagina_11', 'pagina_12')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '1', '-o', 'teste.csv', '/pagina_inicial'])
        expected = []
        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_mock_pages_mixed_no_repetitions(self):
        mock_params = {'/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'pagina_2', 'produto_3/p'),
                       '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'pagina_4', 'pagina_5', 'pagina_6'),
                       '/pagina_2': ('Pagina 2', 'Página 2', 'pagina_7', 'pagina_8', 'pagina_9'),
                       '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'pagina_10', 'pagina_11', 'pagina_12')}
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '1', '-o', 'teste.csv', '/pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', 'http://www.epocacosmeticos.com.br/produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', 'http://www.epocacosmeticos.com.br/produto_3/p']]
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
            crawler.main(['-d', '2', '-o', 'teste.csv', '/pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', 'http://www.epocacosmeticos.com.br/produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', 'http://www.epocacosmeticos.com.br/produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())


