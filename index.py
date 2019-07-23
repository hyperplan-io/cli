import keyring
import getpass

from hpcmd import HyperplanPrompt
from errors import InvalidCredentials
from api import Api

def start_cmd(root_api_url, login, password):
    try:
        api = Api(root_api_url, login, password)
        HyperplanPrompt(api).cmdloop()
    except InvalidCredentials:
        login, password = prompt_credentials()
        start_cmd(root_api_url, login, password)

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
    start_cmd(root_api_url, login, password)
else:
    try:
        login, password = prompt_credentials()
        start_cmd(root_api_url, login, password)
    except Exception as error:
        print(error)




