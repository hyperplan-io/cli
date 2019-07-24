import keyring
import getpass

from hpcmd import HyperplanPrompt
from errors import InvalidCredentials
from api import Api

def get_api(root_api_url, login, password):
    return Api(root_api_url, login, password)

def create_api_and_start_cmd(root_api_url, login, password):
    api = get_api(root_api_url, login, password)
    start_cmd(api)
    
def start_cmd(api):
    try:
        HyperplanPrompt(api).cmdloop()
    except InvalidCredentials:
        login, password = prompt_credentials()
        create_api_and_start_cmd(root_api_url, login, password)

def get_password():
    service = "hyperplan-cli"
    username = keyring.get_credential(service, "username")
    password = keyring.get_password(service, "password")
    return (username, password)

def prompt_credentials():
    login= input("Login: ")
    password = getpass.getpass()
    return (login, password)

root_api_url = 'http://localhost:8090'
login, password = get_password()
if login != None and password != None:
    create_api_and_start_cmd(root_api_url, login, password)
else:
    try:
        login, password = prompt_credentials()
        api = get_api(root_api_url, login, password)
        api.authenticate()
        start_cmd(api)
    except InvalidCredentials:
        print('Invalid credentials')
    except Exception as error:
        print(error)




