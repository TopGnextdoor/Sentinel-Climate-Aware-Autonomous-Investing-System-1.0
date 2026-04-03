import urllib.request
import json
data = json.dumps({'budget': 100000, 'risk_level': 'high', 'max_trade': 100000, 'avoid_sectors': []}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/analyze', data=data, headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
parsed = json.loads(res.read().decode('utf-8'))
with open('debug_out.json', 'w') as f:
    json.dump(parsed, f, indent=4)
