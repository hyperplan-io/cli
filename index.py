import keyring
import getpass
import os

from hpcmd import HyperplanPrompt
from errors import InvalidCredentials
from api import Api

default_service = "hyperplan-cli"

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

def get_password(service):
    username = keyring.get_password(service, "username")
    password = keyring.get_password(service, "password")
    return (username, password)

def prompt_credentials():
    login= input("Login: ")
    password = getpass.getpass()
    return (login, password)

def main():
    root_api_url = 'http://localhost:8090'
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
except KeyboardInterrupt:
    try:
        sys.exit(0)
    except:
        os._exit(0)

