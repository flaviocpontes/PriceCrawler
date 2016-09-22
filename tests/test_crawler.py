import csv
import os
import unittest
import lxml

import crawler
from tests import TEST_FILE_PATH


class TestExtractProductName(unittest.TestCase):
    """Tests the extraction of the product name from a ElementTree"""

    def test_extract_from_ladymillion(self):
        expected = 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino'
        html = open(os.path.join(TEST_FILE_PATH,
                                 'lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_product_name(lxml.html.document_fromstring(html)))

    def test_extract_from_hypnose(self):
        expected = 'Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml'
        html = open(os.path.join(TEST_FILE_PATH, 'hypnose-eau-de-toilette-lancome-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_product_name(lxml.html.document_fromstring(html)))

    def test_extraction_from_synthetic_page(self):
        """Tests a synthetic page for value extraction"""
        expected = 'Fake Product 1'
        fake_html = open(os.path.join(TEST_FILE_PATH, 'mock_page.html')).read()
        self.assertEqual(expected,
                         crawler.extract_product_name(
                             lxml.html.document_fromstring(fake_html.format('My first Fake Product',
                                                                            'Fake Product 1',
                                                                            'page1/p',
                                                                            'page2/p',
                                                                            'page3/p'))))

    def test_extranction_from_invalid_page(self):
        html = open(os.path.join(TEST_FILE_PATH, 'prod_index_cabelos.html')).read()
        self.assertRaises(IndexError, crawler.extract_product_name, lxml.html.document_fromstring(html))


class TestExtractValues(unittest.TestCase):
    """Tests the extraction of the sought values from the test html files"""

    def test_extract_from_ladymillion(self):
        expected = {'product_name': 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino',
                    'page_title': 'Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos'}
        html = open(os.path.join(TEST_FILE_PATH,
                                 'lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino.html')).read()
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

    def test_extranction_from_invalid_page(self):
        html = open(os.path.join(TEST_FILE_PATH, 'prod_index_cabelos.html')).read()
        self.assertRaises(IndexError, crawler.extract_values, html)


class TestExtractLinks(unittest.TestCase):
    """Tests the extraction of the pages links"""

    def test_extract_from_ladymillion(self):
        expected = ['http://www.epocacosmeticos.com.br/',
                    'http://www.epocacosmeticos.com.br/212-vip-rose-eau-de-parfum-carolina-herrera-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/account/orders',
                    'http://www.epocacosmeticos.com.br/bahama-mama-the-balm-po-compacto-bronzeador/p',
                    'http://www.epocacosmeticos.com.br/cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/coloracao/tintura-para-cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/condicionador',
                    'http://www.epocacosmeticos.com.br/cabelos/de-14,9-a-49,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-160-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-50-a-89,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-90-a-159,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/finalizador',
                    'http://www.epocacosmeticos.com.br/cabelos/kits-para-cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/mascara-capilar',
                    'http://www.epocacosmeticos.com.br/cabelos/shampoo',
                    'http://www.epocacosmeticos.com.br/cabelos/tratamento',
                    'http://www.epocacosmeticos.com.br/carolina-herrera',
                    'http://www.epocacosmeticos.com.br/centralatendimento',
                    'http://www.epocacosmeticos.com.br/centralatendimento/vantagens-qualidade-confianca',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/banho/sabonete-e-gel-de-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/barba',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-100-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-200-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-40-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-9,9-a-39,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/kits-para-corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/pos-banho/hidratante',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/pos-banho/oleo',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/utilidades-diversas',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/cuidados-com-o-sol/protetor-solar',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-100-a-169,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-14,9-a-69,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-170-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-70-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/cuidados-faciais-especificos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/hidratantes',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/limpadores',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/nutricosmeticos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/olhos/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/dior',
                    'http://www.epocacosmeticos.com.br/ganhe-brindes-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/ganhe-brindes-tratamento',
                    'http://www.epocacosmeticos.com.br/giftList',
                    'http://www.epocacosmeticos.com.br/hair-remedy-cadiveu-mascara-para-cabelos/p',
                    'http://www.epocacosmeticos.com.br/j-adore-eau-de-parfum-dior-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/la-vie-est-belle-eau-de-parfum-lancome-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/lady-million-eau-de-parfum-paco-rabanne-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/lancamentos-cabelos',
                    'http://www.epocacosmeticos.com.br/lancamentos-corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/lancamentos-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/lancamentos-maquiagem',
                    'http://www.epocacosmeticos.com.br/lancamentos-tratamentos',
                    'http://www.epocacosmeticos.com.br/lancome',
                    'http://www.epocacosmeticos.com.br/legend-spirit-eau-de-toilette-montblanc-perfume-masculino/p',
                    'http://www.epocacosmeticos.com.br/maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/aplicadores-para-maquiagem/pincel-ou-aplicador',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-100-a-159,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-14,9-a-59,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-160-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-200-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-60-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/estojo-completo-e-kit-de-maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/face/base',
                    'http://www.epocacosmeticos.com.br/maquiagem/face/po-facial',
                    'http://www.epocacosmeticos.com.br/maquiagem/labios/batom',
                    'http://www.epocacosmeticos.com.br/maquiagem/olhos/mascara-para-cilios',
                    'http://www.epocacosmeticos.com.br/maquiagem/olhos/sombra',
                    'http://www.epocacosmeticos.com.br/maquiagem/primer-e-finalizador/fixador-da-maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/unhas/esmalte',
                    'http://www.epocacosmeticos.com.br/marcas',
                    'http://www.epocacosmeticos.com.br/outlet-cabelos',
                    'http://www.epocacosmeticos.com.br/outlet-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/outlet-maquiagem',
                    'http://www.epocacosmeticos.com.br/outlet-perfumes',
                    'http://www.epocacosmeticos.com.br/outlet-tratamentos',
                    'http://www.epocacosmeticos.com.br/paco-rabanne',
                    'http://www.epocacosmeticos.com.br/paco-rabanne/lady-million',
                    'http://www.epocacosmeticos.com.br/perfumes',
                    'http://www.epocacosmeticos.com.br/perfumes/de-100-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-200-a-299,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-29,9-a-69,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-300-a-399,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-400-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-70-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/kits-de-perfumes',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-feminino',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-feminino/paco-rabanne',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-infantil',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-masculino',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-para-o-corpo',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-unissex',
                    'http://www.epocacosmeticos.com.br/perfumes/perfumes-importados',
                    'http://www.epocacosmeticos.com.br/perfumes/perfumes-para-ambiente',
                    'http://www.epocacosmeticos.com.br/physical-fusion-uv-defense-spf-50-skinceuticals-protetor-solar/p',
                    'http://www.epocacosmeticos.com.br/pleats-please-l-eau-eau-de-toilette-issey-miyake-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/reative-c-natupele-rejuvenescedor-facial/p',
                    'http://www.epocacosmeticos.com.br/selecao/ofertas',
                    'http://www.epocacosmeticos.com.br/site/carrinho.aspx',
                    'http://www.epocacosmeticos.com.br/soft-cs1560b-cores-sortidas-curaprox-escova-dental/p',
                    'http://www.epocacosmeticos.com.br/tratamentos',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-19,9-a-79,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-200-a-299,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-300-a-499,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-500-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-80-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/cuidados-faciais-especificos ',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/hidratantes-faciais',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/rejuvenescedores-faciais',
                    'http://www.epocacosmeticos.com.br/tratamentos/labios/rejuvenescedores-labiais',
                    'http://www.epocacosmeticos.com.br/tratamentos/olhos/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/tratamentos/unhas',
                    'http://www.epocacosmeticos.com.br/unhas',
                    'http://www.epocacosmeticos.com.br/unhas-de-gel-medias-autocolantes-impress-message-me/p',
                    'http://www.epocacosmeticos.com.br/unhas/de-10-a-19,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-100-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-20-a-49,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-50-a-99,99?map=c,priceFrom']
        html = open(os.path.join(TEST_FILE_PATH,
                                 'lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_links(html))

    def test_extract_from_hypnose(self):
        expected = ['http://www.epocacosmeticos.com.br/',
                    'http://www.epocacosmeticos.com.br/account/orders',
                    'http://www.epocacosmeticos.com.br/bahama-mama-the-balm-po-compacto-bronzeador/p',
                    'http://www.epocacosmeticos.com.br/cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/coloracao/tintura-para-cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/condicionador',
                    'http://www.epocacosmeticos.com.br/cabelos/de-14,9-a-49,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-160-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-50-a-89,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/de-90-a-159,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/cabelos/finalizador',
                    'http://www.epocacosmeticos.com.br/cabelos/kits-para-cabelos',
                    'http://www.epocacosmeticos.com.br/cabelos/mascara-capilar',
                    'http://www.epocacosmeticos.com.br/cabelos/shampoo',
                    'http://www.epocacosmeticos.com.br/cabelos/tratamento',
                    'http://www.epocacosmeticos.com.br/centralatendimento',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/banho/sabonete-e-gel-de-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/barba',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-100-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-200-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-40-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/de-9,9-a-39,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/kits-para-corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/pos-banho/hidratante',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/pos-banho/oleo',
                    'http://www.epocacosmeticos.com.br/corpo-e-banho/utilidades-diversas',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/cuidados-com-o-sol/protetor-solar',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-100-a-169,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-14,9-a-69,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-170-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/de-70-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/cuidados-faciais-especificos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/hidratantes',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/limpadores',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/face/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/nutricosmeticos',
                    'http://www.epocacosmeticos.com.br/dermocosmeticos/olhos/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/ganhe-brindes-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/ganhe-brindes-tratamento',
                    'http://www.epocacosmeticos.com.br/giftList',
                    'http://www.epocacosmeticos.com.br/hair-remedy-cadiveu-mascara-para-cabelos/p',
                    'http://www.epocacosmeticos.com.br/hypnose-eau-de-parfum-lancome-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/la-nuit-tresor-l-eau-de-parfum-lancome-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/la-vie-est-belle-eau-de-parfum-lancome-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/lancamentos-cabelos',
                    'http://www.epocacosmeticos.com.br/lancamentos-corpo-e-banho',
                    'http://www.epocacosmeticos.com.br/lancamentos-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/lancamentos-maquiagem',
                    'http://www.epocacosmeticos.com.br/lancamentos-tratamentos',
                    'http://www.epocacosmeticos.com.br/lancome',
                    'http://www.epocacosmeticos.com.br/legend-spirit-eau-de-toilette-montblanc-perfume-masculino/p',
                    'http://www.epocacosmeticos.com.br/maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/aplicadores-para-maquiagem/pincel-ou-aplicador',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-100-a-159,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-14,9-a-59,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-160-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-200-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/de-60-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/maquiagem/estojo-completo-e-kit-de-maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/face/base',
                    'http://www.epocacosmeticos.com.br/maquiagem/face/po-facial',
                    'http://www.epocacosmeticos.com.br/maquiagem/labios/batom',
                    'http://www.epocacosmeticos.com.br/maquiagem/olhos/mascara-para-cilios',
                    'http://www.epocacosmeticos.com.br/maquiagem/olhos/sombra',
                    'http://www.epocacosmeticos.com.br/maquiagem/primer-e-finalizador/fixador-da-maquiagem',
                    'http://www.epocacosmeticos.com.br/maquiagem/unhas/esmalte',
                    'http://www.epocacosmeticos.com.br/marcas',
                    'http://www.epocacosmeticos.com.br/outlet-cabelos',
                    'http://www.epocacosmeticos.com.br/outlet-dermocosmeticos',
                    'http://www.epocacosmeticos.com.br/outlet-maquiagem',
                    'http://www.epocacosmeticos.com.br/outlet-perfumes',
                    'http://www.epocacosmeticos.com.br/outlet-tratamentos',
                    'http://www.epocacosmeticos.com.br/paco-rabanne',
                    'http://www.epocacosmeticos.com.br/perfumes',
                    'http://www.epocacosmeticos.com.br/perfumes/de-100-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-200-a-299,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-29,9-a-69,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-300-a-399,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-400-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/de-70-a-99,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/perfumes/kits-de-perfumes',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-feminino',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-feminino/lancome',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-infantil',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-masculino',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-para-o-corpo',
                    'http://www.epocacosmeticos.com.br/perfumes/perfume-unissex',
                    'http://www.epocacosmeticos.com.br/perfumes/perfumes-importados',
                    'http://www.epocacosmeticos.com.br/perfumes/perfumes-para-ambiente',
                    'http://www.epocacosmeticos.com.br/physical-fusion-uv-defense-spf-50-skinceuticals-protetor-solar/p',
                    'http://www.epocacosmeticos.com.br/pleats-please-l-eau-eau-de-toilette-issey-miyake-perfume-feminino/p',
                    'http://www.epocacosmeticos.com.br/reative-c-natupele-rejuvenescedor-facial/p',
                    'http://www.epocacosmeticos.com.br/selecao/ofertas',
                    'http://www.epocacosmeticos.com.br/site/carrinho.aspx',
                    'http://www.epocacosmeticos.com.br/soft-cs1560b-cores-sortidas-curaprox-escova-dental/p',
                    'http://www.epocacosmeticos.com.br/tratamentos',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-19,9-a-79,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-200-a-299,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-300-a-499,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-500-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/de-80-a-199,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/cuidados-faciais-especificos ',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/hidratantes-faciais',
                    'http://www.epocacosmeticos.com.br/tratamentos/face/rejuvenescedores-faciais',
                    'http://www.epocacosmeticos.com.br/tratamentos/labios/rejuvenescedores-labiais',
                    'http://www.epocacosmeticos.com.br/tratamentos/olhos/rejuvenescedores',
                    'http://www.epocacosmeticos.com.br/tratamentos/unhas',
                    'http://www.epocacosmeticos.com.br/unhas',
                    'http://www.epocacosmeticos.com.br/unhas-de-gel-medias-autocolantes-impress-message-me/p',
                    'http://www.epocacosmeticos.com.br/unhas/de-10-a-19,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-100-a-5000?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-20-a-49,99?map=c,priceFrom',
                    'http://www.epocacosmeticos.com.br/unhas/de-50-a-99,99?map=c,priceFrom']
        html = open(os.path.join(TEST_FILE_PATH, 'hypnose-eau-de-toilette-lancome-perfume-feminino.html')).read()
        self.assertEqual(expected, crawler.extract_links(html))

    def test_extraction_from_synthetic_page(self):
        """Tests a synthetic page for value extraction"""
        expected = ['http://www.epocacosmeticos.com.br/page1/p',
                    'http://www.epocacosmeticos.com.br/page2/p',
                    'http://www.epocacosmeticos.com.br/page3/p']
        fake_html = open(os.path.join(TEST_FILE_PATH, 'mock_page.html')).read()
        self.assertEqual(expected, crawler.extract_links(fake_html.format('My first Fake Product',
                                                                          'Fake Product 1',
                                                                          'page1/p',
                                                                          'page2/p',
                                                                          'page3/p')))


class TestIsProductPage(unittest.TestCase):
    """Tests for checking if a page is a prodcutd page"""

    def test_is_product_page(self):
        self.assertTrue(crawler.is_product_page(
            'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p',
            'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p'))

    def test_is_not_product_page(self):
        self.assertFalse(crawler.is_product_page(
            'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino',
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
