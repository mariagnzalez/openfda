import http.client
import json
headers = {'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov")#establecemos conexión con esa pagina
connection.request("GET", "/drug/label.json", None, headers)# le pedimos que nos de la información pedida
r1 = connection.getresponse()
print(r1.status, r1.reason)#imprimimos el estado:200 y la razon:OK
repos_raw = r1.read().decode("utf-8")
connection.close()


repos = json.loads(repos_raw)#transformamos dicho documento en diccionario, listas para que así podamos acceder de una forma más sencilla
info_medicamento=repos['results'][0]

print ('- Identificador del medicamento: ',info_medicamento['id'])
print ('- Proposito: ',info_medicamento['purpose'][0])

print ('- Fabricante: ',info_medicamento['openfda']['manufacturer_name'][0])


