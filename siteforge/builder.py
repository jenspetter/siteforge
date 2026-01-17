import os
import shutil
from . import json_function_registration
from . import json_functions
from . import json_utils as JsonUtils
from jinja2 import Environment, FileSystemLoader

BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION = "template"
BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION = "output"
BUILD_REGISTRY_OPTIONAL_VAR_BOUNDCONTEXT_NOTATION = "boundContext"

ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION = "Source"
ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION = "Destination"

""" Containing functionality to build a website
    """

env = Environment(loader=FileSystemLoader("templates"))

def load_content(path):
    """
    Loading content from a path\n
    The content being the data used reference in templating
    
    :param path: The path to the content files. Expected to be a path to a directory
    """

    # Load content from json first
    content = JsonUtils.load_objects(path)

    # Ressolve tokens in json content
    # Tokens can be:
    # - A method reference
    def _process_content_value(value):
        if isinstance(value, dict) and "$func" in value:
            name = value["$func"]

            if name not in json_function_registration.JSON_FUNCTION_REFERENCES:
                print("Content value referenced a function but the function can not be found. Is it imported?")
                print("Continuing by defining as unknown")
                print("Value: ", value)
                return "UNKNOWN_FUNCTION_RESSOLVE"
            
            func = json_function_registration.JSON_FUNCTION_REFERENCES[name]

            args = [_process_content_value(v) for v in value.get("args", [])]
            kwargs = {k: _process_content_value(v) for k, v in value.get("kwargs", {}).items()}

            return func(*args, **kwargs)

        if isinstance(value, dict):
            return {k: _process_content_value(v) for k, v in value.items()}

        if isinstance(value, list):
            return [_process_content_value(v) for v in value]

        return value
    
    for k, v in content.items():
        content[k] = _process_content_value(v)

    return content

def load_build_registry(path):
    """
    Loading build registry data\n
    Build registry data being data that defines what to build and how to build it\n
    We both load and validate the data. The data requiring to be a .json file
    
    :param path: Path to the build registry file.
    """

    return JsonUtils.load_container(path, [BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION, BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION])

def load_asset_registry(path):
    """
    Loading asset registry data\n
    Asset registry data being data that defines what to copy over as asset data to the output directory of the build\n
    We both load and validate the data. The data requiring to be a .json file
    
    :param path: Path to the asset registry file.
    """

    return JsonUtils.load_container(path, [ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION, ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION])

def get_processed_content_from_build_item(build_item, content):
    """
    Get content based on build registry item notation\n
    A build registry item can denote a bound context which bounds to something in the loaded in content\n
    If so, then we try to bind to the context by searching for it in the contents
    
    :param build_item: The build item that can potentially contain a bound contexts
    :param content: The already loaded content
    """

    # Just return the content if there is no build item
    if build_item is None:
        return None
    
    processed_content = {}

    # Process bound context if existing
    if not BUILD_REGISTRY_OPTIONAL_VAR_BOUNDCONTEXT_NOTATION in build_item:
        return None

    # Try and ressolve all bound context items
    ressolved_once = False
    for bound_entry in build_item[BUILD_REGISTRY_OPTIONAL_VAR_BOUNDCONTEXT_NOTATION]:
        name = bound_entry['Name']
        # Only supporting 1 query right now
        query = bound_entry['Where']

        key = query['Key']
        value = query['Value']

        for k, v in content.items():
            filtered = JsonUtils.get_filtered_objects(v, JsonUtils.JsonFilter(key, value))
            if filtered is None:
                continue

            for item in filtered:
                # Entry already exists, this is an issue
                if name in content:
                    continue

                processed_content[name] = item
                ressolved_once = True
    
    if ressolved_once:
        return processed_content
    else:
        return None

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

def build_site(content_path, build_registry_path, asset_registry_path, output_dir):
    """ Build the site
    """

    # Load all data needed to build the site
    content = load_content(content_path)
    build_registry = load_build_registry(build_registry_path)
    asset_registry = load_asset_registry(asset_registry_path)

    # Build each registry entry
    for build_entry in build_registry:
        final_content = {}

        # Load in existing content
        for k, v in content.items():
            final_content[k] = v

        # Process build item
        processed_content = get_processed_content_from_build_item(build_entry, content)

        # Add processed content if existing
        if processed_content is not None:
            for k, v in processed_content.items():
                final_content[k] = v

        # Render and write
        template = render(build_entry[BUILD_REGISTRY_EXPECTED_VAR_TEMPLATE_NOTATION], **{k.capitalize(): v for k, v in final_content.items()})
        write(os.path.join(output_dir, build_entry[BUILD_REGISTRY_EXPECTED_VAR_OUTPUT_NOTATION]), template)
 
    # Copy over each asset entry
    for asset_entry in asset_registry:
        copy(asset_entry[ASSET_REGISTRY_EXPECTED_VAR_SOURCE_NOTATION], os.path.join(output_dir, asset_entry[ASSET_REGISTRY_EXPECTED_VAR_DESTINATION_NOTATION]))
