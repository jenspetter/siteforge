import json
import os
from pathlib import Path
JSON_EXTENSION = '.json'

"""
Containing utilities for json operations
"""

class JsonFilter:
    """
    Key value pair storage for referencing a key value pair of a json value
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

def load_objects(path):
    """
    Loading json data where the input is expected to be a path to input files\n
    Data will be loaded in as a dictionary, where\n
    - The key is the name of the file
    - The value is the loaded json structure 
    
    :param path: Path to the directory containing input files
    """

    data = {}
    if path == "":
        print("Failed to load data as requested path is empty")
        return data

    path = str(Path(path).resolve())
    if not os.path.exists(path):
        print("Failed to load data as requested path does not exist")
        return data

    for file in os.listdir(path):
        file = os.path.join(path, file)
        if not file.endswith('.json'):
            print("Ignoring input data '" + file + "' as file is not a valid .json file")
            continue

        name = Path(file).stem
        data[name] = json.load(open(file, encoding="utf-8"))

    return data

def load_container(path, required_properties = []):
    """
    Loading json data where the input is expected to be a container\n
    Includes the possibility to check if items in the container have certain properties
    
    :param path: Path to the json file
    :param required_properties: Required properties that all entries in the container should have
    """

    if path == "":
        print("Failed to load data as requested path is empty")
        return {}
    
    path = str(Path(path).resolve())
    if not os.path.exists(path):
        print("Failed to load json at path '" + path + "' as the file doesn't exist")
        return {}

    if not path.endswith(JSON_EXTENSION):
        print("Failed to load json at path '"  + path + "' as the file isn't a valid" + JSON_EXTENSION + " file")
        return {}
    
    with open(path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Only check required properties if needed
    if required_properties == [] or None:
        return data

    for entry in data:
        # Check if all required propereties exist
        for required_property in required_properties:
            if not required_property in entry:
                print('Missing required entry: ', required_property)
                print("Value: ", entry)
                return {}

    return data

def _get_objects_with_key(json, key):
    """
    Setup to recursively search (part of) the input json that has the input key
    
    :param json: The input json
    :param key: The requested key
    """

    if isinstance(json, dict):
        for k, v in json.items():
            if k == key:
                yield json
            else:
                yield from _get_objects_with_key(v, key)
    elif isinstance(json, list):
        for item in json:
            yield from _get_objects_with_key(item, key)

def get_filtered_objects(json, filter):
    """
    Get (part of) the input json based on a key-value filter
    
    :param json: The input json
    :param filter: The filter, has to be of the JSonFilter type
    """

    if not isinstance(json, object):
        print("Failed to get filtered json object as the json passed through is not an object")
        return []

    if not isinstance(filter, JsonFilter):
        print("Failed to get filtered json object as one of the filtered items passed through is not a filter")
        return []

    result = list(_get_objects_with_key(json, filter.key))
    matching_result = []

    for r in result:
        if r[filter.key] == filter.value:
            matching_result.append(r)

    return matching_result
