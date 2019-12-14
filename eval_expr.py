#!/usr/bin/python3
import sys
import re
import argparse
from operator import add, sub, mod, truediv, mul, pow


parser = argparse.ArgumentParser(description='Resolve a mathematical expression.')
parser.add_argument('exp', type=str, help='an expression')
parser.add_argument('-r', '--recursive', dest='rec', action='store_true', help='solve the expression recursively')

OPER1 = {
    '+': add,
    '-': sub,
    '%': mod,
    '--': add,
    '++': add,
    '+-': sub,
    '-+': sub,
    '%-': lambda a, b: mod(a, -b)
}


OPER2 = {
    '*': mul,
    '**': pow,
    '/': truediv,
    '*-': lambda a, b: mul(a, -b),
    '/-': lambda a, b: truediv(a, -b)
}


OPERATORS = list(OPER1.keys()) + list(OPER2.keys())


LEGAL_CHARS = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')'
] + OPERATORS


def checkCharacters(exp):
    for c in exp:
        if c not in LEGAL_CHARS:
            print("Illegal char [{}] in expression [{}]".format(c, exp))
            exit(1)


def exec_op(li, op, i):
    try:
        n1 = int(li[i-1])
        n2 = int(li[i+1])
        tmp = str(op(n1, n2))
        return [tmp]
    except ValueError:
        print(
            "Formatting error in expression. Last expression state was {}"
            .format(li)
        )
        exit(1)


def compute_op(li, op_types):
    i = 0
    # Looping through li.
    # Everytime an op is found, skipping one increment
    while i < len(li):
        if li[i] in op_types:
            op = op_types[li[i]]
            # Execute the operator and insert it in the array
            exec_op(li, op, i)
            li = li[:i-1] + exec_op(li, op, i) + li[i+2:]
            # print(li)
            continue
        i += 1
    return li


def compute_op_rec(li, op_types, i=0):
    if i < len(li):
        if li[i] in op_types:
            op = op_types[li[i]]
            # Execute the operator and insert it in the array
            exec_op(li, op, i)
            li = li[:i-1] + exec_op(li, op, i) + li[i+2:]
            return compute_op_rec(li, op_types, i)
        return compute_op_rec(li, op_types, i+1)
    return li


def clean_ops(li):
    for elem in li:
        # Check if the element is an illegal stacking of operators
        # If so, trying to resolve it
        if elem[0] in OPERATORS and elem not in OPERATORS:
            for c in reversed(elem):
                print("Illegal stacking of operators [{}]".format(elem))
                exit(1)
    return li


def evaluate(exp, rec=False):
    # String to array
    li = re.findall('[\d.]+|[+\-%\/*]+', exp)
    li = clean_ops(li)
    if rec is True:
        # search for lvl 2 OPS (*, /)
        li = compute_op_rec(li, OPER2)
        # then for lvl 1 OPS (+, -, %)
        li = compute_op_rec(li, OPER1)
    else:
        li = compute_op(li, OPER2)
        li = compute_op(li, OPER1)
    return (li[0])


def compute(exp):
    # Evaluating every elements inside parentheses
    start = exp.rfind('(')
    while start != -1:
        end = exp.find(')', start)
        if (end == -1):
            print("missing ending parenthese")
            exit(1)
        sub = exp[start+1:end]
        exp = exp[:start] + evaluate(sub) + exp[end+1:]
        # print(exp)
        # print("--------------------")
        # getting next parenthese
        start = exp.rfind('(')

    # Evaluating remaining elements
    return evaluate(exp)


def compute_rec(exp):
    # Evaluating every elements inside parentheses
    start = exp.rfind('(')
    if start != -1:
        end = exp.find(')', start)
        if (end == -1):
            print("missing ending parenthese")
            exit(1)
        sub = exp[start+1:end]
        exp = exp[:start] + evaluate(sub) + exp[end+1:]
        # calling function again
        return compute_rec(exp)
    # Evaluating remaining elements
    return evaluate(exp, rec=True)

if __name__ == "__main__":
    args = parser.parse_args()

    # Removing every spaces
    exp = args.exp.replace(' ', '')

    # Some security checks
    checkCharacters(args.exp)

    # Evaluate the expression
    if args.rec is True:
        res = compute_rec(exp)
    else:
        res = compute(exp)
    print(res)
