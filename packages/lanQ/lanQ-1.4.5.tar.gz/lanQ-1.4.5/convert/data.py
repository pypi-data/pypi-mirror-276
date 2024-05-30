import uuid
import json
from typing import List

class Data():
    Type_List = [
        'json',
        'text',
        'jsonl'
    ]

    def __init__(self, input_path: str, type: str, column_output: List[str] = None, column_id: List[str] = None, column_input: List[str] = None):
        self.input_path = input_path
        self.type = type
        self.column_id = column_id
        self.column_input = column_input
        self.column_output = column_output

        if self.type not in self.Type_List:
            raise Exception('no such data type: ' + self.type)

    def find_nested_data(self, jsn: json, levels: List[str]):
        data = jsn
        for key in levels:
            data = data[key]
        return data

    def load_data(self):
        if self.type == 'json':
            return self.load_data_from_json()
        if self.type == 'text':
            return self.load_data_from_text()
        if self.type == 'jsonl':
            return self.load_data_from_jsonl()

    def load_data_from_json(self):
        if self.column_output is None:
            raise Exception('column_output is not set')

        raw_data = []
        with open(self.input_path, 'r', encoding='utf-8') as f:
            s = f.read()
            j = json.loads(s)
            for k, v in j.items():
                raw_data.append({
                    'id': self.find_nested_data(v, self.column_id) if self.column_id is not None else k,
                    'input': self.find_nested_data(v, self.column_input) if self.column_input is not None else '',
                    'output': self.find_nested_data(v, self.column_output)
                })
        return raw_data

    def load_data_from_text(self):
        raw_data = []
        with open(self.input_path, 'r', encoding='utf-8') as f:
            for line in f:
                raw_data.append({
                    'id': str(uuid.uuid4()),
                    'input': '',
                    'output': line
                })
        return raw_data

    def load_data_from_jsonl(self):
        if self.column_output is None:
            raise Exception('column_output is not set')

        raw_data = []
        with open(self.input_path, 'r', encoding='utf-8') as f:
            for j_l in f:
                j = json.loads(j_l)
                raw_data.append({
                    'id': self.find_nested_data(j, self.column_id) if self.column_id is not None else str(uuid.uuid4()),
                    'input': self.find_nested_data(j, self.column_input) if self.column_input is not None else '',
                    'output': self.find_nested_data(j, self.column_output)
                })
        return raw_data
