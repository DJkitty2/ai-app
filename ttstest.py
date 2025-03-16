import os 

name = os.name
print(name) 

if name == "nt":
    key = "Insert"
    print(key)
else:
    key = "esc"
    print(key)
