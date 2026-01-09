import unittest

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import json_functions as funcs

"""
Tests for json_functions.py
"""
class JsonUtilsTests(unittest.TestCase):

    def test_current_year(self):
        year = datetime.today().year
        self.assertEqual(year, funcs.current_year())

if __name__ == '__main__':
    unittest.main()