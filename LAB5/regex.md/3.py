import re

with open("row.txt","r")as file:
    text =file.read()

pattern = r"[a-z]+_ +[a-z]"
result = re.findall(pattern, text)
for i in result:
    print(i, end = " ")
    