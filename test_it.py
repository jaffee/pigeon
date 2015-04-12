import requests
import json
from pprint import pprint
import sys

print sys.argv

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = "sample.json"

f = open(fname, 'r')

resp = requests.post("http://localhost:5654/push", data=f.read())


print resp
pprint(json.loads(resp.text))
# import ipdb; ipdb.set_trace()
