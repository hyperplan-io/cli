from hyperplan.api import Api
from hyperplan.features_descriptors import *
from hyperplan.labels_descriptors import *
from hyperplan.project import *
from hyperplan.predict import *

class TestWorkingApi:

    def setUp(self):
        self.api = Api("test_service", "http://localhost:8080", "admin", "admin")
        self.logger = logging.getLogger()
        self.logger.setLevel(level=logging.DEBUG)

    def teardown_module(self):
        self.api.delete_features('myFeature')
        self.api.delete_labels('myLabel')

    def test_01_list_features(self):
        features = list_features(self.api, self.logger)
        assert features is not None

    def test_02_list_labels(self):
        labels = list_labels(self.api, self.logger)
        assert labels is not None

    def test_03_list_projects(self):
        projects = list_labels(self.api, self.logger)
        assert projects is not None

    def test_04_create_features(self):
        features = [{'name': 'myFeature', 'type': 'string', 'dimension': 'scalar', 'description': 'My custom feature'}]
        create_features(self.api, self.logger, 'myFeature', features)
        feature_data = describe_feature(self.api, self.logger, 'myFeature')['data']
        assert feature_data == features

    def test_05_create_label(self):
        create_labels(self.api, self.logger, 'myLabel', label_type='oneOf', label_one_of=['test1','test2','test3'], label_description='My description')
        label_data = describe_label(self.api, self.logger, 'myLabel')
        assert label_data == { 'id': 'myLabel', 'data': {'type': 'oneOf', 'oneOf': ['test1', 'test2', 'test3'], 'description': 'My description'}}
    
    def test_06_create_project(self):
        create_project(self.api, self.logger, 'myProjectId', 'My project name', 'classification', 'myFeature', 'myLabel', 'myTopic')
        project = describe_project(self.api, self.logger, 'myProjectId')
        assert project == {'id': 'myProjectId', 'name': 'My project name', 'problem': 'classification', 'algorithms': [{'id': 'random', 'projectId': 'myProjectId', 'backend': {'class': 'LocalRandomClassification', 'labels': ['test1', 'test2', 'test3']}, 'security': {'encryption': 'plain', 'headers': []}}], 'policy': {'class': 'DefaultAlgorithm', 'algorithmId': 'random'}, 'configuration': {'features': {'id': 'myFeature', 'data': [{'name': 'myFeature', 'type': 'string', 'dimension': 'scalar', 'description': 'My custom feature'}]}, 'labels': {'id': 'myLabel', 'data': {'type': 'oneOf', 'oneOf': ['test1', 'test2', 'test3'], 'description': 'My description'}}, 'dataStream': {'topic': 'myTopic'}}}

    def test_07_predict(self):
        prediction = predict(self.api, self.logger, 'myProjectId', features = { 'myFeature': 'example string' }, annotate=False, log=False)
        assert prediction['type'] == 'classification'
        assert prediction['projectId'] == 'myProjectId'
        assert prediction['algorithmId'] == 'random'
        assert prediction['features'] == [{'key': 'myFeature', 'type': 'string', 'dimension': 'scalar', 'value': 'example string'}]
        assert prediction['examples'] == []
