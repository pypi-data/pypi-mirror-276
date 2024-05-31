import os
from base64 import b64encode
from random import randint

import requests

from praetorian_cli.sdk.keychain import verify_credentials, Keychain


class Chariot:

    def __init__(self, keychain: Keychain):
        self.keychain = keychain

    @verify_credentials
    def my(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def count(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my/count", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def add(self, type, payload: dict) -> {}:
        resp = requests.post(f"{self.keychain.api}/{type}", json=payload, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def delete(self, type, key: str, account="") -> {}:
        resp = requests.delete(f"{self.keychain.api}/{type}/{account}", json={'key': key},
                               headers=self.keychain.headers)
        if not resp.ok:
            print(resp.url)
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def update(self, resource: str, data: dict) -> {}:
        resp = requests.put(f"{self.keychain.api}/{resource}", json=data, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def report(self, name: str) -> {}:
        resp = requests.get(f"{self.keychain.api}/report/risk", {'name': name}, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.text

    @verify_credentials
    def link_account(self, username: str, config: dict):
        resp = requests.post(f"{self.keychain.api}/account/{username}", json={'config': config},
                             headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def unlink_account(self, username: str):
        resp = requests.delete(f"{self.keychain.api}/account/{username}", headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def upload(self, name: str, upload_path: str = ""):
        with open(name, 'rb') as file:
            path = name
            if upload_path != "":
                path = upload_path

            resp = requests.put(f"{self.keychain.api}/file", params={"name": path}, data=file, allow_redirects=True,
                                headers=self.keychain.headers)
            if not resp.ok:
                raise Exception(f'[{resp.status_code}] Request failed')

    @verify_credentials
    def download(self, name: str, download_path: str) -> bool:
        resp = requests.get(f"{self.keychain.api}/file", params={"name": name}, allow_redirects=True,
                            headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')

        name = name.replace('/', '_')
        directory = os.path.expanduser(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, name), 'wb') as file:
            file.write(resp.content)

    def add_webhook(self):
        pin = str(randint(10000, 99999))
        self.link_account(username="hook", config={'pin': pin})
        username = b64encode(self.keychain.username.encode('utf8'))
        encoded_string = username.decode('utf8')
        encoded_username = encoded_string.rstrip('=')
        return f'{self.keychain.api}/hook/{encoded_username}/{pin}'
