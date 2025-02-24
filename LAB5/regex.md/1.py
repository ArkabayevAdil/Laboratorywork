import re
with open("row.txt","r")as file:
    text =file.read()



pattern = r"ab*"
result = re.findall(pattern, text)
for i in result:
    print(i, end = " ")

