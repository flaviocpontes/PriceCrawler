#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This package is a crawler for extracting the product's name, page title and page's URL from the product pages on the
http://www.epocacosmeticos.com.br and is meant as a technical challenge for the admission process at SIVIE.
"""
import os
import sys
import csv
import argparse
import urllib.parse
import urllib.request

import lxml.html
import lxml
from lxml.cssselect import CSSSelector

__author_name__ = 'Flávio Pontes'
__author_email__ = 'flaviocpontes@gmail.com'
__author__ = '{} <{}>'.format(__author_name__, __author_email__)
__copyright__ = 'Copyright © 2016 Flávio Pontes'
__license__ = 'MIT'
__version_info__ = (0, 1, 'alpha')
__version__ = '.'.join(map(str, __version_info__))


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


def extract_values(html: str):
    """Extracts the sought values from the product page

    Args:
        html (str): The html document

    Returns:
        dict: The extracted page title and product name
    """
    element_tree = lxml.html.document_fromstring(html)
    return {'product_name': extract_product_name(element_tree),
            'page_title': element_tree.xpath('head/title')[0].text}


def extract_links(html: str):
    """Extract the links in the html page that are pointed to the same domain

    Args:
        html (str): The HTMls documento for parsing

    Returns:
        Set: A set containing all the links in the html page that are from the epocacosmeticos.com.br domain.
    """
    element_tree = lxml.html.document_fromstring(html)
    return sorted(list({link.get('href') for link in element_tree.cssselect('a')
                        if link.get('href') and link.get('href').startswith('http://www.epocacosmeticos.com.br')}))


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


def write_values_to_csv(output, values):
    """Writes the values extracted from the product page to the csv file

    Args:
        output (str): The output filename
        values (list): The list of values to be written to the csv.
    """
    with open(output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(values)


def get_page_contents(url):
    """Wrapper function to urllib request.
    For easier mocking and better readability

    Args:
        url(str): url to get contents from

    Returns:
        str: The page's HTML content
    """
    print('Visiting url: {}'.format(url))
    return urllib.request.urlopen(url).read()


def visit_url(url):
    html_page = get_page_contents(url)
    values = extract_values(html_page) if is_product_page(url) else None
    return values, extract_links(html_page)


def main(args):
    try:
        config = parse_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    visited = []
    horizon = [config.url]
    if not os.path.exists(config.output):
        open(config.output, 'w').close()

    for i in range(config.depth):
        iteration_horizon = horizon.copy()
        horizon = []
        for url in iteration_horizon:
            if url in visited:
                iteration_horizon[0]
                continue
            values, links = visit_url(url)
            visited.append(iteration_horizon[0])
            horizon.extend(links)
            if values:
                print('Product page found. Extracted {}'.format(values))
                write_values_to_csv(config.output, [values.get('product_name'),
                                                    values.get('page_title'),
                                                    url])

if __name__ == '__main__':
    main(sys.argv[1:])
