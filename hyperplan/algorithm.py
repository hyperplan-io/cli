from hyperplan.project import list_projects

class TensorFlowFeaturesTransformer():
    def __init__(self, signature_name, fields):
        self.signature_name = signature_name
        self.fields = fields
    def to_json(self):
        return { 'signatureName': self.signature_name, 'mapping': self.fields}

class TensorFlowLabelsTransformer():
    def __init__(self, fields):
        self.fields = fields 
    def to_json(self):
        return {'fields': self.fields}


class RasaNluFeaturesTransformer():
    def __init__(self, field, join_character):
        self.field = field
        self.join_character = join_character
    def to_json(self):
        return {'field': self.field, 'joinCharacter': self.join_character}

class SecurityConfig():
    def __init__(self, encryption, kv):
        self.encryption = encryption
        self.headers = kv
    def to_json(self):
        return { 'encryption': self.encryption, 'headers': self.headers }
class Backend():
    pass

class BasicHttpClassificationBackend(Backend):
    def __init__(self, root_path, ):
        self.root_path = root_path 
    def to_json(self):
        return {'class': 'BasicHttpClassification', 'rootPath': self.root_path}


class TensorFlowClassificationBackend(Backend):
    def __init__(self, root_path, model_name, model_version, features_transformer, labels_transformer):
        self.root_path = root_path 
        self.model_name = model_name
        self.model_version = model_version
        self.features_transformer = features_transformer
        self.labels_transformer = labels_transformer
    def to_json(self):
        return {'class': 'TensorFlowClassificationBackend', 'rootPath': self.root_path, 'model': self.model_name, 'modelVersion': self.model_version, 'featuresTransformer': self.features_transformer.to_json(), 'labelsTransformer': self.labels_transformer.to_json()}

class TensorFlowRegressionBackend(Backend):
    def __init__(self, root_path, model_name, model_version, features_transformer):
        self.root_path = root_path 
        self.model_name = model_name
        self.model_version = model_version
        self.features_transformer = features_transformer
    def to_json(self):
        return {'class': 'TensorFlowClassificationBackend', 'rootPath': self.root_path, 'model': self.model_name, 'modelVersion': self.model_version, 'featuresTransformer': self.features_transformer.to_json()}

class RasaNluClassificationBackend(Backend):
    def __init__(self, root_path, features_transformer):
        self.root_path = root_path
        self.features_transformer = features_transformer
    def to_json(self):
        return {'class': 'TensorFlowClassificationBackend', 'rootPath': self.root_path, 'featuresTransformer': self.features_transformer.to_json(), 'labelsTransformer': {}}

class Algorithm():
    def __init__(self, backend, security):
        self.backend = backend
        self.security = security

    def to_json(self):
        return {"backend": self.backend.to_json(), "security": self.security.to_json()}

def get_project_id(projects):
    project_id = input("project: ")
    if project_id not in projects:
        print("project does not exist") 
        return get_project_id(projects)
    return project_id

def get_tensorflow_features_transformer(fields):
    signature_name = input('signature name ')
    print('1. identity')
    print('2. custom')
    choice = input('feature transformer: ')
    if choice == '1':
        fields_mapping = {}
        for f1, f2 in zip(fields, fields):
            fields_mapping.update({ f1: f2 })
        return TensorFlowFeaturesTransformer(signature_name, fields_mapping)
    elif choice == '2':
        fields_mapping = {}
        for field in fields:
            mapped_field = input('{}: '.format(field))
            fields_mapping.update({ field: mapped_field})
        return TensorFlowFeaturesTransformer(signature_name, fields_mapping)
    else:
        print('Expected choice 1 or 2')
        return get_tensorflow_features_transformer(fields)

def get_tensorflow_labels_transformer(fields):
    print('1. identity')
    print('2. custom')
    choice = input('label transformer: ')
    if choice == '1':
        fields_mapping = {}
        for field in fields:
            fields_mapping.update({ field: field })
        return TensorFlowLabelsTransformer(fields_mapping)
    elif choice == '2':
        fields_mapping = {}
        for field in fields:
            mapped_field = input('{}: '.format(field))
            fields_mapping.update({ field: mapped_field})
        return TensorFlowLabelsTransformer(fields_mapping)
    else:
        print('Expected choice 1 or 2')
        return get_tensorflow_labels_transformer(fields)

def get_tensorflow_classification_backend(project):
    root_path = input('root path: ')
    model_name = input('model name: ')
    model_version = input('model version: ')
    features = [feature['name'] for feature in project['configuration']['features']['data']]
    features_transformer = get_tensorflow_features_transformer(features)
    labels_transformer = TensorFlowLabelsTransformer({}) 
    if project['configuration']['labels']['data']['type'] == 'oneOf':
        labels = [label for label in project['configuration']['labels']['data']['oneOf']]
        labels_transformer = get_tensorflow_labels_transformer(labels)
    return TensorFlowClassificationBackend(root_path, model_name, model_version, features_transformer, labels_transformer) 

def get_tensorflow_regression_backend(project):
    root_path = input('root path: ')
    model_name = input('model name: ')
    model_version = input('model version: ')
    features = [feature['name'] for feature in project['configuration']['features']['data']]
    features_transformer = get_tensorflow_features_transformer(features)
    return TensorFlowRegressionBackend(root_path, model_name, model_version, features_transformer) 

def get_rasa_nlu_classification_backend(project):
    pass

def get_basic_http_classification_backend(project):
    root_path = input('root path: ')
    return BasicHttpClassificationBackend(root_path)

def get_classification_backend(project):
    print('1. TensorFlow Serving')
    print('2. Rasa Nlu')
    print('3. Hyperplan Basic Http')
    choice = input('Backend: ')
    if choice == '1':
        return get_tensorflow_classification_backend(project)
    elif choice == '2':
        return get_rasa_nlu_classification_backend(project)
    elif choice == '3':
        return get_basic_http_classification_backend(project)
    else:
        print('Unexpected choice {}'.format(choice))
        return get_classification_backend(project)
def get_regression_backend(project):
    print('1. TensorFlow Serving')
    choice = input('Backend: ')
    if choice == '1':
        return get_tensorflow_regression_backend(project)
    else:
        print('Unexpected choice {}'.format(choice))
        return get_regression_backend(project)

def get_security_config():
    print('If you want to add HTTP headers, use the following format')
    print('HEADER_NAME_1:HEADER_VALUE_1,HEADER_NAME_2:HEADER_VALUE_2')
    headers = input('headers: ')
    splitted_headers = headers.split(',')
    if len(splitted_headers) > 1:
        headers = []
        for s in splitted_headers:
            header_split = s.split(':')
            if len(header_split) != 2:
                break
            header_key = header_split[0]
            header_value = header_split[1]
            headers.append({ 'key': header_key, 'value': header_value})
        if len(headers) == 0:
            print('Unexpected format, please retry')
            return get_security_config()
        else:
            return SecurityConfig('plain', headers)
    else:
        return SecurityConfig('plain', [])

def create_algorithm(api, logger, algorithm_id):
    try:
        projects = list_projects(api, logger)
        project_ids = [p['id'] for p in projects]
        project_id = get_project_id(project_ids)
        project = api.get_project(logger, project_id, log=False)
        problem_type = project['problem']
        backend = None
        if problem_type == 'classification':
            backend = get_classification_backend(project)
        elif problem_type == 'regression':
            backend  = get_regression_backend(project)
        else:
            print('Unexpected project type: {}'.format(problem_type))
            return None
        security_config = get_security_config()
        algorithm = Algorithm(backend, security_config) 
        api.create_algorithm(logger, project_id, algorithm_id, algorithm)
        return algorithm
    except Exception as err:
        logger.warn('an unhandled error occurred in create_algorithm: {}'.format(err))
