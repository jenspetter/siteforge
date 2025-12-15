import json
import os
from jinja2 import Environment, FileSystemLoader

""" Containing functionality to build the website
    """

env = Environment(loader=FileSystemLoader("templates"))

def load_data():
    """ Load json data
    """

    info = json.load(open("data/info.json"))
    projects = json.load(open("data/projects.json"))
    return projects, info

def render(template_name, **args):
    """ Get a jinja2 template and render it by passing through arguments
    """
    template = env.get_template(template_name)
    return template.render(**args)

def write(path, content):
    """ Write content to disk
    """

    path = os.path.join(os.path.dirname(__file__), path)
    print(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build_site():
    """ Build the site
    """

    (projects, info) = load_data()
    index_html = render("home.html", Info=info, Banner=info["Banner"], Projects=projects)
    write("../index.html", index_html)
