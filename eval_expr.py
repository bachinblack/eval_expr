#!/usr/bin/python3
import sys
import re

NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

OPERATORS1 = ['+', '-', '%', '+-', '--', '%-']

LAMBDAS1 = [
    lambda a, b: a + b,
    lambda a, b: a - b,
    lambda a, b: a % b,
    lambda a, b: a - b,
    lambda a, b: a + b,
    lambda a, b: a % -b,
]

OPERATORS2 = ['*', '/', '*-', '/-']

LAMBDAS2 = [
    lambda a, b: a * b,
    lambda a, b: a / b,
    lambda a, b: a * -b,
    lambda a, b: a / -b,
]

OPERATORS = OPERATORS1 + OPERATORS2

PARENTHESES = ['(', ')']

LEGAL_CHARS = NUMBERS + OPERATORS + PARENTHESES


def checkCharacters(exp):
    for c in exp:
        if c not in LEGAL_CHARS:
            print("Illegal char [{}] in expression [{}]".format(c, exp))
            exit(1)


def any_op(arr, op_types, lambdas):
    for i in range(0, len(arr)):
        if arr[i] in op_types:
            op = op_types.index(arr[i])
            return i, lambdas[op]
    return -1, None


def exec_op(arr, i, op):
    n1 = int(arr[i-1])
    n2 = int(arr[i+1])
    tmp = str(op(n1, n2))
    return [tmp]


def evaluate(exp):
    # String to array
    arr = re.findall('[\d.]+|[+\-%\/*]+', exp)

    i = 0
    while i != -1:
        # search for lvl 2 OPS
        i, op = any_op(arr, OPERATORS2, LAMBDAS2)
        if op is not None:
            arr = arr[:i-1] + exec_op(arr, i, op) + arr[i+2:]
            continue
        # then for lvl 1
        i, op = any_op(arr, OPERATORS1, LAMBDAS1)
        if op is not None:
            arr = arr[:i-1] + exec_op(arr, i, op) + arr[i+2:]
    # print(arr[0])
    return (arr[0])


def compute(exp):
    # Evaluating every elements inside parentheses
    start = exp.rfind('(')
    while start != -1:
        end = exp.find(')', start)
        if (end == -1):
            print("missing ending parenthese")
            exit(1)
        sub = exp[start+1:end]
        # print(sub)
        exp = exp[:start] + evaluate(sub) + exp[end+1:]
        # print(exp)
        # print("--------------------")
        # getting next parenthese
        start = exp.rfind('(')

    # Evaluating remaining elements
    return evaluate(exp)


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        print("Usage: ./eval_expr.py [expression]")
        exit(1)

    # Removing every spaces
    exp = sys.argv[1].replace(' ', '')

    # Some security checks
    checkCharacters(exp)
    # Evaluate the expression
    res = compute(exp)
    print("{}".format(res))
