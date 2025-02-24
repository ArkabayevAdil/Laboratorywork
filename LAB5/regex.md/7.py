import re

with open("row.txt","r")as file:
    text =file.read()

pattern = r"(.*?)_([a-zA-Z])"
def snake(match):
    return match.group(1) + match.group(2).upper()
result = re.sub(pattern, snake, text)
print(result)
