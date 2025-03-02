import os
files = str(input("Enter the name files: "))
copyfiles = r"C:\Users\Asus\Desktop\LaboratoryPP2\LAB6\dirandfiles\text.txt"
try:
    with open(files, "r") as original:
        data = original.read()
    with open(copyfiles, "w") as copy:
        copy.write(data)
except FileNotFoundError:
    print(f"File {files} already exists")