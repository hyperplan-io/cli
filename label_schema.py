import json

class LabelSchema():
    def __init__(self, label_id, label_descriptors):
        self.label_id = label_id
        self.label_descriptors = label_descriptors
    def to_json(self):
        return {'id': self.label_id, 'data': self.label_descriptors}
