import json

class FeatureSchema():
    def __init__(self, feature_id, feature_descriptors):
        self.feature_id = feature_id
        self.feature_descriptors = feature_descriptors
    def to_json(self):
        return {'id': self.feature_id, 'data': self.feature_descriptors}
