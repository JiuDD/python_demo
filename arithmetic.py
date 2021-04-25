import pandas
import json
import sys

import pandas as pd

obj1 = '''
[{"id": 1,"name": "李一", "age": 25, "pet": "汪星人"},
{"id": 2,"name": "李二", "age": 23, "pet": "喵星人"},
{"id": 3,"name": "李三", "age": 18, "pet": "火星人"}]
'''


def test():
    sql = {
        'having': {
            'age': '3',
            'operator': '>'
        },
        'select_item': {
            'age*id': 'multiply',
            'age+id': 'add',
            'age-id': 'substract',
            'age/id': 'divide'
        },
        'join_clause': {
            'rightTable': 'data4',
            'onCloumn': 'data3.userId,data4.userId',
            'onOperator': '=',
            'joinType': ' join'
        },
        'arithmetic': {
            'add': 'age,id',
            'div': 'age,id',
            'sub': 'age,id',
            'mul': 'age,id'
        },
        'where': {
            '1': {
                'name,=': '1',
                'age,=': '2',
                'operator': 'and'
            },
            'depth': '1'
        },
        'fromTable': 'data3',
        'group': {
            'group_by': 'age'
        }
    }
    json_value = json.loads(obj1)
    df = pd.DataFrame(json_value)

    arithmetic = sql["arithmetic"]
    select_item = sql["select_item"]
    print(arithmetic)
    if 'add' in arithmetic or 'sub' in arithmetic or 'mul' in arithmetic or 'div' in arithmetic:
        add_arithmetic = arithmetic.get("add")
        sub_arithmetic = arithmetic.get("sub")
        mul_arithmetic = arithmetic.get("mul")
        div_arithmetic = arithmetic.get("div")

        # 加法
        if add_arithmetic is not None:
            alias_params = get_alias_for_arithmetic(arithmetic, "add", select_item)
            alias = alias_params["alias"]
            # 参与运算的参数列表
            params = alias_params["params"]

            # 加法运算处理
            # 1.首先先添加一列，初始值为运算参数的第1个
            df.insert(0, alias, df[params[0]], allow_duplicates=False)
            # 2.给新字段赋值
            i = 1
            while i < len(params):
                df[alias] += df[params[i]]
                i += 1

        # 减法
        if sub_arithmetic is not None:
            alias_params = get_alias_for_arithmetic(arithmetic, "sub", select_item)
            alias = alias_params["alias"]
            # 参与运算的参数列表
            params = alias_params["params"]

            # 减法运算处理
            # 1.首先先添加一列，初始值为运算参数的第1个
            df.insert(0, alias, df[params[0]], allow_duplicates=False)
            # 2.给新字段赋值
            i = 1
            while i < len(params):
                df[alias] -= df[params[i]]
                i += 1

        #乘法
        if mul_arithmetic is not None:
            alias_params = get_alias_for_arithmetic(arithmetic, "mul", select_item)
            alias = alias_params["alias"]
            # 参与运算的参数列表
            params = alias_params["params"]

            # 乘法运算处理
            # 1.首先先添加一列，初始值为运算参数的第1个
            df.insert(0, alias, df[params[0]], allow_duplicates=False)
            # 2.给新字段赋值
            i = 1
            while i < len(params):
                df[alias] *= df[params[i]]
                i += 1

        #除法
        if div_arithmetic is not None:
            alias_params = get_alias_for_arithmetic(arithmetic, "div", select_item)
            alias = alias_params["alias"]
            # 参与运算的参数列表
            params = alias_params["params"]

            # 除法运算处理
            # 1.首先先添加一列，初始值为运算参数的第1个
            df.insert(0, alias, df[params[0]], allow_duplicates=False)
            # 2.给新字段赋值
            i = 1
            while i < len(params):
                df[alias] /= df[params[i]]
                i += 1
            print(df.to_json(orient="records", force_ascii=False))

'''
获取列别名
1.arithmetic            sql里的算法定义
2.arithmetic_fun        具体算法，eg：add、sub、mul、div
3.select_item           查询项
'''
def get_alias_for_arithmetic(arithmetic, arithmetic_fun, select_item):
    arithmetic_param = arithmetic.get(arithmetic_fun)
    # 取出别名
    params = arithmetic_param.split(",")
    key = ""
    symbol = ""
    if "add" == arithmetic_fun:
        symbol = "+"
    if "sub" == arithmetic_fun:
        symbol = "-"
    if "mul" == arithmetic_fun:
        symbol = "*"
    if "div" == arithmetic_fun:
        symbol = "/"
    for i in params:
        key += i + symbol
    key = key[0:len(key)-1]
    alias = select_item[key]
    # alias：别名      params：参与运算的参数列表
    dict_param = {"alias": alias, "params": params}
    return dict_param


if __name__ == '__main__':
    test()
