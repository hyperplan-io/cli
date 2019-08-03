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
    problem_type = input("problem_type(classification or regression): ") 
    if problem_type != "classification" and problem_type != "regression":
        print("problem type should be classification or regression")
        return get_problem_type()
    else:
        return problem_type

def list_projects(api):
    try:
        projects = api.list_projects(log=False)
        table = PrettyTable(['id', 'name', 'type', 'features', 'labels', 'algorithms'])
        for project in projects:
            project_id = project['id']
            project_name = project['name']
            project_problem = project['problem']
            project_features = project['configuration']['features']['id']
            project_labels = project['configuration']['labels']['id']
            project_algorithms = len(project['algorithms'])
            table.add_row([project_id, project_name, project_problem, project_features, project_labels, project_algorithms])
        print(table)

    except Exception as err:
        print(err)

def create_project(api):
    try:
        features = api.list_features(log=False)
        labels = api.list_labels(log=False)
        project_id = get_project_id()
        project_name = get_project_name()
        problem_type = get_problem_type()
        feature_id = qcm_features(features)
        label_id = qcm_labels(labels)
        api.create_project(Project(project_id,project_name, problem_type, feature_id, label_id))
        print("Ready to start predicting !")


    except Exception as err:
        print(err)
        pass
