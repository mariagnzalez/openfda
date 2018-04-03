import http.client
import json

headers = {'User-Agent': 'http-client'}
skip=0
while True:

    connection = http.client.HTTPSConnection("api.fda.gov")
    connection.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100&skip='+str(skip), None, headers)
    r1 = connection.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    connection.close()
    repos= json.loads(repos_raw)
    for elemento in range (len(repos['results'])):#recorro la lista de 'results' (teniendo 10 posiciones)
        info_medicamento=repos['results'][elemento]
        if not (info_medicamento['openfda']):#si existe la opción 'openfda' entonces imprimir el fabricante.
            continue
        print('-Fabricante',elemento+1,':',info_medicamento['openfda']['manufacturer_name'][0])
    # Utilizamos la opción search= active_ingredient como dice openFDA para encontrar todos aquellos medicamentos que presenten el acetilsalycilic
    # Imponemos un limit= 100.
    if (len(repos['results']))<100:
        break
    skip=skip+100

