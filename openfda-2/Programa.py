import http.client
import json

headers = {'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov")
connection.request("GET", "/drug/label.json?limit=10search:acetylsalicylic", None, headers)
r1 = connection.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
connection.close()
repos= json.loads(repos_raw)
