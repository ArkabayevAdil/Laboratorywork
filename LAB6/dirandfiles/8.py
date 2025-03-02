import os
files = str(input("Enter the name files: "))
if os.access(files, os.F_OK):
    os.remove(files)
else:
    print("File not found!")