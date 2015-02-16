import requests
import json
from pprint import pprint

f = open("sample.json", 'r')


r = requests.post("http://localhost:5654/push", data=f.read())

print r
pprint(json.loads(r.text))
# import ipdb; ipdb.set_trace()
