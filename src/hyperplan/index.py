#!/usr/bin/env python

import keyring
import getpass
import os
import requests
from http.client import RemoteDisconnected

from hyperplan.hpcmd import HyperplanPrompt
from hyperplan.errors import InvalidCredentials
from hyperplan.api import Api

default_service = "hyperplan-cli"

def get_health(root_api_url):
    try:
        response = requests.get(
            '{}/_health'.format(root_api_url)
        )
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def get_api(service, root_api_url, login, password):
    return Api(service, root_api_url, login, password)

def create_api_and_start_cmd(service, root_api_url, login, password):
    api = get_api(service, root_api_url, login, password)
    start_cmd(api)
    
def start_cmd(api):
    try:
        HyperplanPrompt(api).cmdloop()
    except InvalidCredentials:
        login, password = prompt_credentials()
        create_api_and_start_cmd(api.service, api.root_api_url, login, password)
    except KeyboardInterrupt:
        pass

def get_password(service):
    username = keyring.get_password(service, "username")
    password = keyring.get_password(service, "password")
    return (username, password)

def get_root_api_url(service):
    root_api_url = keyring.get_password(service, "api_url")
    should_persist = False
    if root_api_url == None:
        root_api_url = input('api url: ')
        should_persist = True
    health = get_health(root_api_url)
    if health and should_persist:
        set_root_api_url(service, root_api_url)
    return (health, root_api_url)
        

def set_root_api_url(service, root_api_url):
    keyring.set_password(service, 'api_url', root_api_url)


def prompt_credentials():
    login= input("Login: ")
    password = getpass.getpass()
    return (login, password)

def main():
    (health, root_api_url) = get_root_api_url(default_service)
    if health == False:
        print('Server is not reachable, is it running on "{}" ?'.format(root_api_url))
        raise Exception('')
    else:
        login, password = get_password(default_service)
        if login != None and password != None:
            create_api_and_start_cmd(default_service, root_api_url, login, password)
        else:
            try:
                login, password = prompt_credentials()
                api = get_api(default_service, root_api_url, login, password)
                api.authenticate(save_credentials=True, log_error=False)
                start_cmd(api)
            except InvalidCredentials:
                print('Invalid credentials')
            except Exception as error:
                print(error)

try:
    main()
except Exception:
    try:
        sys.exit(0)
    except:
        os._exit(0)


