import ast

file = open('test.py', 'r')
print(ast.dump(ast.parse(file.read())))


