import os
path = str(input("Enter the directory path: "))
if os.access(path, os.F_OK):
    list = os.listdir(path)
    print("Files: ")
    for i in list:
        print(i)
else:
    print("path is wrong!")
        