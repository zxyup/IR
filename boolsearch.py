import os,sys
import json

os.chdir(sys.path[0])

def boolean_search(query,inverted_index):
    # 分割查询条件
    terms = query.split()
    print(terms)
    # 定义操作数栈和操作符栈
    operand_stack = []
    operator_stack = []

    # 定义操作符优先级
    precedence = {'not': 3, 'and': 2, 'or': 1}

    # 处理查询条件
    for term in terms:
        # 处理操作数
        if term not in {'and', 'or', 'not'}:
            operand_stack.append(term)
            # print(inverted_index[term])
        # 处理操作符
        else:
            while operator_stack and precedence[operator_stack[-1]] >= precedence[term]:
                operator = operator_stack.pop()
                if operator == 'not':
                    operand = operand_stack.pop()
                    # 执行 NOT 操作
                    try:
                        result = set(inverted_index.keys()) - set(inverted_index[operand]) if type(operand)==str else operand
                    except Exception as e:
                        print(e)
                        return
                else:
                    right_operand = operand_stack.pop()
                    left_operand = operand_stack.pop()
                    # 执行 AND 或 OR 操作
                    try:
                        if operator == 'and':
                            result = set(inverted_index[left_operand]) if type(left_operand)==str else left_operand & set(inverted_index[right_operand]) if type(right_operand)==str else right_operand
                        else:
                            result = set(inverted_index[left_operand]) if type(left_operand)==str else left_operand | set(inverted_index[right_operand]) if type(right_operand)==str else right_operand
                    except Exception as e:
                        print(e)
                        return
                operand_stack.append(result)
            operator_stack.append(term)

    # 处理剩余的操作符
    while operator_stack:
        operator = operator_stack.pop()
        if operator == 'not':
            operand = operand_stack.pop()
            # 执行 NOT 操作
            try:
                result = set(inverted_index.keys()) - set(inverted_index[operand]) if type(operand)==str else operand
            except Exception as e:
                print(e)
                return
        else:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            # 执行 AND 或 OR 操作
            try:
                if operator == 'and':
                    result = set(inverted_index[left_operand]) if type(left_operand)==str else left_operand & set(inverted_index[right_operand]) if type(right_operand)==str else right_operand
                else:
                    result = set(inverted_index[left_operand]) if type(left_operand)==str else left_operand | set(inverted_index[right_operand]) if type(right_operand)==str else right_operand
            except Exception as e:
                print(e)
                return
        operand_stack.append(result)
    sorted_result = sorted(list(operand_stack[0]))
    return sorted_result

if __name__=="__main__":
    with open("index_table.json",'r',encoding='utf-8') as f:
        ii = json.loads(f.read())
    inverted_index = {}
    for k,v in ii.items():
        inverted_index[k] = list(v['docs'].keys())
    query = input("请输入布尔检索式：")
    result = boolean_search(query,inverted_index)
    if result == None:
        print("无结果")
    else:
        with open("id_url.json",'r',encoding='utf-8') as f:
            idurl = json.loads(f.read())
        for i in result:
            print(idurl[i])
