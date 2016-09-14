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
import lxml
from lxml.cssselect import CSSSelector


def extract_product_name(elem_tree):
    """Extracts the Product name from the Product page

    Args:
        elem_tree: The Element tree representing the DOM

    Returns:
        str: The product name
    """
    product_name_selector = CSSSelector('.productName')
    raw_text = product_name_selector(elem_tree)[0].text
    text = ' '.join([row.strip() for row in raw_text.split('\n')]).strip()
    return text


def extract_page_title(element_tree):
    """Extracts the page title

    Agrs:
        element_tree (lxml.etree.Element): The element

    Returns:
        str: The page title
    """
    return element_tree.xpath('head/title')[0].text


def extract_values(html: str):
    """Extracts the sought values from the product page

    Args:
        html (str): The html document

    Returns:
        dict: The extracted page title and product name
    """
    element_tree = lxml.html.document_fromstring(html)
    return {'product_name': extract_product_name(element_tree),
            'page_title': extract_page_title(element_tree)}


def extract_links(html: str):
    """Extract the links in the html page that are pointed to the same domain

    Args:
        html (str): The HTMl documento for parsing

    Returns:
        Set: A set containing all the links in the html page.
    """
    element_tree = lxml.html.document_fromstring(html)
    return {link.get('href') for link in element_tree.cssselect('a')
            if link.get('href') and link.get('href').startswith('http://www.epocacosmeticos.com.br')}


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
        result = extract_values(html_page)
        writer.writerow([result.get('product_name'),
                        result.get('page_title'),
                        config.url])

if __name__ == '__main__':
    main(sys.argv[1:])
