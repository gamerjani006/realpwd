import json

with open('database.json','r') as f:
	vault=f.read()
	x=json.loads(vault)

print(type(x))