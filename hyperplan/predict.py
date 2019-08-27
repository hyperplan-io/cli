from prettytable import PrettyTable

def validate_element(element_value, expected_type):
    if expected_type == 'string':
        return str(element_value)
    elif expected_type == 'float':
        return float(element_value)
    elif expected_type == 'int':
        return int(element_value)
    else:
        raise ValueError('Unknown type: {}'.format(expected_type))

def parse_array(arr, element_type):
    array_content = arr[1:len(arr)-1]
    elements = array_content.split(',')
    return [validate_element(e, element_type) for e in elements]

def get_feature_value(feature_name, feature_type, feature_dimension, feature_description):
    
    feature_value = input('Enter a {} {} value for "{}" ({}) : '.format(feature_type, feature_dimension, feature_name, feature_description))
    try:
        if feature_dimension == 'scalar':
            return validate_element(feature_value, feature_type)
        elif feature_dimension == 'array':
            return parse_array(feature_value, feature_type)
        elif feature_dimension == 'matrix':
            array_content = feature_value[1:len(feature_value)-1]
            array_split = array_content.split(',')
            return [parse_array(arr, feature_type) for arr in array_split]
        else:
            print('unknown feature dimension')
    except ValueError as err:
        print(err)
        get_feature_value(feature_name, feature_type, feature_dimension, feature_description)
    except Exception as err:
        print(err)

def add_example(api, logger, prediction_id):
    reply = input('Do you want to add an example ? (y/n)')
    if reply == 'y':
        label = input('label: ') 
        return api.add_example(logger, prediction_id, label)
    elif reply == 'n':
        return None
    else:
        print('Expected y/n')
        return add_example(api, logger, prediction_id)

def predict(api, logger, project_id, features=None, annotate=True, log=True):
    try:
        project = api.get_project(logger, project_id, log=False)
        if project == None:
            return None
        problem_type = project['problem']
        features_descriptor = project['configuration']['features']['data']
        if features == None:
            features = {}
            for descriptor in features_descriptor:
                feature_name = descriptor['name']
                feature_type = descriptor['type']
                feature_dimension = descriptor['dimension']
                feature_description = descriptor['description']
                features.update({ feature_name: get_feature_value(feature_name, feature_type, feature_dimension, feature_description) })
        prediction = api.predict(logger, project['id'], features)
        labels = prediction['labels']
        print('\nalgorithm used: {}'.format(prediction['algorithmId']))
        if problem_type  == 'classification':
            table = PrettyTable(['label', 'prob'])
            for label in labels:
                table.add_row([label['label'], label['probability']])
        elif problem_type == 'regression':
            table = PrettyTable(['reg'])
            for label in labels:
                table.add_row([label['label']])
        print(table)
        if annotate:
            add_example(api, logger, prediction['id'])
        return prediction
    except Exception as err:
        print(err)
        pass
