from get_input import get_feature_type, get_feature_dimension, get_alphanumerical_id
from qcm_result import QCMResult
from label_schema import LabelSchema 

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



def create_labels(api):
    label_id = get_labels_id() 
    label_data = get_label_data()
    try:
        api.create_label(LabelSchema(label_id, label_data))
    except Exception as err:
        print(err)
        print('something did not work')

def label_build(label_type, label_one_of, label_description):
    return {'type': label_type, 'oneOf': label_one_of, 'description': label_description}


def get_label_data():
    label_type = get_label_type()
    label_one_of = []
    if label_type == 'oneOf':
        label_one_of = get_label_one_of()
    label_description = get_label_description()
    print("==============")
    return label_build(label_type, label_one_of, label_description)


