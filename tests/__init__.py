import os
import sys

TESTS_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(TESTS_PATH)
TEST_FILE_PATH = os.path.join(PROJECT_ROOT, 'test_files')
CRAWLER_PATH = os.path.join(PROJECT_ROOT, 'crawler')

sys.path.extend([CRAWLER_PATH])