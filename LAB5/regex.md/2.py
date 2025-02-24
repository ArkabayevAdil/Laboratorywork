import re

with open("row.txt","r")as file:
    text =file.read()

pattern = r"abb*"
result = re.findall(pattern, text)
for i in result:
    print(i, end = " ")