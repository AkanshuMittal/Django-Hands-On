import requests
import json

url = "http://127.0.0.1:8000/stucreate/"

data = {
    'name': 'Akanshu Mittal',
    'roll': 2202900100019,
    'city': 'Delhi'
}

json_data = json.dumps(data)
r = requests.post(url= url, data = json_data)
data = r.json()
print(data)