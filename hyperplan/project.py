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