import json

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler, list_options


@chariot.group()
@cli_handler
def list(ctx):
    """Get a list of resources from Chariot"""
    pass


list_translate = {'seeds': 'seed', 'assets': 'asset', 'risks': 'risk', 'references': 'ref', 'attributes': 'attribute',
                  'jobs': 'job', 'threats': 'threat', 'files': 'file'}
list_filter = {'seeds': 'seed', 'assets': 'seed', 'risks': 'seed', 'references': 'seed', 'attributes': 'seed',
               'jobs': 'updated', 'threats': 'source', 'files': 'name'}


@list.command('accounts', help="List accounts")
@list_options('name')
def accounts(controller, filter, offset, details):
    result = my_result(controller, '#account#', 'accounts', filter, offset)
    display_list(result, details)


@list.command('integrations', help="List integrations")
@list_options('name')
def integrations(controller, filter, offset, details):
    result = my_result(controller, '#account#', 'accounts', filter, offset)
    result['data'] = [item for item in result['data'] if '@' not in item['key'].split("#")[-2]]
    display_list(result, details)


@list.command('definitions', help="List definitions")
@list_options('name')
def definitions(controller, filter, offset, details):
    result = my_result(controller, f'#file#definitions/{filter}', 'files', "", offset)
    if not details:
        for hit in result.get('data', []):
            hit['key'] = hit['key'].split("definitions/")[-1]
    display_list(result, details)


def create_list_command(item_type, item_filter):
    @list.command(item_type, help=f"List {item_type}")
    @list_options(item_filter)
    def command(controller, filter, offset, details):
        result = my_result(controller, f'#{list_translate[item_type]}#{filter}', item_type, "", offset)
        display_list(result, details)


def display_list(result, details):
    if details:
        print(json.dumps(result, indent=4))
    else:
        for hit in result.get('data', []):
            print(f"{hit['key']}")
        if 'offset' in result:
            print(f"Next offset: {result['offset']}")


def my_result(controller, key, item_type, filter, offset):
    resp = controller.my(dict(key=key, offset=offset))
    result = {'data': resp.get(item_type, [])}
    if filter != "":  # filter by name or member only for accounts
        result['data'] = [item for item in resp['accounts'] if filter == item['name'] or filter == item['member']]
    if resp.get('offset'):
        result['offset'] = resp['offset']
    return result


for key, value in list_translate.items():
    create_list_command(key, list_filter[key])
