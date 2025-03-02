import string
import os
for letter in string.ascii_uppercase:
    filename = f"{letter}.txt"
    try:
        with open(filename, "x") as file:
            file.write(f"This is files {filename}\n")
        print(f"Created files {filename}")
    except FileExistsError:
        print(f"File {filename} already exists")





for letter in string.ascii_uppercase:
    filename = f"{letter}.txt" 
    if os.path.exists(filename):
        os.remove(filename) 
        print(f"Deleted file: {filename}")
    else:
        print(f"File {filename} not found. Skipping.")

            