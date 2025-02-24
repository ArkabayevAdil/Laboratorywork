import re

with open("row.txt","r")as file:
    text =file.read()


pattern = r"a.+b"
result = re.findall(pattern, text)
print(result)
