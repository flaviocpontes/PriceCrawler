import os
import sys

__author_name__ = 'Flávio Pontes'
__author_email__ = 'flaviocpontes@gmail.com'
__author__ = '{} <{}>'.format(__author_name__, __author_email__)

TESTS_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(TESTS_PATH)
TEST_FILE_PATH = os.path.join(PROJECT_ROOT, 'test_files')

sys.path.insert(0, os.path.abspath(PROJECT_ROOT))