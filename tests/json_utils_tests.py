import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import json_utils

"""
Tests for json_utils.py
"""
class BuilderTests(unittest.TestCase):

    # JSonFilter

    def test_json_filter_init(self):
        filter = json_utils.JsonFilter(key="k", value="v")
        self.assertEqual(filter.key, "k")
        self.assertEqual(filter.value, "v")

    # load_objects

    def test_load_objects_simple(self):
        # Loading from a single data file
        result = json_utils.load_objects("../tests/resources/simple")
        expected = {'data': {'String': 'String', 'Boolean': 'Bool', 'Integer': 'Int', 'Float': 'Float'}}
        self.assertEqual(result, expected)

    def test_load_objects_more(self):
        # Loading from 2 data files
        result = json_utils.load_objects("../tests/resources/more")
        expected = {'data': {'String': 'String', 'Boolean': 'Bool', 'Integer': 'Int', 'Float': 'Float'}, 'data2': {'Person': {'Name': 'Eric', 'Age': 62}}}
        self.assertEqual(result, expected)

    def test_load_objects_empty(self):
        # Loading nothing should return an empty collection
        self.assertEqual(json_utils.load_objects(""), {})

    def test_load_objects_not_existing_path(self):
        # Loading from an incorrect path should return an empty collection
        self.assertEqual(json_utils.load_objects("../tests/resources/not_existing_hopefully"), {})

    def test_load_objects_wrong_format(self):
        # Loading from a path with invalid formatted data (not .json) should return an empty collection
        self.assertEqual(json_utils.load_objects("../tests/resources/wrong_format"), {})
        
    # load_container

    def test_load_container(self):
        # Loading a container
        result = json_utils.load_container("../tests/resources/build_registry/simple.json")
        expected = [{'template': 'GreatTemplate', 'output': 'index.html'}, {'template': 'GreatTemplate', 'output': 'coolproject.html'}]
        self.assertEqual(result, expected)

    def test_load_container_empty(self):
        # Loading nothing should return an empty collection
        self.assertEqual(json_utils.load_container(""), {})

    def test_load_container_not_existing_path(self):
        # Loading a file that cannot be found should return an empty collection
        self.assertEqual(json_utils.load_container("../tests/resources/build_registry/not_existing_hopefully.json"), {})

    def test_load_container_required_key(self):
        # Loading a file that must contain a specific key
        result = json_utils.load_container("../tests/resources/build_registry/simple.json", ["template"])
        expected = [{'template': 'GreatTemplate', 'output': 'index.html'}, {'template': 'GreatTemplate', 'output': 'coolproject.html'}]
        self.assertEqual(result, expected)

    def test_load_container_missing_required_key(self):
        # Loading a file that must contain a specific key that isn't there, which should result in an empty container
        self.assertEqual(json_utils.load_container("../tests/resources/build_registry/simple.json", ["requiredKey"]), {})

if __name__ == '__main__':
    unittest.main()