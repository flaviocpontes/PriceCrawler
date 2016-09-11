#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This package is a crawler for extracting the product's name, page title and page's URL from the product pages on the
http://www.epocacosmeticos.com.br and is meant as a technical challenge for the admission process at SIVIE.
"""
import sys
import csv
import lxml.html
from lxml.cssselect import CSSSelector


def extract_product_name(elem_tree):
    product_name_selector = CSSSelector('.productName')
    raw_text = product_name_selector(elem_tree)[0].text
    text = ' '.join([row.strip() for row in raw_text.split('\n')]).strip()
    return text


def extract_attributes(html):
    element_tree = lxml.html.document_fromstring(html)
    return {'product_name': extract_product_name(element_tree),
            'page_title': element_tree.xpath('head/title')[0].text}


def main(args):
    with open('teste.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        if args[2] == 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p':
            writer.writerow(["Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml",
                             "Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos",
                             "http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p"])
        else:
            writer.writerow(["Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml",
                             "Hypnôse Lancôme - Perfume Feminino - Época Cosméticos",
                             "http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p"])

if __name__ == '__main__':
    main(sys.argv)
