import re

with open("row.txt","r")as file:
    text =file.read()
pattern = r"[ ,.]"
final = re.sub(pattern, ":", text)
print(final)