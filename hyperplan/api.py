import requests
import keyring
from hyperplan.errors import InvalidCredentials
from http.client import RemoteDisconnected
from requests.exceptions import ConnectionError

class Api():

    def __init__(self, service, root_api_url, login, password):
        self.service = service
        self.root_api_url = root_api_url
        self.login = login
        self.password = password
        self.token = None

    def persist_credentials(self):
        keyring.set_password(self.service, 'username', self.login)
        keyring.set_password(self.service, 'password', self.password)

    def get_token_if_needed(self):
        if self.token == None:
            self.authenticate(save_credentials=False, log_error=False)

    def handle_status_code(self, status_code): 
        if status_code == 401:
            self.token = None
            self.get_token_if_needed()
        elif status_code >= 500:
            self.remote_disconnected()
    def remote_disconnected(self):
        print('Server is not reachable, is it running on {}'.format(self.root_api_url))
    
    def authenticate(self, save_credentials=False, log_error=True):
        try:
            response = requests.post(
                '{}/authentication'.format(self.root_api_url),
                json = { 
                    "username": self.login,
                    "password": self.password
                }
            )
            if response.status_code == 200:
                print('success')
                if save_credentials:
                    self.persist_credentials()
                self.token = response.json()['token']
            elif response.status_code == 401:
                print('Authentication failed')
                raise InvalidCredentials()
        except (RemoteDisconnected, ConnectionError):
            if log_error:
                self.remote_disconnected()
        except Exception as err:
            print(err)

    def list_features(self, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/features'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                features = response.json()
                if log:
                    for feature in features:
                        print(feature['id'])
                return features
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_labels(self, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/labels'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                labels = response.json()
                if log:
                    for label in labels:
                        print(label['id'])
                return labels
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_projects(self, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/projects'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                projects = response.json()
                if log:
                    for project in projects:
                        print(project['id'])
                return projects
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
                
    def create_feature(self, feature):
        try:
            print(feature.to_json())
            self.get_token_if_needed()
            response = requests.post(
                '{}/features'.format(self.root_api_url),
                json = feature.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                print('success')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_label(self, label):
        try:
            print(label.to_json())
            self.get_token_if_needed()
            response = requests.post(
                '{}/labels'.format(self.root_api_url),
                json = label.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                print('success')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_algorithm(self, project_id, algorithm_id, algorithm):
        try:
            print(algorithm.to_json())
            self.get_token_if_needed()
            response = requests.post(
                '{}/projects/{}/algorithms/{}'.format(self.root_api_url, project_id, algorithm_id),
                json = algorithm.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                print('success')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_project(self, project):
        try:
            print(project.to_json())
            self.get_token_if_needed()
            response = requests.post(
                '{}/projects'.format(self.root_api_url),
                json = project.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                print('success')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def get_project(self, project_id, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/projects/{}'.format(self.root_api_url, project_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                project = response.json()
                if log:
                    print(project)
                return project
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def get_features(self, features_id, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/features/{}'.format(self.root_api_url, features_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                features = response.json()
                if log:
                    print(features)
                return features 
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def get_labels(self, labels_id, log=True):
        try:
            self.get_token_if_needed()
            response = requests.get(
                '{}/labels/{}'.format(self.root_api_url, labels_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                labels = response.json()
                if log:
                    print(labels)
                return labels 
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def predict(self, project_id, features):
        try:
            self.get_token_if_needed()
            response = requests.post(
                '{}/predictions'.format(self.root_api_url),
                json = {'projectId': project_id, 'features': features},
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def add_example(self, prediction_id, label):
        try:
            self.get_token_if_needed()
            response = requests.post(
                '{}/examples?predictionId={}&label={}&isCorrect=true'.format(self.root_api_url, prediction_id, label),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def delete_features(self, features_id):
        try:
            self.get_token_if_needed()
            response = requests.delete(
                '{}/features/{}'.format(self.root_api_url, features_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                print('Feature {} does not exist'.format(features_id))
                return False
            else:
                print('status is {}'.format(response.status_code))
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False
    def delete_labels(self, labels_id):
        try:
            self.get_token_if_needed()
            response = requests.delete(
                '{}/labels/{}'.format(self.root_api_url, labels_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                print('Label {} does not exist'.format(labels_id))
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False
    def delete_algorithm(self, project_id, algorithm_id):
        try:
            self.get_token_if_needed()
            response = requests.delete(
                '{}/project/{}/algorithms/{}'.format(self.root_api_url, project_id, algorithm_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(response.status_code)
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                print('Algorithm {} does not exist in project {}'.format(algorithm_id, project_id))
                return False
            else:
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False
