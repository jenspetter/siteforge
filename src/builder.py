import json
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BUILD_REGISTRY_PATH = "../data/build_registry.json"
BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION = "template"
BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION = "output"

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

def load_build_registry(path):
    """
    Loading build registry data\n
    Build registry data being data that defines what to build and how to build it\n
    We both load and validate the data. The data requiring to be a .json file
    
    :param path: Path to the build registry file.
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
    
    data = json.load(open(path, encoding="utf-8"))

    expected_keys = {BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION, BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION}
    for entry in data:
        if not BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION in entry:
            print('Missing required entry: ', BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION)
            print("Value: ", entry)
            return {}

        if not BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION in entry:
            print('Missing required entry: ', BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION)
            print("Value: ", entry)
            return {}

        unexpected = set(entry) - expected_keys
        if(unexpected):
            print("Failed to load build registry at path '" + path + "' as (an) unexpected key(s) were found")
            print("Expected key(s): ", expected_keys)
            print("Unexpected key(s): ", unexpected)
            print("Value: ", entry)
            return {}

    return data

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

    for build_entry in build_registry:
        template = render(build_entry[BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION], **{k.capitalize(): v for k, v in content.items()})
        write(os.path.join(output_dir, build_entry[BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION]), template)

    copy("../assets", os.path.join(output_dir, "assets"))
    copy("../css", os.path.join(output_dir, "css"))
