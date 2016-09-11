#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from lxml import html


def extract_attributes(html_string):
    tree = html.fromstring

    return {'product_name': 'Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml',
            'page_title': tree.xpath('/html/head/title')[0].text}


def main(args):
    if args[2] == 'http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p':
        print('{"product_name": "Lady Million Eau my Gold Eau de Toilette Paco Rabanne - Perfume Feminino - 30ml",'
              '"page_title": "Perfume Lady Million Eau my Gold EDT Paco Rabanne Feminino - Época Cosméticos",'
              '"url": "http://www.epocacosmeticos.com.br/lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p"}')
    else:
        print('{"product_name": "Hypnôse Eau de Toilette Lancôme - Perfume Feminino - 30ml",'
              '"page_title": "Hypnôse Lancôme - Perfume Feminino - Época Cosméticos",'
              '"url": "http://www.epocacosmeticos.com.br/hypnose-eau-de-toilette-lancome-perfume-feminino/p"}')

if __name__ == '__main__':
    main(sys.argv)
