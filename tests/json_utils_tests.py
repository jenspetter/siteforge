import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import json_utils

"""
Tests for json_utils.py
"""
class JsonUtilsTests(unittest.TestCase):

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

    # get_filtered_objects

    def test_get_filtered_objects_matching_key_value(self):
        json = {
            'key': 'value',
            'AnotherKey': 'AnotherValue'
        }

        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="key", value="value"))

        self.assertEquals(len(result), 1)
        self.assertEqual(result[0], json)

    def test_get_filtered_objects_matching_key_value_half(self):
        json = [
            {
                'key': 'value',
                'AnotherKey': 'AnotherValue'
            },
            {
                'IncorrectKey': 'value',
                'DifferentKey': 'DifferentValue'
            }
        ]

        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="key", value="value"))

        self.assertEquals(len(result), 1)
        self.assertEqual(result[0], json[0])

    def test_get_filtered_objects_matching_key_value_multiple(self):
        json = [
            {
                'key': 'value',
                'AnotherKey': 'AnotherValue'
            },
            {
                'key': 'value',
                'DifferentKey': 'DifferentValue'
            }
        ]

        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="key", value="value"))

        self.assertEquals(len(result), 2)
        self.assertEqual(result[0], json[0])
        self.assertEqual(result[1], json[1])

    def test_get_filtered_objects_not_matching_key(self):
        json = {
            'key': 'value',
            'AnotherKey': 'AnotherValue'
        }

        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="incorrectKey", value="value"))

        self.assertEquals(len(result), 0)

    def test_get_filtered_objects_not_matching_value(self):
        json = {
            'key': 'value',
            'AnotherKey': 'AnotherValue'
        }

        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="key", value="incorrectValue"))

        self.assertEquals(len(result), 0)

    def test_get_filtered_objects_none_json(self):
        json = None
        result = json_utils.get_filtered_objects(json, json_utils.JsonFilter(key="key", value="value"))

        self.assertEquals(result, [])

    def test_get_filtered_objects_none_filter(self):
        json = {
            'key': 'value',
            'AnotherKey': 'AnotherValue'
        }

        result = json_utils.get_filtered_objects(json, None)

        self.assertEquals(result, [])

if __name__ == '__main__':
    unittest.main()