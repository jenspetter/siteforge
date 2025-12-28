import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import builder

"""
Tests for builder.py
"""
class BuilderTests(unittest.TestCase):

    def test_load_data_simple(self):
        # Loading from a single data file
        result = builder.load_data("../tests/resources/simple")
        expected = {'data': {'String': 'String', 'Boolean': 'Bool', 'Integer': 'Int', 'Float': 'Float'}}
        self.assertEqual(result, expected)

    def test_load_data_more(self):
        # Loading from 2 data files
        result = builder.load_data("../tests/resources/more")
        expected = {'data': {'String': 'String', 'Boolean': 'Bool', 'Integer': 'Int', 'Float': 'Float'}, 'data2': {'Person': {'Name': 'Eric', 'Age': 62}}}
        self.assertEqual(result, expected)

    def test_load_data_empty(self):
        # Loading nothing should return an empty collection
        self.assertEqual(builder.load_data(""), {})

    def test_load_data_not_existing_path(self):
        # Loading from an incorrect path should return an empty collection
        self.assertEqual(builder.load_data("../tests/resources/not_existing_hopefully"), {})

    def test_load_data_wrong_format(self):
        # Loading from a path with invalid formatted data (not .json) should return an empty collection
        self.assertEqual(builder.load_data("../tests/resources/wrong_format"), {})

if __name__ == '__main__':
    unittest.main()