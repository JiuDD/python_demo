import pandas as pd
import json
import sys
import demjson


obj1 = '''
[{"id": 1,"name": "李一", "age": 25, "pet": "汪星人"},
{"id": 2,"name": "李二", "age": 23, "pet": "喵星人"},
{"id": 3,"name": "李三", "age": 18, "pet": "火星人"}]
'''

def test():
    sql = {'having': {'age': '3', 'operator': '>'},
           'select_item': {'concat(age,name,id)': 'aliasName', 'nvl(age,1)': 'nvl(age,1)'},
           'expr_func': {'nvl': 'age,1', 'concat': 'age,name,id'},
           'join_clause': {'rightTable': 'data4', 'onCloumn': 'data3.proviceId,data4.proviceId', 'onOperator': '=',
                           'joinType': ' join'}, 'arithmetic': {},
           'where': {'1': {'k,=': '4', 'operator': 'and'}, '2': {'name,=': '1', 'age,=': '2', 'operator': 'and'},
                     'depth': '2'}, 'fromTable': 'data3', 'group': {'group_by': 'age'}}

    expr_func = sql["expr_func"]
    select_item = sql["select_item"]
    print(expr_func)
    if 'concat' in expr_func:
        value = expr_func.get("concat")
        print(value)
        value_items = value.split(",")
        print(value_items)
        json_value = json.loads(obj1)
        df = pd.DataFrame(json_value)
        print(df)
        # 将非str类型转换为str（全局转换）
        df = df.applymap(str)

        new_column_name_key = "concat(" + value + ")"
        # new_column_name_value = select_item[new_column_name_key]
        new_column_name_value = select_item.get(new_column_name_key)

        df.insert(0, new_column_name_value, "", allow_duplicates=False)

        i = 0
        # obj12 =df[new_column_name_value]
        while i < len(value_items):
            df[new_column_name_value] += df[value_items[i]]
            i += 1
        print(df)

if __name__ == '__main__':
    test()
