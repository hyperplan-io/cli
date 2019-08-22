from prettytable import PrettyTable

from hyperplan.qcm_result import QCMResult
from hyperplan.get_input import get_feature_type, get_feature_dimension, get_alphanumerical_id
from hyperplan.label_schema import LabelSchema 

def post_features():
    return []

def noop():
    return []

def qcm(choice_1, choice_2, choice_3):
    print('1. Create a new label')
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

def list_labels(api, logger):
    try:
        labels = api.list_labels(logger, log=False)
        logger.debug('server returns labels: {}'.format(labels))
        if labels == None:
            return None
        table = PrettyTable(['Id', 'Type', 'Description', 'oneOf'])
        for label in labels:
            data = label['data']
            label_id = label['id']
            label_type = data['type']
            label_description = data['description']
            if label_type == 'oneOf':
                label_one_of = ", ".join(data['oneOf'])
                table.add_row([label_id, label_type, label_description, label_one_of])
            elif label_type == 'dynamic':
                table.add_row([label_id, label_type, label_description, ''])
            else:
                print('Label type is unknown')
        print(table)
        return labels
    except Exception as err:
        logger.warn('An unhandled error occurred in list_labels: {}'.format(err))
        return None

def describe_label(api, logger, label_id):
    try:
        label = api.get_labels(logger, label_id, log=False)
        logger.debug('server returns label: {}'.format(label))
        if label == None:
            return None
        data = label['data']
        label_type = data['type']
        label_description = data['description']
        if label_type == 'oneOf':
            label_one_of = ", ".join(data['oneOf'])
            table = PrettyTable(['Id', 'Type', 'Description', 'oneOf'])
            table.add_row([label_id, label_type, label_description, label_one_of])
            print(table)
        elif label_type == 'dynamic':
            table = PrettyTable(['Id', 'Type', 'Description'])
            table.add_row([label_id, label_type, label_description])
            print(table)
        else:
            print('Label type is unknown')
        return label
    except Exception as err:
        logger.warn('an unhandled error occurred in describe_labels: {}'.format(err))
        return None

def get_labels_id():
    feature_id = input('id: ')
    if not feature_id.isalnum():
        print('Label descriptor id should be alphanumeric')
        return get_labels_id() 
    return feature_id

def get_label_type():
    label_type = input('type(oneOf or dynamic): ')
    if label_type != 'oneOf' and label_type != 'dynamic':
        print('Label type should either be oneOf or dynamic')
        return get_label_type() 
    return label_type

def get_label_one_of():
    one_of = input('enter the labels separated by a comma: ')
    return one_of.split(",")

def get_label_description():
    description = input('description: ')
    return description 



def create_labels(api, logger, label_id, label_type=None, label_one_of=None, label_description=None):
    label_data = get_label_data(label_type, label_one_of, label_description)
    label_schema = LabelSchema(label_id, label_data)
    logger.debug('json payload for create_labels: {}'.format(label_schema.to_json()))
    try:
        api.create_label(logger, label_schema)
    except Exception as err:
        logger.warn('an unhandled error occurred in create_labels: {}'.format(err))
        return None

def label_build(label_type, label_one_of, label_description):
    return {'type': label_type, 'oneOf': label_one_of, 'description': label_description}


def get_label_data(label_type=None, label_one_of=None, label_description=None):
    if label_type == None:
        label_type = get_label_type()
    if label_type == 'oneOf' and label_one_of == None:
        label_one_of = get_label_one_of()
    elif label_type == 'dynamic':
        label_one_of = []
    if label_description == None:
        label_description = get_label_description()
    return label_build(label_type, label_one_of, label_description)


