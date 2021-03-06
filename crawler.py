#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This package is a crawler for extracting the product's name, page title and page's URL from the product pages on the
http://www.epocacosmeticos.com.br and is meant as a technical challenge for the admission process at SIEVE.
"""
import json
import os
import sys
import csv
import argparse
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
from time import sleep

import lxml.html
import lxml
import requests
from lxml.cssselect import CSSSelector

BASE_URL = 'http://www.epocacosmeticos.com.br'

__author_name__ = 'Flávio Pontes'
__author_email__ = 'flaviocpontes@gmail.com'
__author__ = '{} <{}>'.format(__author_name__, __author_email__)
__copyright__ = 'Copyright © 2016 Flávio Pontes'
__license__ = 'MIT'
__version_info__ = (1, 0)
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
    link_set = {link.get('href') for link in element_tree.cssselect('a')
                if link.get('href') and (link.get('href').startswith('http://www.epocacosmeticos.com.br') or
                                         link.get('href').startswith('/'))}
    return sorted(list(link_set))


def is_product_page(url, response_url):
    """Returns True if a page is a Product Page

        Args:
            url (str): The url to be evaluated
            reponse (requests.response): The http response

        Returns:
            bool: If the URL is for a product page.
    """
    if type(url) != str:
        raise ValueError("url must be a string")
    if url.endswith('/p') and url == response_url:
        return True
    return False


def get_page_contents(url):
    """Wrapper function to urllib request.
    For easier mocking and better readability

    Args:
        url(str): url to get contents from

    Returns:
        str: The page's HTML content
    """
    print('Visiting url: {}'.format(url))
    r = requests.get(BASE_URL + url if url.startswith('/') else url)
    return r.text, r


def visit_url(url, retries=3):
    """Retrives the HTML page at the URL and extracts the product info if present and all its links

    Args:
        url (str): The URL to be retrieved

    Returns:
        values (dict): The product data if present or None

    """
    for i in range(retries):
        try:
            html_page, http_response = get_page_contents(url)
            values = extract_values(html_page) if is_product_page(url, http_response.url) else None
            return values, extract_links(html_page), url
        except IndexError as e:
            print("Couldn't find productName for page {}".format(url))
            sleep(1)
        except Exception as e:
            print("The error {} occurred while processing page {}".format(e, url))
            sleep(1)
    return None, None, url


def write_values_to_csv(output, values):
    """Writes the values extracted from the product page to the csv file

    Args:
        output (str): The output filename
        values (list): The list of values to be written to the csv.
    """
    with open(output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(values)


def parse_args(args):
    """Parses the command line arguments

    Args:
        args (list): the list of cli arguments. /doesn't include the executable.

    Returns:
        argparse.namespace
    """
    parser = argparse.ArgumentParser(description="Crawls the site www.epocacosmeticos.com.br, acquiring data from the product pages.")
    parser.add_argument('-d', '--depth', default=1, type=int, help='The maximum link depth to crawl. Must be greater than 0.')
    parser.add_argument('-o', '--output', default='crawl_output.csv', type=str, help='The output csv file')
    parser.add_argument('-r', '--resume', default=None, type=str, help='The resume file filename')
    parser.add_argument('path', help='The starting path for the crawling')
    config = parser.parse_args(args)
    if config.path.startswith('/'):
        config.path = BASE_URL + config.path
    else:
        raise ValueError()
    if config.depth < 0:
        print('Depth must be an integer greater or equal to 0. Setting depth to 0.')
        config.depth = 0
    return config


def main(args):
    try:
        config = parse_args(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

    visited = []
    horizon = [config.path]

    open(config.output, 'w').close()

    for i in range(config.depth + 1):
        iteration_horizon = horizon.copy()
        horizon = []

        if not iteration_horizon:
            print("No more links to visit.")
            break

        while iteration_horizon:
            iteration_horizon, tasks = generate_tasks(iteration_horizon, visited)
            with Pool(processes=cpu_count()*4) as pool:
                result = pool.map(visit_url, tasks)
            visited = visited + tasks
            for values, links, url in result:
                horizon.extend(links or [])
                if values:
                    print('Product page found. Extracted {}'.format(values))
                    write_values_to_csv(config.output, [values.get('product_name'),
                                                        values.get('page_title'),
                                                        url])


def generate_tasks(iteration_horizon, visited):
    iteration_horizon = sorted(list({url for url in iteration_horizon if url not in visited}))
    tasks = iteration_horizon[:800]
    iteration_horizon = iteration_horizon[800:]
    return iteration_horizon, tasks


if __name__ == '__main__':
    main(sys.argv[1:])
