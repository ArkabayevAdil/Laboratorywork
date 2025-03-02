import os
path = input("Enter Directory path: ")
if os.path.exists(path):
    items = os.listdir(path)
    print("only Directory: ")
    for item in items:
        if os.path.isdir(os.path.join(path, item)):
            print(item)
    print("/nonly Files: ")
    for item in items:
        if os.path.isfile(os.path.join(path, item)):
            print(item)
    print("/All items: ")
    for item in items:
        print(item)
else:
    print("The specified path does not exist!")
    