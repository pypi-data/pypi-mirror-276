import os
import sys
import json
import time
import pprint
import jsonlines
import argparse
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable, Optional, List

from convert.data import Data
from configuration import Model
from lanQ_rule.config.const import QUALITY_MAP

app = FastAPI(title='lanQ: Tool for detect language quality', version='1.4.3')

class Item(BaseModel):
    input_models: List[str]
    input_path: str
    data_type: str
    column_output: Optional[List[str]] = None
    column_id: Optional[List[str]] = None
    column_input: Optional[List[str]] = None

@app.on_event("startup")
async def startup():
    print("应用程序启动了")

@app.on_event("shutdown")
def shutdown():
    print("应用程序关闭了")

@app.get("/")
def readme():
    return {'hello'}

def get_quality_signal(rule: Callable):
    for quailty_signal in QUALITY_MAP:
        if rule in QUALITY_MAP[quailty_signal]:
            return quailty_signal

    raise Exception('this rule can not find its quailty_signal: ' + rule.__name__)

def read_data(path: str, data_type: str, column_output: List[str] = None, column_id: List[str] = None, column_input: List[str] = None):
    data = Data(path, data_type, column_output=column_output, column_id=column_id, column_input=column_input)
    return data.load_data()


def write_data_rule(data, path):
    summary = {
        'input_model': data['input_model'],
        'input_path': data['input_path'],
        'score': data['score'],
        'num_good': data['num_good'],
        'num_bad': data['num_bad'],
        'total': data['total'],
        'error_info': {}
    }

    for quality_signal in data['error_info']:
        if quality_signal not in summary['error_info']:
            summary['error_info'][quality_signal] = []
        for rule_name in data['error_info'][quality_signal]:
            summary['error_info'][quality_signal].append({'filter_by_func': rule_name, 'ratio':data['error_info'][quality_signal][rule_name]['ratio']})
            with open(path + '/{}.json'.format(rule_name), 'w', encoding='utf-8') as f:
                json.dump(data['error_info'][quality_signal][rule_name], f, indent=4, ensure_ascii=False)

    with open(path + '/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    return summary

def write_data_model(data, path):
    summary = {
        'input_model': data['input_model'],
        'input_path': data['input_path'],
        'score': data['score'],
        'num_good': data['num_good'],
        'num_bad': data['num_bad'],
        'total': data['total'],
        'error_info': [],
    }

    for error_type in data['error_info']:
        summary['error_info'].append({'error_type': error_type, 'ratio':data['error_info'][error_type]['ratio']})
        with open(path + '/{}.json'.format(error_type), 'w', encoding='utf-8') as f:
            json.dump(data['error_info'][error_type], f, indent=4, ensure_ascii=False)

    with open(path + '/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    return summary

def execute_rule(record, rule_map, d):
    if_good = True
    for r in rule_map:
        r_n = r.__name__
        # execute rule
        if r_n.startswith('prompt'):
            tmp = r(d['input'], d['output'])
        else:
            tmp = r(d['output'])
        # analyze result
        if tmp['error_status'] == False:
            continue
        if_good = False
        q_s = get_quality_signal(r)
        if q_s not in record['error_info']:
            record['error_info'][q_s] = {}
        if r_n not in record['error_info'][q_s]:
            record['error_info'][q_s][r_n] = {'name': r_n, 'count': 0, 'ratio': 0, 'detail': []}
        record['error_info'][q_s][r_n]['count'] += 1
        record['error_info'][q_s][r_n]['detail'].append({'id': d['id'], 'input': d['input'], 'output': d['output'], 'error_reason': tmp['error_reason']})

    if if_good == False:
        record['num_bad'] += 1

def execute_model(record, api, d):
    tmp = api(d['output'])
    if tmp['score'] > 6:
        return

    record['num_bad'] += 1
    e = tmp['error']
    if e not in record['error_info']:
        record['error_info'][e] = {'name': e, 'count': 0, 'ratio': 0, 'detail': []}
    record['error_info'][e]['count'] += 1
    record['error_info'][e]['detail'].append({'api_score':tmp['score'], 'id': d['id'], 'input': d['input'], 'output': d['output'], 'error_reason': tmp['reason']})

def calculate_ratio(record, model_type):
    record['num_good'] = record['total'] - record['num_bad']
    record['score'] = record['num_good'] / record['total'] * 100
    if model_type == 'rule':
        for q_s in record['error_info']:
            for r_n in record['error_info'][q_s]:
                record['error_info'][q_s][r_n]['ratio'] = record['error_info'][q_s][r_n]['count'] / record['total']
    else:
        for e in record['error_info']:
            record['error_info'][e]['ratio'] = record['error_info'][e]['count'] / record['total']

@app.post("/main/")
def main(item: Item):
    current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    input_path = item.input_path
    output_path = 'data/outputs/' + current_time
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    record_list = []
    for model_name in item.input_models:
        model = Model(model_name)

        model_path = output_path + '/' + model.model_name
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        record = {
            'input_model': model.model_name,
            'input_path': input_path,
            'score': 0,
            'num_good': 0,
            'num_bad': 0,
            'total': 0,
            'error_info': {},
        }
        path_list = []
        path_list.append(input_path)
        while len(path_list) != 0:
            path = path_list.pop(0)
            print('[Handling]:' + path)
            if os.path.isfile(path):
                # type: file
                dataset = read_data(path, item.data_type, column_output=item.column_output, column_id=item.column_id, column_input=item.column_input)
                record['total'] += len(dataset)
                if len(dataset) == 0:
                    continue
                for data in dataset:
                    if model.model_type == 'rule':
                        execute_rule(record, model.load_model(), data)
                    if model.model_type == 'model':
                        execute_model(record, model.load_model(), data)

            if os.path.isdir(path):
                # type: directory
                for path_child in os.listdir(path):
                    path_child = path + '/' + path_child
                    path_list.append(path_child)

        calculate_ratio(record, model.model_type)

        pprint.pprint(record, sort_dicts=False)
        if model.model_type == 'rule':
            summary = write_data_rule(record, model_path)
        if model.model_type == 'model':
            summary = write_data_model(record, model_path)

        record_list.append(summary)
    return record_list

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8081)