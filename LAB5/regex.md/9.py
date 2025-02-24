import re

with open("row.txt","r")as file:
    text =file.read()


pattern = r"(.*?)([A-Z])"
def Upp(match):
    return match.group(1) + " " + match.group(2)
result = re.sub(pattern, Upp, text)
print(result)