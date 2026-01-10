import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../siteforge")

import builder
from json_function_registration import json_func

"""
Tests for builder.py
"""
class BuilderTests(unittest.TestCase):

    # load_content
    def test_load_content(self):
        # Loading from a single data file
        result = builder.load_content("../tests/resources/simple")
        expected = {'data': {'String': 'String', 'Boolean': 'Bool', 'Integer': 'Int', 'Float': 'Float'}}
        self.assertEqual(result, expected)

    def test_load_content_with_func_zero(self):
        result = builder.load_content("../tests/resources/content/func/zero")
        expected = {'zero': {'zero': 0}}
        self.assertEqual(result, expected)

    def test_load_content_with_func_add(self):
        result = builder.load_content("../tests/resources/content/func/add")
        expected = {}
        expected['add_args'] = {'add': 3}
        expected['add_kwargs'] = {'add': 3}
        self.assertEqual(result, expected)

    # json test methods
    @json_func
    def zero():
        return 0
    
    @json_func
    def add(left, right):
        return left + right

    # load_build_registry

    def test_load_build_registry(self):
        # Loading a build registry collection
        result = builder.load_build_registry("../tests/resources/build_registry/simple.json")
        expected = [{'template': 'GreatTemplate', 'output': 'index.html'}, {'template': 'GreatTemplate', 'output': 'coolproject.html'}]
        self.assertEqual(result, expected)

    def test_load_build_registry_empty(self):
        # Loading nothing should return an empty collection
        self.assertEqual(builder.load_build_registry(""), {})

    def test_load_build_registry_not_existing_path(self):
        # Loading a file that cannot be found should return an empty collection
        self.assertEqual(builder.load_build_registry("../tests/resources/build_registry/not_existing_hopefully.json"), {})

    def test_load_build_registry_missing_template(self):
        # Loading a file with a missing 'template' key. Should return an empty collection
        self.assertEqual(builder.load_build_registry("../tests/resources/build_registry/missing_template_key.json"), {})

    def test_load_build_registry_missing_output(self):
        # Loading a file with a missing 'output' key. Should return an empty collection
        self.assertEqual(builder.load_build_registry("../tests/resources/build_registry/missing_output_key.json"), {})

    # load_asset_registry

    def test_load_asset_registry(self):
        # Loading an asset registry collection
        result = builder.load_asset_registry("../tests/resources/asset_registry/simple.json")
        expected = [{'Source': 'assets', 'Destination': 'assets'}]
        self.assertEqual(result, expected)

    def test_load_asset_registry_empty(self):
        # Loading nothing should return an empty collection
        self.assertEqual(builder.load_asset_registry(""), {})

    def test_load_asset_registry_not_existing_path(self):
        # Loading a file that cannot be found should return an empty collection
        self.assertEqual(builder.load_asset_registry("../tests/resources/asset_registry/not_existing_hopefully.json"), {})

    def test_load_asset_registry_missing_source(self):
        # Loading a file with a missing 'Source' key. Should return an empty collection
        self.assertEqual(builder.load_asset_registry("../tests/resources/asset_registry/missing_source_key.json"), {})

    def test_load_asset_registry_missing_destination(self):
        # Loading a file with a missing 'Destination' key. Should return an empty collection
        self.assertEqual(builder.load_asset_registry("../tests/resources/asset_registry/missing_destination_key.json"), {})

    # get_processed_content_from_build_item

    def test_get_processed_content_from_build_item_no_processing_needed(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!"
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html"
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is nothing as we no build item processing was needed
        expected = None
        self.assertEqual(result, expected)

    def test_get_processed_content_from_build_item_simple_bound(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!"
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html",
            "boundContext": [
                {
                    "Name": "BoundEntry",
                    "Where": {
                        "Key": "Id",
                        "Value": "Test"
                    }
                }
            ]
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is to be bound
        expected = {}
        expected['BoundEntry'] = content['Entry']
        self.assertEqual(result, expected)

    def test_get_processed_content_from_build_item_wrong_key_bound(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!"
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html",
            "boundContext": [
                {
                    "Name": "BoundEntry",
                    "Where": {
                        "Key": "IncorrectKey",
                        "Value": "Test"
                    }
                }
            ]
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is to not be bound as we bound with the wrong key
        expected = None
        self.assertEqual(result, expected)

    def test_get_processed_content_from_build_item_wrong_value_bound(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!"
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html",
            "boundContext": [
                {
                    "Name": "BoundEntry",
                    "Where": {
                        "Key": "Id",
                        "Value": "IncorrectValue"
                    }
                }
            ]
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is to not be bound as we bound with the wrong value
        expected = None
        self.assertEqual(result, expected)

    def test_get_processed_content_from_build_item_complex_bound(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!"
        }
        content['Entry2'] = {
            "Id": "Test2",
            "Title": "Cool 2nd Title",
            "Description": "This is the 2nd best description!"
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html",
            "boundContext": [
                {
                    "Name": "BoundEntry",
                    "Where": {
                        "Key": "Id",
                        "Value": "Test"
                    }
                }
            ]
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is to be bound
        expected = {}
        expected['BoundEntry'] = content['Entry']
        self.assertEqual(result, expected)

    def test_get_processed_content_from_build_item_depth_bound(self):
        content = {}
        content['Entry'] = {
            "Id": "Test",
            "Title": "Cool Title",
            "Description": "This is the best description!",
            "Person": {
                "Name": "Friday",
                "Age": 43
            }
        }
        
        build_item_json = {
            "template": "home.html",
            "output": "index.html",
            "boundContext": [
                {
                    "Name": "Friday",
                    "Where": {
                        "Key": "Name",
                        "Value": "Friday"
                    }
                }
            ]
        }

        result = builder.get_processed_content_from_build_item(build_item_json, content)
        # Expected is to be bound
        expected = {}
        expected['Friday'] = content['Entry']['Person']
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()