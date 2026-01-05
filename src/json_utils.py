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

    path = os.path.join(os.path.dirname(__file__), path)
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
    
    path = os.path.join(os.path.dirname(__file__), path)
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