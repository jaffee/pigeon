import requests
import json
from pprint import pprint
import sys

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = "sample.json"

f = open(fname, 'r')

r = requests.post("http://localhost:5654/push", data=f.read())

print r
pprint(json.loads(r.text))
# import ipdb; ipdb.set_trace()
