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


def is_product_page(url):
    """Returns True if a page is a Product Page

        Args:
            url (str): The url to be evaluated

        Returns:
            bool: If the URL is for a product page.
        """
    if type(url) != str:
        raise ValueError("url must be a string")
    if url.endswith('/p'):
        return True
    return False


def parse_args(args):
    """Parses the command line arguments

    Args:
        args (list): the list of cli arguments. /doesn't include the executable.

    Returns:
        argparse.namespace

    """
    parser = argparse.ArgumentParser(description="Crawls the site www.epocacosmeticos.com.br, acquiring data from the product pages.")
    parser.add_argument('-d', '--depth', default=1, type=int, help='The maximum link depth to crawl. Must be greater than 0.')
    parser.add_argument('-o', '--output', type=str, help='The output csv file')
    parser.add_argument('url', help='The base url for the crawling session')
    config = parser.parse_args(args)
    if urllib.parse.urlparse(config.url).netloc != 'www.epocacosmeticos.com.br' :
        raise ValueError('URL must be from the www.epocacosmeticos.com.br domain')
    if config.depth < 1:
        print('Depth must be an integer greater than 0. Setting depth to 1.')
        config.depth = 1
    return config


def main(args):
    try:
        config = parse_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    visited = []
    horizon = [config.url]
    open(config.output, 'w').close()

    for i in range(config.depth):
        for n, url in enumerate(horizon):
            if url in visited:
                horizon.pop(n)
                continue
            html_page = urllib.request.urlopen(config.url).read()
            values = []
            if is_product_page(url):
                values = extract_values(html_page)
            visited.append(horizon.pop(n))
            horizon.extend(list(extract_links(html_page)))
            if values:
                with open(config.output, 'a+') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([values.get('product_name'),
                                     values.get('page_title'),
                                     url])

if __name__ == '__main__':
    main(sys.argv[1:])
