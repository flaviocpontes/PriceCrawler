import unittest
import os
import subprocess
import csv

from tests import CRAWLER_PATH
CRAWLER_EXECUTABLE = os.path.join(CRAWLER_PATH, 'crawler.py')


class TestCrawlSinglePage(unittest.TestCase):
    def execute_command(self, page):
        command = [CRAWLER_EXECUTABLE, '-s', page, '-o', 'teste.csv']
        subprocess.run(command)

    def load_result_csv(self):
        with open('teste.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            return [row for row in csvreader]

    def test_crawl_lady_million(self):
        target_page = 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'
        self.execute_command(target_page)

        expected = [['Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml',
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
