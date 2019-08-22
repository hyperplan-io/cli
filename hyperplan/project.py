from prettytable import PrettyTable
import logging

class DefaultAlgorithmPolicy():
    def __init__(self, default_algorithm_id):
        self.default_algorithm_id = default_algorithm_id
    def to_json(self):
        return { 'class': 'DefaultAlgorithm', 'algorithmId': self.default_algorithm_id }

class WeightedAlgorithmPolicy():
    def __init__(self, weights):
        self.weights = weights
    def to_json(self):
        weights = [{'algorithmId': w[0], 'weight': w[1] }for w in self.weights]
        return { 'class': 'WeightedAlgorithm', 'weights': weights}

class Project():

    def __init__(self, project_id, project_name, problem_type, feature_id, label_id, project_topic):
        self.project_id = project_id
        self.project_name = project_name
        self.problem_type = problem_type
        self.feature_id = feature_id 
        self.label_id = label_id 
        self.project_topic = project_topic

    def to_json(self):
        if self.project_topic == None:
            return {'id': self.project_id, 'name': self.project_name, "problem": self.problem_type, "featuresId": self.feature_id, "labelsId": self.label_id}
        else:
            return {'id': self.project_id, 'name': self.project_name, "problem": self.problem_type, "featuresId": self.feature_id, "labelsId": self.label_id, "topic": self.project_topic}


def get_project_id():
    project_id = input("id(alphanumeric): ")
    if not project_id.isalnum():
        print("project id should be alphanumeric") 
        return get_project_id()
    return project_id

def get_project_name():
    return input("name: ")

def get_project_topic():
    reply = input("publish data stream ? (y/n)")
    if reply.lower() == 'y':
        topic = input("topic: ") 
        if topic == '':
            print('topic cannot be empty')
            return get_project_topic()
        else:
            return topic
    elif reply.lower() == 'n':
        return None
    else:
        print('expected (y/n)')
        return get_project_topic()

def qcm_features(features):
    print("==== Features ====")
    for feature in features:
        print('{}'.format(feature['id']))
    print("==================")
    feature = input("feature: ")
    return feature

def qcm_labels(labels):
    print("==== Labels ====")
    for label in labels:
        print('{}'.format(label['id']))
    print("==================")
    label = input("label: ")
    return label

def get_problem_type():
    problem_type = input("problem category(classification or regression): ") 
    if problem_type != "classification" and problem_type != "regression":
        print("problem type should be classification or regression")
        return get_problem_type()
    else:
        return problem_type

def describe_project(api, logger, project_id):
    try:
        project = api.get_project(logger, project_id, log=False)
        if project is None:
            return None
        project_table = PrettyTable(['id', 'name', 'type', 'features', 'labels', 'algorithms', 'topic'])
        project_id = project['id']
        project_name = project['name']
        project_problem = project['problem']
        project_features = project['configuration']['features']['id']
        project_datastream = project['configuration']['dataStream']
        project_topic = ''
        if project_datastream != None:
            project_topic = project_datastream['topic']
        project_labels = None
        if project_problem == 'classification':
            project_labels = project['configuration']['labels']['id']
        project_algorithms = len(project['algorithms'])
        project_table.add_row([project_id, project_name, project_problem, project_features, project_labels, project_algorithms, project_topic])
        print(project_table)
        policy = project['policy']
        policy_class = policy['class']
        algorithms_table = PrettyTable(['id', 'weight'])
        if policy_class == 'DefaultAlgorithm':
            default_algorithm_id = policy['algorithmId']
            algorithms_table.add_row([default_algorithm_id, 1])
            print(algorithms_table)
        elif policy_class == 'WeightedAlgorithm':
            weights = policy['weights']
            for w in weights:
                algorithms_table.add_row([w['algorithmId'], w['weight']])
            print(algorithms_table)
        else:
            pass
        return project
    except Exception as err:
        logger.warn('an unhandled error occurred in describe_project: {}'.format(err))

def list_projects(api, logger):
    try:
        projects = api.list_projects(logger, log=False)
        table = PrettyTable(['id', 'name', 'type', 'features', 'labels', 'algorithms', 'topic'])
        if projects is None:
            return None
        for project in projects:
            project_id = project['id']
            project_name = project['name']
            project_problem = project['problem']
            project_features = project['configuration']['features']['id']
            project_datastream = project['configuration']['dataStream']
            project_topic = ''
            if project_datastream != None:
                project_topic = project_datastream['topic']
            project_labels = None
            if project_problem == 'classification':
                project_labels = project['configuration']['labels']['id']
            project_algorithms = len(project['algorithms'])
            table.add_row([project_id, project_name, project_problem, project_features, project_labels, project_algorithms, project_topic])
        print(table)
        return projects

    except Exception as err:
        logger.warn('an unhandled error occurred in list_projects: {}'.format(err))

def list_algorithms(project, logger):
    try:
        table = PrettyTable(['id', 'backend', 'headers'])
        algorithms = project['algorithms']
        for algorithm in algorithms:
            algorithm_id = algorithm['id']
            algorithm_backend = algorithm['backend']
            backend_class = algorithm_backend['class']
            algorithm_headers = algorithm['security']['headers']
            table.add_row([algorithm_id, backend_class, algorithm_headers])
        print(table)
        return algorithms
    except Exception as err:
        logger.warn('an unhandled error occurred in list_algorithms: {}'.format(err))


def create_project(api, logger, project_id, project_name=None, problem_type=None, feature_id=None, label_id=None, project_topic=None):
    try:
        features = api.list_features(logger, log=False)
        if features is None:
            return None
        if project_name is None:
            project_name = get_project_name()
        if problem_type is None:
            problem_type = get_problem_type()

        if feature_id is None:
            feature_id = qcm_features(features)

        if problem_type == 'classification':
            labels = api.list_labels(logger, log=False)
            if labels is None:
                return None
            if label_id is None:
                label_id = qcm_labels(labels)
        
        if project_topic is None:
            project_topic = get_project_topic()
        api.create_project(logger, Project(project_id,project_name, problem_type, feature_id, label_id, project_topic))
        print("Ready to start predicting !")
    except Exception as err:
        logger.warn('an unhandled error occurred in create_project: {}'.format(err))

def delete_project(api, logger, project_id):
    try:
        api.delete_project(logger, project_id)
    except Exception as err:
        logger.warn('an unhandled error occurred in delete_project: {}'.format(err))

def update_project(api, logger, project_id):
    project = api.get_project(logger, project_id, log=False)
    if project is None:
        return None
    print('1. Set default algorithm')
    print('2. Set AB testing')
    choice = input('choice: ')
    if choice == '1':
        list_algorithms(logger, project)
        algorithm_id = input('id of the default algorithm: ')
        policy = DefaultAlgorithmPolicy(algorithm_id)
        api.update_project(logger, project_id, policy)
    elif choice == '2':
        weights = []
        for algorithm in project['algorithms']:
            algorithm_id = algorithm['id']
            weight = input('algorithm {}, weight: '.format(algorithm_id))
            try:
                weights.append([algorithm_id, float(weight)])
            except ValueError:
                print('Not a number, skipping...')
        policy = WeightedAlgorithmPolicy(weights)
        try:
            return api.update_project(logger, project_id, policy)
        except Exception as err:
            logger.warn('an unhandled error occurred in update_project: {}'.format(err))
            return False 
    else:
        print('choice should be either 1 or 2')
        return update_project(api, logger, project_id)
