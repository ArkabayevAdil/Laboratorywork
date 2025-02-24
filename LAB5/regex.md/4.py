import re

with open("row.txt","r")as file:
    text =file.read()

pattern = r"[A-Z]{1}[a-z]+"
result = re.findall(pattern, text)
print(result)