import json
from getch import getche

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import cli_handler, list_options


list_translate = {'seeds': 'seed', 'assets': 'asset', 'risks': 'risk', 'references': 'ref', 'attributes': 'attribute',
                  'jobs': 'job', 'threats': 'threat', 'files': 'file'}
list_filter = {'seeds': 'seed', 'assets': 'seed', 'risks': 'seed', 'references': 'seed', 'attributes': 'seed',
               'jobs': 'updated', 'threats': 'source', 'files': 'name'}


@chariot.group()
@cli_handler
def list(ctx):
    """Get a list of resources from Chariot"""
    pass


def identity(x):
    return x


def is_integration(item):
    name = item['key'].split('#')[3]
    return '@' not in name and name != 'settings'


def is_user_account(item):
    return '@' in item['key'].split('#')[3]


@list.command('accounts', help='List accounts')
@list_options('name')
def accounts(controller, filter, offset, details, page):
    def filter_accounts(result):
        if filter != '':
            result['data'] = [item for item in result['data'] if filter == item['name'] or filter == item['member']]
        result['data'] = [item for item in result['data'] if is_user_account(item)]
        return result

    paginate(controller, '#account#', 'accounts', offset, details, page, filter_accounts, identity)


@list.command('integrations', help='List integrations')
@list_options('name')
def integrations(controller, filter, offset, details, page):
    def filter_integrations(result):
        result['data'] = [item for item in result['data'] if is_integration(item)]
        return result

    paginate(controller, '#account#', 'accounts', offset, details, page, filter_integrations, identity)


@list.command('definitions', help='List definitions')
@list_options('name')
def definitions(controller, filter, offset, details, page):
    def extract_risk_name(key):
        return key.split('definitions/')[-1]

    paginate(controller, f'#file#definitions/{filter}', 'files', offset, details, page,
             identity, extract_risk_name)


def create_list_command(item_type, item_filter):
    @list.command(item_type, help=f'List {item_type}')
    @list_options(item_filter)
    def command(controller, filter, offset, details, page):
        paginate(controller,f'#{list_translate[item_type]}#{filter}', item_type, offset,
                 details, page, identity, identity)

def paginate(controller, search_key, item_type, offset, details, page, filter_data, modify_key):
    pages = 1
    while True:
        result = my_result(controller, search_key, item_type, offset, filter_data)
        next_offset = display_list(result, details, modify_key)

        if next_offset:
            if page == "no":
                break
            elif page == "interactive":
                print("There are more results. Press 'q' to stop; any other key for next page...", end='', flush=True)
                next_page = getche()
                print()
                if next_page.lower() == "q":
                    break
            else:
                if pages == 100:
                    break
                pages += 1

            offset = json.dumps(result['next_offset'])
        else:
            break

    if next_offset:
        print(f"Next offset: {json.dumps(next_offset)}")


def display_list(result, details, modify_key):
    if details:
        print(json.dumps(result, indent=4))
    else:
        for hit in result.get('data', []):
            print(modify_key(hit['key']))

    return result['next_offset'] if 'next_offset' in result else None


def my_result(controller, key, item_type, offset, filter_data):
    response = controller.my(dict(key=key, offset=offset))
    result = filter_data({'data': response.get(item_type, [])})
    #if response.get('offset'):
    if 'offset' in response:
        result['next_offset'] = response['offset']
    return result


for key, value in list_translate.items():
    create_list_command(key, list_filter[key])
