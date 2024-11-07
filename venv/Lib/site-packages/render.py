#!/bin/env python
import argparse
import json
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader


def error(msg, *args, **kwargs):
    """Print an error and exit."""
    sys.stderr.write(msg.format(*args, **kwargs) + "\n")
    sys.exit(1)


def get_vars(values):
    """Parse a list of vars and return them as a dictionary."""
    items = {}
    for value in (values or []):
        if '=' not in value:
            error("var '{}' is invalid", value)
        key, _, value = value.partition('=')
        items[key] = value
    return items


def get_file_context(paths, loader):
    """Parse a list files using the provided parser. Return their combined context as a
    dictionary."""
    context = {}
    for path in paths or ():
        try:
            with open(path) as fd:
                data = loader(fd)
            context.update(data)
        except IOError as e:
            error("file '{}' not readable: {}", e)
    return context


def get_yaml(paths):
    """Parse a list of YAML files and return their combined contents as a dictionary."""
    def loader(fd):
        data = yaml.load(fd)
        if not isinstance(data, dict):
            error("file '{}' does not contain a YAML object")
        return data

    return get_file_context(paths, loader)


def get_json(paths):
    """Parse a list of JSON files and return their combined contents as a dictionary."""
    def loader(fd):
        data = json.load(fd)
        if not isinstance(data, dict):
            error("file '{}' does not contain a JSON object")
        return data

    return get_file_context(paths, loader)


def get_envs(names):
    """Retrieve the named environment values and return them as a dictionary. Non-existent
    environment variables will contain an empty string for the value."""
    items = {}
    for name in (names or []):
        items[name] = os.getenv(name, "")
    return items


def get_context(options):
    """Return the template context from the provided options."""
    context = {}
    context.update(get_yaml(options.yaml))
    context.update(get_json(options.json))
    if options.allenv:
        context.update(os.environ)
    context.update(os.environ if options.allenv else get_envs(options.envs))
    context.update(get_vars(options.vars))
    return context


def render(out, tpl, context):
    """Render the template at ``tpl`` to the file-like object ``out`` using the provided
    context."""
    tpl = os.path.abspath(tpl)
    env = Environment(loader=FileSystemLoader(searchpath='/'))
    template = env.get_template(tpl)
    template.stream(context).dump(out)
    # Jinja strips the end-of-file newline. Let's add it back.
    out.write('\n')


def run():
    parser = argparse.ArgumentParser(
        description="Render a template file to stdout. All options may be given multiple times.")
    parser.add_argument('-v', '--var', metavar='name=value', dest='vars', action='append',
                        help="Add the provided value.")
    parser.add_argument('-e', '--env', metavar='name', dest='envs', action='append',
                        help="Add an environment variable.")
    parser.add_argument('-E', '--all-env', dest='allenv', action='store_true',
                        help="Add all environment variables.")
    parser.add_argument('-y', '--yaml', metavar='file', dest='yaml', action='append',
                        help="Add contents of a YAML file.")
    parser.add_argument('-j', '--json', metavar='file', dest='json', action='append',
                        help="Add contents of a JSON file.")
    parser.add_argument('template', action='store',
                        help="The template to render.")
    options = parser.parse_args()

    render(sys.stdout, options.template, get_context(options))


if __name__ == '__main__':
    run()
