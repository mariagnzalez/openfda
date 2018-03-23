import http.client
import json

headers = {'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov")
connection.request("GET", "/drug/label.json?search=active_ingredient:%22acetylsalicylic%22&limit=100", None, headers)
r1 = connection.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
connection.close()
repos= json.loads(repos_raw)
for i in range (len(repos['results'])):#recorro la lista de 'results' (teniendo 10 posiciones)
    info_medicamento=repos['results'][i]
    if (info_medicamento['openfda']):
        print('-Fabricante: ',info_medicamento['openfda']['manufacturer_name'][0])
