import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

""" Containing functionality to build the website
    """

env = Environment(loader=FileSystemLoader("templates"))

def load_data():
    """ Load json data
    """

    info = json.load(open("data/info.json", encoding="utf-8"))
    projects = json.load(open("data/projects.json", encoding="utf-8"))
    return projects, info

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
    print(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build_site(output_dir):
    """ Build the site
    """

    (projects, info) = load_data()
    index_html = render("home.html", Info=info, Banner=info["Banner"], Projects=projects)

    copy("../assets", os.path.join(output_dir, "assets"))
    copy("../css", os.path.join(output_dir, "css"))
    write(os.path.join(output_dir, "index.html"), index_html)
