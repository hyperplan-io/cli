import requests
from errors import InvalidCredentials
from http.client import RemoteDisconnected
from requests.exceptions import ConnectionError

class Api():

    def __init__(self, root_api_url, login, password):
        self.root_api_url = root_api_url
        self.login = login
        self.password = password
        self.token = None

    def get_token_if_needed(self):
        if self.token == None:
            self.authenticate(log_error=False)

    def handle_status_code(self, status_code): 
        if status_code == 401:
            self.token = None
        elif status_code >= 500:
            self.remote_disconnected()
    def remote_disconnected(self):
        print('Server is not reachable, is it running on {}'.format(self.root_api_url))
    
    def authenticate(self, log_error=True):
        try:
            response = requests.post(
                '{}/authentication'.format(self.root_api_url),
                json = { 
                    "username": self.login,
                    "password": self.password
                }
            )
            if response.status_code == 200:
                self.token = response.json()['token']
            elif response.status_code == 401:
                raise InvalidCredentials()
        except (RemoteDisconnected, ConnectionError):
            if log_error:
                self.remote_disconnected()

    def list_features(self):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/features'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                features = response.json()
                for feature in features:
                    print(feature['id'])
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_labels(self):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/labels'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                labels = response.json()
                for label in labels:
                    print(label['id'])
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_projects(self):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/projects'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                projects = response.json()
                for project in projects:
                    print(project['id'])
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
                
    def list_algorithms(self):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/algorithms'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                algorithms = response.json()
                for algorithm in algorithms:
                    print(algorithm['id'])
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
