import uuid
import json
import orjson

from typing import List

from pyspark.sql import Row, DataFrame
from pyspark.sql.functions import explode, count,col, format_number
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, ArrayType


def find_nested_data(jsn: json, levels: List[str]):
    data = jsn
    for key in levels:
        data = data[key]
    return data

def execute_rule(rule_map, d):
    d['error_status'] = True
    d['error_functions'] = []
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

        d['error_status'] = False
        d['error_functions'].append(r_n)
    return d

def convert_data(df: DataFrame,
                 column_output: List[str],
                 column_id: List[str] = None,
                 column_input: List[str] = None) -> DataFrame:
    def func(row) -> Row:
        data = orjson.loads(row.value)
        new_data = {
            'id': find_nested_data(data, column_id) if column_id is not None else str(uuid.uuid4()),
            'input': find_nested_data(data, column_input) if column_input is not None else '',
            'output': find_nested_data(data, column_output),
        }
        return Row(value=orjson.dumps(new_data).decode("utf-8"))

    convert_df = df.rdd.map(func).toDF()
    return convert_df

def process_data(rule_map, df: DataFrame) -> DataFrame:
    def func1(row):
        data = orjson.loads(row.value)
        new_data = execute_rule(rule_map, data)
        return Row(value=orjson.dumps(new_data).decode("utf-8"))
    output_df = df.rdd.map(func1).toDF()

    def func2(row) -> Row:
        return orjson.loads(row.value)['error_status'] is False
    output_df = output_df.rdd.filter(func2).toDF()

    return output_df

def extract_error_info(spark, df: DataFrame) -> DataFrame:
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("error_status", BooleanType(), True),
        StructField("error_functions", ArrayType(StringType()), True)
    ])

    def func(row):
        data = orjson.loads(row.value)
        return Row(id=data['id'], error_status=data['error_status'], error_functions=data['error_functions'])

    df_error_info = spark.createDataFrame(df.rdd.map(func), schema=schema)
    return df_error_info

def get_summary(input_df: DataFrame, output_df: DataFrame) -> json:
    summary = {
        'score': 0,
        'num_good': 0,
        'num_bad': output_df.count(),
        'total': input_df.count()
    }
    summary['num_good'] = summary['total'] - summary['num_bad']
    summary['score'] = summary['num_good'] / summary['total']
    return summary

def caculate_error_ratio(df: DataFrame, num_total: int) -> DataFrame:
    df_exploded = df.select("id", explode("error_functions").alias("error_function"))
    df_grouped = df_exploded.groupBy("error_function").agg(count("*").alias("count"))
    df_grouped = df_grouped.withColumn("ratio", format_number(col("count") / num_total, 4))

    return df_grouped

# if __name__ == '__main__':
#     j = {"myid": 123, 'myinput': '', 'myoutput': '�I am 8 years old. I love apple because:'}
#     output = find_nested_data(j, ['myoutput'])
#     print(output)