import re

with open("row.txt","r")as file:
    text =file.read()

pattern = re.compile('(?=[A-Z])')
def camelToSnake(camel):
    almCamel = pattern.sub('_', camel)
    return almCamel.lower()
print(camelToSnake(text))
