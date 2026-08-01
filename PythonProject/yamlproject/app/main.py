import yaml

with open("/Users/navyadev/Documents/GitHub/DataEngineering/PythonProject/yamlproject/example.yml", "r") as f:
    data=yaml.safe_load(f)

print(data)
print(data["key"])
print(data["mylist"][0])
print(data["mydict"]["key1"])