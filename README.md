# Crawler

Crawler is a Web Crawler, seeking product data from the site http://www.epocacosmeticos.com.br, specifically product names, the product page's title and it's URL.

It is very simple, single threaded program, built whenever possible on the python standard library with 3 exceptions: requests, lxml and cssselect.

Extensive tests are provided, with nearly 100% test coverage.
 
## Installation:

Crawler is developed in **Ubuntu 16.04 64-bit** with python 3.5.1. It is only tested in that configuration.
Installation requires the following:

`sudo apt-get install python3-lxml python3-cssselect python3-requests`

Then, you just need to copy `crawler.py` to your desired directory and give it execution capabilities with `chmod +x crawler.py`.

## Usage

Crawler is limited to the www.epocacosmeticos.com.br domain. It works by collecting all links from the web page and visiting all those links in order, collecting the links from those pages and appending them to the visiting list.

The usage semantics is really simple: "Crawl **n** pages deep and output the product data found to **file.csv**, saving state in **file.json** so we can restart later, starting from **path**".

`crawler.py -d [depth] -o [output] -r [state file] [path]`

For example:

`crawler.py -d 1 -o output.csv -r resume.json /` visits the path page and all the pages linked to it.

`crawler.py -d 0 -o output.csv -r resume.json /lady-million-eau-my-gold-eau-de-toilette-paco-rabanne-perfume-feminino/p` visits only the path page and extracts it's information since it is a product page.
