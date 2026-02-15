# Siteforge
Ever found yourself duplicating web pages/html content as pages in your site are very similar? Such as a portfolio site where all projetc pages are Similar? Or another site? Meet siteforge.
Siteforge aims to tackle this by enabling to build up a site by using templating to generate the pages for your site, and use json as the content to your site.

# Installation
One can install siteforge via pip

```
$ pip install siteforge
```

# Example
An example on how to use Siteforge can be found on the source repo of Siteforge at https://github.com/jenspetter/siteforge

# Usage
An example usage of siteforge could be
```py
import argparse
from siteforge.builder import build_site

parser = argparse.ArgumentParser()
parser.add_argument('--content_path', type=str, required=True)
parser.add_argument('--build_registry_path', type=str, required=True)
parser.add_argument('--asset_registry_path', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    build_site(args.content_path, args.build_registry_path, args.asset_registry_path, args.output)
```

The above example shows a `build_site` call to Siteforge together with the arguments Siteforge expects, these are in the above example provided by argparse which isn't specific to Siteforge. **Siteforge wants all argument paths to be specified relative to the executing directory**

Let's go over the individual components that Siteforge expects.

## content path
This is the path to a folder containing json data to use within template building. Json data is referenced by key value pair where its key is the name of the json file that is imported and the value trickles down depending on the json data.

Imagine we have the following content-path folder that we import with the following Json files:
```
{
    "Name": "Ben",
    "Age": 29 
}
```
*personal.json*

```
{
    "Dog": {
        "Name": "Doef",
        "Breed": "Golden Retriever"
    } 
}
```
*pet.json*

With this, one can access the name of the dog in templating like `Pet.Dog.Name`. To get the age of Ben, one would reference `Personal.Age`. Notice how the first reference here (Pet and Personal) is capitalized. This is forced for each imported file.

**Only single hierarchy Json importing is supported at the moment. So when importing a folder one can expect sub folders that contain Json data to not be imported. This is on the agenda to support.

## build registry path
The build registry is what defines what pages are build with what template. This is also a Json file. An example could be
```
[
    {
        "template": "home.html",
        "output": "index.html"
    }
]
```

Notice how this is a container. We have 1 element that specifies that we would want to build the template `home.html` and output as `index.html`. Output supports paths, meaning one could also output to `folder/index.html` which would output to the `folder` folder within the requested output path (more on that later).

**It is expected that each entry has a `template` and `output` entry. Siteforge will error if failing to parse.**

## templates
A little detour to the arguments that the builder of Siteforge expects but I thought it would be a good idea to talk about templating now as it uses the above 2 concepts (content and build registry).

Siteforge uses [Jinja2](https://jinja.palletsprojects.com/en/stable/) for templating. The variables normally used in Jinja2 for templating are the Json values in the content files talked about above. The `template` entries in the build registry are individual Jinja2 templates. I hope one can see now that a site can easily be build up with these 2 concepts as one can add content Json data and add build registry items to tell Siteforge to build more pages, therefore building a site!

**The templates are expected to be in a `templates` folder within the executing directory. This is very hardcoded and expected to be changeable in the future via arguments as well.**

## asset registry path
The above is all nice and all but what if one needs to reference an image or something? This is where the asset registry comes in. The asset registry is in charge of telling Siteforge what directories need to be brought over to the output so created build registry items created with Jinja2 templating can actually reference the asset items. An example could be
```
[
    {
        "Source": "../../assets",
        "Destination": "assets"
    },
    {
        "Source": "../../css",
        "Destination": "css"
    }
]
```

Here we have 2 asset registry entries. Notice how the asset registry is a container. `Source` is the path to the folder that needs to be brought over, this folder path is relative to the path where the asset registry lives. `Destination` denotes where the folder in `Source` should be brought to relative to the requested output directory. 

**It is expected that each entry has a `Source` and `Destination` entry. Siteforge will error if failing to parse.**

## output
The output argument is where one would want the entire output of the site to go to. This is expected to be a path to a directory. 

# Advanced
Siteforge offers some considered to be advanced functionality.

## Bound context
Imagine the following. One has a nice site working but a content Json containing an array item where one wants to reference a specific item in this array for a template. This is where bounding contexts come in. 
```
[
    {
        "template": "project.html",
        "output": "project/project1.html",
        "boundContext": [
            {
                "Name": "Project",
                "Where": {
                    "Key": "Id",
                    "Value": "Project1"
                }
            }
        ]
    }
]
```

The above specifies a (part of) a build registry that contains an element with a bound context. What Siteforge gets told here is that we have template 'project.html' that outputs to 'project/project1.html' where we tell that the variable 'Project' is equal to an entry within all imported content Json files where its key-value pair is equal to 'Id', 'Project1'. Notice how 'boundContext' is a container. One can have as many bound contexts as they want.

So then, when a Json content contains
```
[
    {
        "Id": "Project1",
        "Title": "Project 1",
    },
    {
        "Id": "Project2",
        "Title": "Project 2",
    }
]
```

Siteforge will bind to the first entry for the bound context in the build registry example above. Note that this can of course be duplicated for the same Jinja2 template. Making the possibility if wanted to re-use templates.

# Todo
What follows is a todo list of things to support for Siteforge
- Support for importing Json files in content paths existing is sub-folders to the imported path.
- Allow for a path to be passed in for defining where Jinja2 templates come from.
- Proper Json spec validation is on the radar but not very high priority right now.