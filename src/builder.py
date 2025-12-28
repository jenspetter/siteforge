import json
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

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

    index_html = render("home.html", **{k.capitalize(): v for k, v in content.items()})

    copy("../assets", os.path.join(output_dir, "assets"))
    copy("../css", os.path.join(output_dir, "css"))
    write(os.path.join(output_dir, "index.html"), index_html)
