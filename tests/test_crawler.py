import csv
import os
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import crawler
from tests import TEST_FILE_PATH


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




