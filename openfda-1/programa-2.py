import http.client
import json

headers = {'User-Agent': 'http-client'}

connection = http.client.HTTPSConnection("api.fda.gov")
connection.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = connection.getresponse()
if r1.status==404:
    print('Recurso no encontrado')
    exit(1)
repos_raw = r1.read().decode("utf-8")
connection.close()
repos= json.loads(repos_raw)
#para acceder a los 10 identificadores hago uso de un bucle for.
for i in range (len (repos['results'])):#recorro la lista de 'results' (teniendo 10 posiciones)
    info_medicamento=repos['results'][i]#obtendremos la información de cada medicamento ya que la 'i' tomará valores de 0-9

    print ('- Identificador del medicamento ',i+1,': ' ,info_medicamento['id'])
#La modificación se establece en la forma que tenemos que pedir a la página. En este caso imponemos un límite como dice la propia pagina que se debe de hacer
