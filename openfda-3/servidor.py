import http.server
import socketserver
import http.client
import json

PORT = 8004


#Aplicaremos herencia
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):#aplicaremos un método
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content = "<html><body><ul>"#creamos el html
        content += "<h1>" + 'El listado de medicamentos pedido es el siguiente: ' + "</h1>"
        
        content+="</ul></body></html>"
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