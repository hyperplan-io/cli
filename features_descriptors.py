from get_input import get_feature_type, get_feature_dimension, get_alphanumerical_id
from prettytable import PrettyTable
from qcm_result import QCMResult
from feature_schema import FeatureSchema

def post_features():
    return []

def noop():
    return []

def qcm(choice_1, choice_2, choice_3):
    print('1. Create a new feature')
    print('2. Finish and save')
    print('3. Finish and ignore')
    choice = input('Choose: ')
    if choice == '1':
        return (QCMResult.CREATED_FEATURE, choice_1())
    elif choice == '2':
        return (QCMResult.CLOSE_AND_SAVE, choice_2())
    elif choice == '3':
        return (QCMResult.CLOSE_AND_DO_NOT_SAVE, choice_3())
    else:
        return qcm(choice_1, choice_2, choice_3)

def get_features_id():
    feature_id = input('id: ')
    if not feature_id.isalnum():
        print('Feature descriptor id should be alphanumeric')
        return get_features_id() 
    return feature_id

def describe_feature(api, feature_id):
    table = PrettyTable(['Name', 'Type', 'Dimension', 'Description'])
    features = api.get_features(feature_id, log=False)
    for data in features['data']:
        feature_name = data['name']
        feature_type = data['type']
        feature_dimension = data['dimension']
        feature_description = data['description']
        table.add_row([feature_name, feature_type, feature_dimension, feature_description])
    print(table)

def create_features(api):
    table = PrettyTable(['Name', 'Type', 'Dimension', 'Description'])
    feature_id = get_features_id() 
    features = []
    print(table)
    while True:
        (result, feature) = qcm(get_feature_data, post_features, noop)
        if result != QCMResult.CREATED_FEATURE:
            break
        features.append(feature)
        table.add_row(feature.values())
        print(table)
    if result == QCMResult.CLOSE_AND_SAVE:
        print('saving feature descriptor {}'.format(feature_id))
        try:
            api.create_feature(FeatureSchema(feature_id, features))
            print('its ok')
        except Exception as err:
            print(err)
            print('something did not work')

def feature_build(feature_name, feature_type, feature_dimension, feature_description):
    return {'name': feature_name, 'type': feature_type, 'dimension': feature_dimension, 'description': feature_description}


def get_feature_data():
    print("============== Create feature")
    feature_name = get_alphanumerical_id()
    feature_type = get_feature_type()
    feature_dimension = get_feature_dimension()
    feature_description = input('description: ')
    print("==============")
    return feature_build(feature_name, feature_type, feature_dimension, feature_description)


