import json
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BUILD_REGISTRY_PATH = "../data/build_registry.json"
BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION = "template"
BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION = "output"

ASSET_REGISTRY_PATH = "../data/asset_registry.json"
ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION = "Source"
ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION = "Destination"

CONTENT_PATH = "../data/content"

""" Containing functionality to build the website
    """

env = Environment(loader=FileSystemLoader("templates"))

def load_data(content_path):
    """ Load json data
    """

    data = {}
    if content_path == "":
        print("Failed to load data as requested path is empty")
        return data

    path = os.path.join(os.path.dirname(__file__), content_path)
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

def _validate_registry(path, required_properties):
    """
    Validate the json format of a registry
    
    :param path: The path to the json file containing the registry
    :param required_properties: Required properties that all entries in the registry should adhere to
    """

    if path == "":
        print("Failed to load data as requested path is empty")
        return {}
    
    path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(path):
        print("Failed to load build registry at path '" + path + "' as the file doesn't exist")
        return {}

    if not path.endswith('.json'):
        print("Failed to load build registry at path '"  + path + "' as the file isn't a valid .json file")
        return {}
    
    with open(path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        # Check if all required propereties exist
        for required_property in required_properties:
            if not required_property in entry:
                print('Missing required entry: ', required_property)
                print("Value: ", entry)
                return {}

        unexpected = set(entry) - required_properties
        if(unexpected):
            print("Failed to load build registry at path '" + path + "' as (an) unexpected key(s) were found")
            print("Expected key(s): ", required_properties)
            print("Unexpected key(s): ", unexpected)
            print("Value: ", entry)
            return {}

    return data

def load_build_registry(path):
    """
    Loading build registry data\n
    Build registry data being data that defines what to build and how to build it\n
    We both load and validate the data. The data requiring to be a .json file
    
    :param path: Path to the build registry file.
    """

    return _validate_registry(path, {BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION, BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION})

def load_asset_registry(path):
    """
    Loading asset registry data\n
    Asset registry data being data that defines what to copy over as asset data to the output directory of the build\n
    We both load and validate the data. The data requiring to be a .json file
    
    :param path: Path to the asset registry file.
    """

    return _validate_registry(path, {ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION, ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION})

def render(template_name, **args):
    """ Get a jinja2 template and render it by passing through arguments
    """
    template = env.get_template(template_name)
    return template.render(**args)

def copy(location, to):
    """ Copy content from a location to another location
    """

    location = os.path.join(os.path.dirname(__file__), location)
    to = os.path.join(os.path.dirname(__file__), to)
    shutil.copytree(location, to, dirs_exist_ok=True)

def write(path, content):
    """ Write content to disk
    """

    path = os.path.join(os.path.dirname(__file__), path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build_site(output_dir):
    """ Build the site
    """

    content = load_data(CONTENT_PATH)
    build_registry = load_build_registry(BUILD_REGISTRY_PATH)
    asset_registry = load_asset_registry(ASSET_REGISTRY_PATH)

    for build_entry in build_registry:
        template = render(build_entry[BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION], **{k.capitalize(): v for k, v in content.items()})
        write(os.path.join(output_dir, build_entry[BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION]), template)

    for asset_entry in asset_registry:
        copy(asset_entry[ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION], os.path.join(output_dir, asset_entry[ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION]))
