import json
import os

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler


@chariot.command('search')
@cli_handler
@click.option('-term', '--term', help="Enter a search term", required=True)
@click.option('-count', '--count', is_flag=True, help="Return statistics on search")
@click.option('-details', '--details', is_flag=True, help="Return detailed search results")
def search(controller, term="", count=False, details=False):
    """ Query the Chariot data store for arbitrary matches """
    if count:
        print(controller.count(dict(key=term)))
    else:
        resp = controller.my(dict(key=term))
        for key, value in resp.items():
            if isinstance(value, list):
                for hit in value:
                    print(json.dumps(hit, indent=4) if details else hit['key'])


@chariot.command('test')
@cli_handler
@click.option('-suite', '--suite', type=click.Choice(["coherence"]), help="Run a specific test suite")
@click.argument('key', required=False)
def trigger_all_tests(controller, key, suite):
    """ Run integration test suite """
    try:
        import pytest
    except ModuleNotFoundError:
        print("Install pytest using 'pip install pytest' to run this command")
    test_directory = os.path.relpath("praetorian_cli/sdk/test", os.getcwd())
    os.environ['CHARIOT_PROFILE'] = controller.keychain.profile
    command = [test_directory]
    if key:
        command.extend(['-k', key])
    if suite:
        command.extend(['-m', suite])
    pytest.main(command)
