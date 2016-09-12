#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This package is a crawler for extracting the product's name, page title and page's URL from the product pages on the
http://www.epocacosmeticos.com.br and is meant as a technical challenge for the admission process at SIVIE.
"""
import sys
import csv
import argparse
import urllib.parse
import urllib.request

import lxml.html
from lxml.cssselect import CSSSelector


def extract_product_name(elem_tree: lxml.etree):
    product_name_selector = CSSSelector('.productName')
    raw_text = product_name_selector(elem_tree)[0].text
    text = ' '.join([row.strip() for row in raw_text.split('\n')]).strip()
    return text


def extract_attributes(html: str):
    """"""
    element_tree = lxml.html.document_fromstring(html)
    return {'product_name': extract_product_name(element_tree),
            'page_title': element_tree.xpath('head/title')[0].text}


def parse_args(args):
    parser = argparse.ArgumentParser(description="Crawls the site www.epocacosmeticos.com.br, acquiring data from the product pages.")
    parser.add_argument('-o', '--output', type=str, help='The output csv file')
    parser.add_argument('url', help='The base url for the crawling session')
    config = parser.parse_args(args)
    if urllib.parse.urlparse(config.url).netloc != 'www.epocacosmeticos.com.br' :
        raise ValueError('URL must be from the www.epocacosmeticos.com.br domain')
    return config


def main(args):
    try:
        config = parse_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    with open(config.output, 'w') as csvfile:
        writer = csv.writer(csvfile)
        html_page = urllib.request.urlopen(config.url).read()
        result = extract_attributes(html_page)
        writer.writerow([result.get('product_name'),
                        result.get('page_title'),
                        config.url])

if __name__ == '__main__':
    main(sys.argv[1:])
