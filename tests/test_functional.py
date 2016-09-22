"""
Functional tests for the PriceCrawler project.
"""

import unittest
import os
import subprocess
import csv
from unittest.mock import patch
from urllib.parse import urlparse

import crawler
from tests import PROJECT_ROOT, TEST_FILE_PATH

CRAWLER_EXECUTABLE = os.path.join(PROJECT_ROOT, 'crawler.py')


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


class TestCrawler(unittest.TestCase):
    """Tests the extraction of the page title, product name and URL from a single page."""
    def execute_command(self, page, depth=0):
        command = [CRAWLER_EXECUTABLE, '-d', str(depth),  '-o', 'teste.csv', page]
        subprocess.run(command, check=True)

    def load_result_csv(self):
        with open('teste.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            return [row for row in csvreader]

    def tearDown(self):
        if os.path.exists('teste.csv'):
            os.remove('teste.csv')

    def test_crawl_lady_million(self):
        target_page = '/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        self.execute_command(target_page)

        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                    'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                     'http://www.epocacosmeticos.com.br' + target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose(self):
        target_page = '/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        self.execute_command(target_page)

        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    'http://www.epocacosmeticos.com.br' + target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_invalid_url(self):
        target_page = 'Invalid_url!'
        self.assertRaises(subprocess.CalledProcessError, self.execute_command, target_page)

class TestMainFunction(unittest.TestCase):
    """Tests the main funtion in a white box manner"""
    def setUp(self):
        if os.path.exists('teste.csv'):
            os.remove('teste.csv')
        if os.path.exists('teste.json'):
            os.remove('teste.json')

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

    def test_crawl_mock_pages_with_persistence(self):
        mock_params = {
            '/pagina_inicial': ('Pagina Inicial', 'Produto Inicial', 'produto_1/p', 'pagina_2', 'produto_3/p'),
            '/produto_1/p': ('Pagina Produto 1', 'Produto 1', 'produto_3/p', 'pagina_5', 'pagina_6'),
            '/produto_2/p': ('Pagina Produto 2', 'Produto 2', 'produto_4/p', 'produto_5/p', 'pagina_1'),
            '/produto_3/p': ('Pagina Produto 3', 'Produto 3', 'produto_2/p', 'produto_4/p', 'produto_6/p'),
            '/produto_4/p': ('Pagina Produto 4', 'Produto 4', 'pagina_inicial', 'pagina_6', 'produto_5/p'),
            '/produto_5/p': ('Pagina Produto 5', 'Produto 5', 'produto_7/p', 'produto_8/p', 'pagina_5'),
            '/produto_6/p': ('Pagina Produto 6', 'Produto 6', 'pagina_inicial', 'pagina_1', 'produto_5/p'),
            '/produto_7/p': ('Pagina Produto 6', 'Produto 6', 'pagina_inicial', 'pagina_1', 'produto_5/p'),
            '/pagina_1': ('Pagina 1', 'Página 1', 'produto_1/p', 'pagina_5', 'produto_3/p'),
            '/pagina_2': ('Pagina 2', 'Página 2', 'produto_2/p', 'pagina_1', 'pagina_3'),
            '/pagina_3': ('Pagina 3', 'Página 3', 'produto_6/p', 'pagina_1', 'pagina_inicial'),
            '/pagina_4': ('Pagina 4', 'Página 4', 'produto_8/p', 'pagina_5', 'produto_3/p'),
            '/pagina_5': ('Pagina 5', 'Página 5', 'produto_2/p', 'pagina_4', 'produto_4/p'),
            '/pagina_6': ('Pagina 6', 'Página 6', 'pagina_inicial', 'pagina_5', 'produto_3/p'),
        }
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '0', '-o', 'teste.csv', '-r', 'teste.json', '/pagina_inicial'])
        expected = []
        self.assertEqual(expected, self.load_result_csv())
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '0', '-o', 'teste.csv', '-r', 'teste.json', '/pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', 'http://www.epocacosmeticos.com.br/produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', 'http://www.epocacosmeticos.com.br/produto_3/p']]
        self.assertEqual(expected, self.load_result_csv())
        with patch('crawler.get_page_contents', MockPageGenerator(mock_params)):
            crawler.main(['-d', '0', '-o', 'teste.csv', '-r', 'teste.json', '/pagina_inicial'])
        expected = [['Produto 1', 'Pagina Produto 1', 'http://www.epocacosmeticos.com.br/produto_1/p'],
                    ['Produto 3', 'Pagina Produto 3', 'http://www.epocacosmeticos.com.br/produto_3/p'],
                    ['Produto 2', 'Pagina Produto 2', 'http://www.epocacosmeticos.com.br/produto_2/p'],
                    ['Produto 4', 'Pagina Produto 4', 'http://www.epocacosmeticos.com.br/produto_4/p'],
                    ['Produto 6', 'Pagina Produto 6', 'http://www.epocacosmeticos.com.br/produto_6/p']]
        self.assertEqual(expected, self.load_result_csv())
