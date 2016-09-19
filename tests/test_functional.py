"""
Functional tests for the PriceCrawler project.
"""

import unittest
import os
import subprocess
import csv

from tests import PROJECT_ROOT
CRAWLER_EXECUTABLE = os.path.join(PROJECT_ROOT, 'crawler.py')


class TestCrawler(unittest.TestCase):
    """Tests the extraction of the page title, product name and URL from a single page."""
    def execute_command(self, page, depth=1):
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
        target_page = 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        self.execute_command(target_page)

        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                    'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                    target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_lady_million_depth_2(self):
        target_page = 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        self.execute_command(target_page, 2)

        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                    'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                    target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose(self):
        target_page = 'http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        self.execute_command(target_page)

        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_crawl_hypnose_depth_2(self):
        target_page = 'http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p'
        self.execute_command(target_page, 2)

        expected = [['Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    target_page]]

        self.assertEqual(expected, self.load_result_csv())

    def test_invalid_url(self):
        target_page = 'Invalid_url!'
        self.assertRaises(subprocess.CalledProcessError, self.execute_command, target_page)
