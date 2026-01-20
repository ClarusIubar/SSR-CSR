import os, json

class MaslowService:
    def __init__(self, base_dir):
        self.data_path = os.path.join(base_dir, 'data', 'maslow.json')

    def get_steps(self):
        if not os.path.exists(self.data_path):
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)