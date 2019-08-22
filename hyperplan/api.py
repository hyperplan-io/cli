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

    def get_token_if_needed(self, logger):
        if self.token == None:
            self.authenticate(logger, save_credentials=False, log_error=False)

    def handle_status_code(self, logger, status_code): 
        if status_code == 401:
            self.token = None
            self.get_token_if_needed(logger)
        elif status_code >= 500:
            self.remote_disconnected()
    def remote_disconnected(self):
        print('Server is not reachable, is it running on {}'.format(self.root_api_url))
    
    def authenticate(self, logger, save_credentials=False, log_error=True):
        try:
            response = requests.post(
                '{}/authentication'.format(self.root_api_url),
                json = { 
                    "username": self.login,
                    "password": self.password
                }
            )
            if response.status_code == 200:
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

    def list_features(self, logger, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/features'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                features = response.json()
                if log:
                    for feature in features:
                        print(feature['id'])
                return features
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_labels(self, logger, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/labels'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                labels = response.json()
                if log:
                    for label in labels:
                        print(label['id'])
                return labels
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def list_projects(self, logger, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/projects'.format(self.root_api_url),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                projects = response.json()
                if log:
                    for project in projects:
                        print(project['id'])
                return projects
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
                
    def create_feature(self, logger, feature):
        try:
            logger.debug(feature.to_json())
            self.get_token_if_needed(logger)
            response = requests.post(
                '{}/features'.format(self.root_api_url),
                json = feature.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                print('Successfully created feature')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_label(self, logger, label):
        try:
            logger.debug(label.to_json())
            self.get_token_if_needed(logger)
            response = requests.post(
                '{}/labels'.format(self.root_api_url),
                json = label.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                print('Successfully created label')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_algorithm(self, logger, project_id, algorithm_id, algorithm):
        try:
            self.get_token_if_needed(logger)
            response = requests.put(
                '{}/projects/{}/algorithms/{}'.format(self.root_api_url, project_id, algorithm_id),
                json = algorithm.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                print('Successfully created algorithm')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def create_project(self, logger, project):
        try:
            logger.debug(project.to_json())
            self.get_token_if_needed(logger)
            response = requests.post(
                '{}/projects'.format(self.root_api_url),
                json = project.to_json(),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                print('Successfully created project')
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            else:
                print('status is {}'.format(response.status_code))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def get_project(self, logger, project_id, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/projects/{}'.format(self.root_api_url, project_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                project = response.json()
                if log:
                    print(project)
                return project
            elif response.status_code == 404:
                print('Project {} does not exist'.format(project_id))
                return None
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()

    def get_features(self, logger, features_id, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/features/{}'.format(self.root_api_url, features_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                features = response.json()
                if log:
                    print(features)
                return features 
            elif response.status_code == 404:
                print('Feature {} does not exist'.format(features_id))
                return None
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def get_labels(self, logger, labels_id, log=True):
        try:
            self.get_token_if_needed(logger)
            response = requests.get(
                '{}/labels/{}'.format(self.root_api_url, labels_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                labels = response.json()
                if log:
                    print(labels)
                return labels 
            elif response.status_code == 404:
                print('Label {} does not exist'.format(labels_id))
                return None
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def predict(self, logger, project_id, features):
        try:
            self.get_token_if_needed(logger)
            response = requests.post(
                '{}/predictions'.format(self.root_api_url),
                json = {'projectId': project_id, 'features': features},
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def add_example(self, logger, prediction_id, label):
        try:
            self.get_token_if_needed(logger)
            response = requests.post(
                '{}/examples?predictionId={}&label={}&isCorrect=true'.format(self.root_api_url, prediction_id, label),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
    def delete_features(self, logger, features_id):
        try:
            self.get_token_if_needed(logger)
            response = requests.delete(
                '{}/features/{}'.format(self.root_api_url, features_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                print('Successfully deleted features {}'.format(features_id))
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
    def delete_labels(self, logger, labels_id):
        try:
            self.get_token_if_needed(logger)
            response = requests.delete(
                '{}/labels/{}'.format(self.root_api_url, labels_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                print('Successfully deleted labels {}'.format(labels_id))
                return True
            elif response.status_code == 404:
                print('Label {} does not exist'.format(labels_id))
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False
            
    def delete_algorithm(self, logger, project_id, algorithm_id):
        try:
            self.get_token_if_needed(logger)
            response = requests.delete(
                '{}/project/{}/algorithms/{}'.format(self.root_api_url, project_id, algorithm_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                print('Successfully deleted algorithm {}'.format(algorithm_id))
                return True
            elif response.status_code == 404:
                print('Algorithm {} does not exist in project {}'.format(algorithm_id, project_id))
                return False
            else:
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False

    def delete_project(self, logger, project_id):
        try:
            self.get_token_if_needed(logger)
            response = requests.delete(
                '{}/projects/{}'.format(self.root_api_url, project_id),
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                print('Successfully deleted project {}'.format(project_id))
                return True
            elif response.status_code == 404:
                print('Project {} does not exist'.format(project_id))
                return False
            else:
                return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False

    def update_project(self, logger, project_id, policy):
        try:
            self.get_token_if_needed(logger)
            response = requests.patch(
                '{}/projects/{}'.format(self.root_api_url, project_id),
                json = {'policy': policy.to_json()},
                headers = { 'Authorization': 'Bearer {}'.format(self.token)}
            )
            self.handle_status_code(logger, response.status_code)
            if response.status_code == 200:
                return True
            elif response.status_code == 400:
                for error in response.json():
                    print('{} : {}'.format(error['class'], error['message']))
            return False
        except (RemoteDisconnected, ConnectionError):
            self.remote_disconnected()
            return False
