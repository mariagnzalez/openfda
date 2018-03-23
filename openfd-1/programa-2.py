import http.client
import json

headers = {'User-Agent': 'http-client'} #voy a hacer un cliente, voy a atacar al api de openFDA
#cuando yo lance la petivción Get . LANZO mi información a openFDA
conn = http.client.HTTPSConnection("api.fda.gov")#me creo una conexion con open FDA
conn.request("GET", "/drug/label.json?limit=10", None, headers)#sobre esa conexion mando una peticion
r1 = conn.getresponse()#conseguir respuesta deopenFDA
print(r1.status, r1.reason)#status:200, razon:Ok
label_raw = r1.read().decode("utf-8")#leyendo la respuesta complenta en formato json
conn.close()
#lo de limit=10 lo pone en el apirest

label=json.loads(label_raw)#decirle a la libreria json tansformarlo a modo dicconario, lista...
for i in range