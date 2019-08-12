from prettytable import PrettyTable

class Project():

    def __init__(self, project_id, project_name, problem_type, feature_id, label_id):
        self.project_id = project_id
        self.project_name = project_name
        self.problem_type = problem_type
        self.feature_id = feature_id 
        self.label_id = label_id 

    def to_json(self):
        return {'id': self.project_id, 'name': self.project_name, "problem": self.problem_type, "featuresId": self.feature_id, "labelsId": self.label_id}

def get_project_id():
    project_id = input("id(alphanumeric): ")
    if not project_id.isalnum():
        print("project id should be alphanumeric") 
        return get_project_id()
    return project_id

def get_project_name():
    return input("name: ")

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

def describe_project(api, project_id):
    try:
        project = api.get_project(project_id, log=False)
        table = PrettyTable(['id', 'name', 'type', 'features', 'labels', 'algorithms'])
        project_id = project['id']
        project_name = project['name']
        project_problem = project['problem']
        project_features = project['configuration']['features']['id']
        project_labels = None
        if project_problem == 'classification':
            project_labels = project['configuration']['labels']['id']
        project_algorithms = len(project['algorithms'])
        table.add_row([project_id, project_name, project_problem, project_features, project_labels, project_algorithms])
        print(table)
        return project
    except Exception as err:
        print(err)
        pass
def list_projects(api):
    try:
        projects = api.list_projects(log=False)
        table = PrettyTable(['id', 'name', 'type', 'features', 'labels', 'algorithms'])
        for project in projects:
            project_id = project['id']
            project_name = project['name']
            project_problem = project['problem']
            project_features = project['configuration']['features']['id']
            project_labels = None
            if project_problem == 'classification':
                project_labels = project['configuration']['labels']['id']
            project_algorithms = len(project['algorithms'])
            table.add_row([project_id, project_name, project_problem, project_features, project_labels, project_algorithms])
        print(table)
        return projects

    except Exception as err:
        print(err)
        pass

def list_algorithms(project):
    try:
        print(project['algorithms'])
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
        print(err)
        return None


def create_project(api, project_id, project_name=None, problem_type=None, feature_id=None, label_id=None):
    try:
        features = api.list_features(log=False)
        if features == None:
            return None
        labels = api.list_labels(log=False)
        if labels == None:
            return None
        if project_name == None:
            project_name = get_project_name()
        if problem_type == None:
            problem_type = get_problem_type()
        if feature_id == None:
            feature_id = qcm_features(features)
        if label_id == None:
            label_id = qcm_labels(labels)
        api.create_project(Project(project_id,project_name, problem_type, feature_id, label_id))
        print("Ready to start predicting !")
    except Exception as err:
        print(err)
        return None
def update_project(api, project_id):
    project = api.get_project(project_id, log=False)
    if project is not None:
        print('1. Set default algorithm')
        print('2. Set AB testing')
        choice = input('choice: ')
        if choice == '1':
            list_algorithms(project)
            algorithm_id = input('id of the default algorithm: ')
        elif choice == '2':
            for algorithm in project['algorithms']:
                weight = input('algorithm {}, weight: '.format(algorithm['id']))
        else:
            print('choice should be either 1 or 2')
            return update_project(api, project_id)
    else:
        print('Project {} does not exist'.format(project_id))
        return False
