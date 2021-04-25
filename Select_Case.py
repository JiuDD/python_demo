import pandas as pd
import json
import sys

obj1 = '''
[{"name": "李四", "age": 25, "pet": "汪星人"},
{"name": "王五", "age": 23, "pet": "喵星人"},
{"name": "李二", "age": 18, "pet": "喵星人"}]
'''

obj2 = '''
[{"name": "张三", "age": 25, "pet": "汪星人"},
{"name": "马六", "age": 23, "pet": "土星人"}]
'''


'''
select的case，处理Json数据:
1.case_column:              case字段
2.enum_key_value_pair:      case的enum的key、value对
3.json_array待处理对象
'''
def hand_data_case(case_column, enum_key_value_pair, json_array):
    print(case_column)


'''
select的concat，处理Json数组格式数据或者<class 'pandas.core.frame.DataFrame'>格式的数据:
1.array_concat_column:      需要concat的字段数组
2.alias:                    concat字段的别名
3.temp_data:                可以为DataFrame格式、Json数组格式的结果集参数
'''
def hand_data_concat(array_concat_column, alias, temp_data):
    #将<class 'pandas.core.frame.DataFrame'>格式参数转换为Json数组
    isPandasDataFrame = isinstance(temp_data, pd.DataFrame)
    if isPandasDataFrame:
        temp_data = temp_data.to_json(orient="records", force_ascii=False)
    json_array = json.loads(temp_data)
    print(json_array)

    #concat
    for single_json in json_array:
        concat_value = ''
        for j in array_concat_column:
            value = single_json[j]
            concat_value = concat_value + str(value)
        single_json[alias] = concat_value
        #删除原key
        for x in array_concat_column:
            del single_json[x]
    return json_array



if __name__ == '__main__':
    # 1、测试 concat
    array_concat_column = ["name", "age"]
    alias = "concat_name_age"
    # Json数组格式参数的测试
    obj = hand_data_concat(array_concat_column, alias, obj1)
    print(obj)

    # <class 'pandas.core.frame.DataFrame'>格式参数的测试
    json_array = json.loads(obj1)
    json_data = pd.DataFrame(json_array)
    obj = hand_data_concat(array_concat_column, alias, json_data)
    print(obj)

    # 2、测试 coalesce
