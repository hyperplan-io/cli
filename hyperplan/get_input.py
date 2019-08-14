
def get_alphanumerical_id():
    data = input('name(alphanumerical): ')
    if data.isalnum():
        return data
    else:
        print('name should be an alphanumerical string')
        return get_alphanumerical_id()

def get_feature_type():
    feature_type = input('type(string, float, int): ')
    if feature_type != 'string' and feature_type != 'float' and feature_type != 'int':
        print("feature type should be one of: 'string', 'float', 'int'")
        return get_feature_type()
    else:
        return feature_type
def get_feature_dimension():
    feature_dimension = input("dimension('scalar', 'array', 'matrix'): ")
    if feature_dimension != 'scalar' and feature_dimension != 'array' and feature_dimension != 'matrix':
        print("dimension should be one of 'scalar', 'array', 'matrix'")
        return get_feature_dimension()
    else:
        return feature_dimension
