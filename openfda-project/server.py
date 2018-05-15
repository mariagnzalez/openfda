import http.server
import http.client
import json
import socketserver


PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):#Aplicamos herencia

    def add_web(self,lista):# función que realiza la pagina web

        list_html = "<html><head><title>OpenFDA App</title></head><body><ul>"
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += "</ul></body></html>"
        return list_html

    def add_conn(self,limit):# función que establece conexión
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit="+str(limit)+self.recurso+ self.parameter,None,headers)
        r1= conn.getresponse()
        repos_raw = r1.read().decode("utf8")
        repos = json.loads(repos_raw)
        return repos

    def formulario(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA App </h1>
                    <h4>Welcome to the OpenFDA application</h4>
                    <form method="get" action="listDrugs">
                        <u>Drug list:</u> <br>
                        Limit: <input type='text' name="limit"></input>
                        <input type = "submit" value="submit">
                        </input>
                    </form>
                    <br>
                    <form method="get" action="listCompanies">
                        <u>List Company: </u><br>
                        Limit: <input type='text' name="limit"></input>
                        <input type = "submit" value="submit">
                        </input>
                    </form>
                    <br>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <br>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <br>
                    <form method="get" action="listWarnings">
                        <u>List Warnings: </u><br>
                        Limit: <input type='text' name="limit"></input>
                        <input type= "submit" value="submit">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html


    def do_GET(self):#Aplicamos sobrescritura.
                                                   # para poder calcular el limite:
        recurso_list = self.path.split("?")        # separamos el recurso por la interrogacion para asi tener por un lado la parte del limit y la otra
        if len(recurso_list) > 1:                  # si tiene posiciones mayores que 1 hay mas parametros.
            parametros = recurso_list[1]           # Nos quedaremos con la parte del limit
        else:
            parametros = ""

        limit=1                                 # si no hay limit se tomará por defecto el limit=1.

        if parametros:

            parte_limit = parametros.split("=")

            if parte_limit[0] == "limit":# nos aseguramos que la parte del igual no es de un 'search'.

                if not(parte_limit[1].isdigit()):#En el caso de que el cliente ponga en el campo del limit un valor no numerico cogerá por defecto limit=1
                    print('ERROR, el campo de limit debe de ser un numero')#De esta forma no saldrá una excepción si utiliza un valor no correcto.

                elif int(parte_limit[1])>100 or int(parte_limit[1])==0: #si el limite no cumple lo establecido cogería por defecto limit=1
                                                                      #De esta forma no saldrá una excepción si utiliza otro limite no correcto.
                    print('ERROR, el limit debe estar entre 1 y 100')

                else:
                    limit = int(parte_limit[1])



        if self.path=='/': #Formulario

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html=self.formulario()#llamada a la función del formulario
            self.wfile.write(bytes(html, "utf8"))


        elif 'listDrugs' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.recurso=''
            self.parameter=''
            repos=self.add_conn(limit) #llamada a la función que establece conexión.

            medicamentos= []
            for elemento in range(len(repos['results'])):
                info_medicamento = repos['results'][elemento]

                if info_medicamento['openfda']:
                    medicamentos.append(info_medicamento['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')

            list_html=self.add_web(medicamentos)#llamada a la funcion que realiza la pagina web.
            self.wfile.write(bytes(list_html, "utf8"))


        elif 'listCompanies' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.recurso = ''
            self.parameter = ''
            repos = self.add_conn(limit)

            companies = []
            for elemento in range(len(repos['results'])):
                info_medicamento = repos['results'][elemento]

                if info_medicamento['openfda']:
                    companies.append(info_medicamento['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocida')

            list_html=self.add_web(companies)
            self.wfile.write(bytes(list_html, "utf8"))


        elif  'searchDrug' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drug=self.path.split('=')[1] #separamos el recurso por la parte que es '=' para quedarnos con el medicamento
            self.recurso="&search=active_ingredient:"
            self.parameter=drug
            limit=10
            repos=self.add_conn(limit)

            li_drug=[]
            for elemento in range(len(repos['results'])):
                info_medicamento = repos['results'][elemento]

                if info_medicamento['openfda']:
                    li_drug.append(info_medicamento['openfda']['generic_name'][0])

                else:
                    li_drug.append('Desconocido')

            list_html = self.add_web(li_drug)
            self.wfile.write(bytes(list_html, "utf8"))


        elif 'searchCompany' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            company=self.path.split('=')[1]
            self.recurso="&search=openfda.manufacturer_name:"
            self.parameter=company
            limit=10
            repos=self.add_conn(limit)

            li_company = []
            for elemento in range(len(repos['results'])):
                info_medicamento = repos['results'][elemento]

                if info_medicamento['openfda']:
                    li_company.append(info_medicamento['openfda']['manufacturer_name'][0])

                else:
                    li_company.append('Desconocido')

            list_html = self.add_web(li_company)
            self.wfile.write(bytes(list_html, "utf8"))


        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.recurso=''
            self.parameter=''
            warnings = []
            repos= self.add_conn(limit)

            for elemento in range(len(repos['results'])):
                info_medicamento = repos['results'][elemento]

                if ("warnings" in info_medicamento):
                    warnings.append(info_medicamento['warnings'][0])

                else:
                    warnings.append('Desconocido')

            list_html= self.add_web(warnings)
            self.wfile.write(bytes(list_html, "utf8"))


        elif 'redirect' in self.path:
            print('Redirección a la página principal')
            self.send_response(302)  #se está haciendo una redirección de una página a otra. Al ser '302' es temporal.
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()



        elif 'secret' in self.path: #Cuando el cliente utilice como recurso 'secret' se abrirá una pagina de error en la que no se encuetra autorizado.
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="My server"')
            self.end_headers()


        else:                     #este caso se dará cuando se escriba un recurso no correcto.
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Page not found '{}'.".format(self.path).encode())

        return



socketserver.TCPServer.allow_reuse_address= True


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
