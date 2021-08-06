"""Simple wine shop."""

import argparse
import os
import pathlib
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Folder for excel files with information about wines
DATA_PATH = pathlib.Path('./data/')


def validate_file(input_file):
    """Check that file exists. Raise error if not."""
    file_path = DATA_PATH / input_file
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f'File {file_path} does not exist.')
    return input_file


def get_datafile_name():
    """Read filename from command line and return it, if exist."""
    parser = argparse.ArgumentParser(
        description=('Read file with information about wines '
                    'form command line and start the server.'),
    )
    parser.add_argument(
        dest='filename',
        nargs='?',
        type=validate_file,
        help='Excel file with information about wines.',
        metavar='FILE',
        default='wine2.xlsx',
    )
    return parser.parse_args().filename


datafile_path = DATA_PATH / get_datafile_name()
wines = pd.read_excel(datafile_path, keep_default_na=False).to_dict('records')

products = defaultdict(list)
for wine in wines:
    products[wine['Категория']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
)

template = env.get_template('template.html')
rendered_page = template.render(products=products)

with open('index.html', 'w', encoding='utf8') as index_file:
    index_file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
