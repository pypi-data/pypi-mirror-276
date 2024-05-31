import base64
import json

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler


@chariot.group()
@cli_handler
def get(ctx):
    """Get resource details from Chariot"""
    pass


@get.command('file')
@cli_handler
@click.argument('name')
@click.option('-path', '--path', default="", help="Download path. Default: save to current directory")
def download_file(controller, name, path):
    """ Download a file using key or name."""
    if name.startswith('#'):
        controller.download(name.split('#')[-1], path)
    else:
        controller.download(name, path)


@get.command('definition')
@cli_handler
@click.argument('name')
@click.option('-path', '--path', default="", help="Download path. Default: save to current directory")
def download_definition(controller, name, path):
    """ Download a definition using the risk name. """
    controller.download(f"definitions/{name}", path)


@get.command('report')
@cli_handler
@click.option('-name', '--name', help="Enter a risk name", required=True)
def report(controller, name):
    """ Generate definition for an existing risk """
    resp = controller.report(name=name)
    resp = base64.b64decode(resp).decode('utf-8')
    print(resp)


get_list = ['seeds', 'assets', 'risks', 'references', 'attributes', 'jobs', 'threats', 'accounts',
            'integrations']


def create_get_command(item):
    @get.command(item[:-1], help=f"Get {item[:-1]} details")
    @click.argument('key', required=True)
    @cli_handler
    def command(controller, key):
        resp = controller.my(dict(key=key))
        print(json.dumps(resp[item][0], indent=4))


for item in get_list:
    create_get_command(item)
