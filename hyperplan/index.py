#!/usr/bin/env python

import keyring
import getpass
import os
import requests
from http.client import RemoteDisconnected
import sys, getopt
import logging

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

def create_api_and_start_cmd(service, logger, root_api_url, login, password):
    api = get_api(service, root_api_url, login, password)
    start_cmd(api, logger)
    
def start_cmd(api, logger):
    try:
        HyperplanPrompt(api, logger).cmdloop()
    except InvalidCredentials:
        login, password = prompt_credentials()
        create_api_and_start_cmd(api.service, logger, api.root_api_url, login, password)
    except KeyboardInterrupt:
        pass

def get_password(service):
    username = keyring.get_password(service, "username")
    password = keyring.get_password(service, "password")
    return (username, password)

def get_root_api_url(service):
    try:
        config_file_path =  os.path.expanduser('~/.hyperplan')
        config_file = open(config_file_path, 'r+')
        root_api_url = config_file.readline()
        should_persist = False
        if root_api_url == "":
            root_api_url = input('api url: ')
            should_persist = True
        health = get_health(root_api_url)
        if health and should_persist:
            config_file.write(root_api_url)
        config_file.flush()
        config_file.close()
        return (health, root_api_url)
    except Exception as err:
        print(err)

def prompt_credentials():
    login= input("Login: ")
    password = getpass.getpass()
    return (login, password)


def help():
    print('hyperplan -loglevel <loglevel>')
def main():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hl:",["loglevel=", "help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    log_level = logging.INFO
    for opt, arg in opts:
        if opt in('-h', '--help'):
            help()
            sys.exit()
        elif opt in ("-l", "--loglevel"):
            if arg.lower() == 'debug':
                log_level = logging.DEBUG
                print('Using log level debug')
            elif arg.lower() == 'info':
                log_level = logging.INFO
                print('Using log level info')
            elif arg.lower() == 'warn':
                log_level = logging.WARN
                print('Using log level warn')
            elif arg.lower() == 'error':
                log_level = logging.ERROR
                print('Using log level error')

    logger = logging.getLogger()
    logger.setLevel(level=log_level)
    logging.basicConfig(level=log_level)
    (health, root_api_url) = get_root_api_url(default_service)
    if health == False:
        print('Server is not reachable, is it running on "{}" ?'.format(root_api_url))
    else:
        login, password = get_password(default_service)
        if login != None and password != None:
            create_api_and_start_cmd(default_service, logger, root_api_url, login, password)
        else:
            try:
                login, password = prompt_credentials()
                api = get_api(default_service, root_api_url, login, password)
                api.authenticate(logger, save_credentials=True, log_error=False)
                start_cmd(api, logger)
            except InvalidCredentials:
                print('Invalid credentials')
            except Exception as error:
                print(error)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print('Unhandled error: {}'.format(err))
        try:
            sys.exit(0)
        except:
            os._exit(0)
