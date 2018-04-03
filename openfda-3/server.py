import http.server
import socketserver
import http.client
import json

PORT = 8004
def add_medicamento():#creamos una función que actúe de cliente.
    lista_medicamentos=[]#abrimos una lista en la que introduciremos el contenido de medicamentos pedido
    headers = {'User-Agent': 'http-client'}
    connection = http.client.HTTPSConnection("api.fda.gov")
    connection.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = connection.getresponse()
    repos_raw = r1.read().decode("utf-8")
    connection.close()
    repos = json.loads(repos_raw)
    for elemento in range(len(repos['results'])):#recorro la lista de 'results' (teniendo 10 posiciones)
        info_medicamento = repos['results'][elemento]
        if  (info_medicamento['openfda']):#si existe añadiremos el nombre genérico del medicamento
            lista_medicamentos.append(info_medicamento['openfda']['generic_name'][0])
    return lista_medicamentos

#Aplicaremos herencia
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):#aplicaremos un método
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        lista=add_medicamento()#introducimos en la variable lista lo obtenido en la función
        content = "<html><body><ol>"#creamos el html
        content += "<h1>" + 'El listado de medicamentos pedido es el siguiente: ' + "</h1>"
        for medicamento in lista:#recorro la lista donde se han añadido los medicamentos.
            content+="<li>"+medicamento+'</li>'#creamos una lista en html.
        content+="</ol></body></html>"
        self.wfile.write(bytes(content,'utf8'))
        return



Handler = testHTTPRequestHandler#objeto Handler que llevará a cabo lo que hemos aplicado en la clase
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.close()

