import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import builder

"""
Tests for builder.py
"""
class BuilderTests(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()