import unittest
import json
import os
import subprocess

from tests import CRAWLER_PATH
CRAWLER_EXECUTABLE = os.path.join(CRAWLER_PATH, 'crawler.py')


class TestCrawlSinglePage(unittest.TestCase):
    def test_crawl_lady_million(self):
        expected = {'product_name': 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml',
                    'page_title': 'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos',
                    'url': 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-'
                           'perfume-feminino/p'}
        command = [CRAWLER_EXECUTABLE, '-s', 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-'
                                             'toilette-paco-rabanne-perfume-feminino/p']
        self.assertEqual(expected, json.loads(subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()))

    def test_crawl_hypnose(self):
        expected = {'product_name': 'Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml',
                    'page_title': 'Hypnôse Lancôme - Perfume Feminino - Época Cosméticos',
                    'url': 'http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p'}
        command = [CRAWLER_EXECUTABLE, '-s', 'http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-'
                                             'perfume-feminino/p']
        self.assertEqual(expected, json.loads(subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()))
