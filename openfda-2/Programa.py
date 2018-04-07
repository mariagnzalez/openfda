import http.client
import json

headers = {'User-Agent': 'http-client'}
skip=0
while True:

    connection = http.client.HTTPSConnection("api.fda.gov")
    connection.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100&skip='+str(skip), None, headers)
    r1 = connection.getresponse()
    if r1.status == 404:
        print('Recurso no encontrado')
        exit(1)
    repos_raw = r1.read().decode("utf-8")
    connection.close()



    repos= json.loads(repos_raw)

    for elemento in range (len(repos['results'])):
        info_medicamento=repos['results'][elemento]

        if not (info_medicamento['openfda']):#si existe la opción 'openfda' entonces imprimir el fabricante.
            print('- El fabricante del medicamento',elemento+1,'no precisa')#Si no presenta esa opción se impimirá dicho mensaje.
            continue
        print('- El fabricante de ',info_medicamento['openfda']['generic_name'][0],'es ',info_medicamento['openfda']['manufacturer_name'][0])

    # Utilizamos la opción search= active_ingredient como dice openFDA para encontrar todos aquellos medicamentos que presenten el acetilsalycilic
    # Imponemos un limit= 100 puesto que la página no admite mostrar más de 100 medicamentos.

    if (len(repos['results']))<100:
        break

    skip=skip+100

#Para poder acceder a todos los fabricantes y no tener problemas con el limit=100 utilizamos skip.
#Realizamos un bucle infinito en el que el valor de skip irá cambiando. Así pues, en la primera vuelta no nos saltaremos ningun valor.
#En la segunda si la longitud de la lista es mayor que 100 o igual entonces se saltará los 100 pimeros medicamentos y así sucesivamente.
#En el caso en el que la longitud sea menor que 100 entonces saldrá del bucle e imprimiremos los fabricantes que quedan