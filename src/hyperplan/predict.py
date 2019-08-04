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

def predict(api, project_id, log=True):
    try:
        project = api.get_project(project_id, log=False)
        features_descriptor = project['configuration']['features']['data']
        features = {}
        for descriptor in features_descriptor:
            feature_name = descriptor['name']
            feature_type = descriptor['type']
            feature_dimension = descriptor['dimension']
            feature_description = descriptor['description']
            features.update({ feature_name: get_feature_value(feature_name, feature_type, feature_dimension, feature_description) })
        prediction = api.predict(project['id'], features)
        labels = prediction['labels']
        table = PrettyTable(['label', 'prob'])
        print('\nalgorithm used: {}'.format(prediction['algorithmId']))
        for label in labels:
            table.add_row([label['label'], label['probability']])
        print(table)

    except Exception as err:
        print(err)
        pass
