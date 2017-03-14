#!/usr/bin/python3


import webapp


class acortarApp(webapp.webApp):

#Devuelve la url con su correspondiente acortada
    def devuelveUrl(self):
        html = "</br>URLs acortadas:<ul>"
        for numero, url in enumerate(self.acortadas):
            html += "http://" + self.hostname + ":" + str(self.port) + "/" + str(numero) + " : " + url
        return html

#Trocea la petición y se queda con la acción usada, GET o POST
    def parse(self, request):
        try:
            accion = request.split(' ', 2)[0]
            recurso = request.split(' ',2)[1]
            cuerpo = request.split('\r\n\r\n', 1)[1]
        except IndexError:
                    return ("404 Not Found", "Recurso no disponible")
        return (accion, recurso, cuerpo)


    def process(self, respuesta):
        accion, recurso, cuerpo = respuesta
        
        formulario = "<form method='POST' action=''>URL: <input type='text' name='url'><br><input type='submit' value='Acortar!'></form>"

        if accion == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body>ACORTADOR DE URLs" + formulario + self.devuelveUrl() + "</body></html>"
                return (httpCode, htmlBody)
            
            else:
                numero = int(recurso[1:])
                recurso = ('http://localhost:1234' + recurso)
                if recurso in self.acortadas:
                    RETURN("307 Redirect" + "\n" + "Location: " + self.acortadas[numero], "")
                    
                else:
                    return ("404 Not Found")
                    
        elif accion == "POST":
            contenido = cuerpo.split("=")[1]

            if not contenido.startswith("http"):
                contenido = "http://" + contenido
                return contenido

            if contenido in self.acortadas:
                return ("404 Not Found", "<html><body>Esta url ya esta acortada.")
            else:
                self.acortadas.append(contenido)
                return ("200 OK", "<html><body>URL acortada para '" + contenido + "': <strong>http://" + self.hostname + ":" + str(self.port) + "/" + str(len(self.acortadas)-1) + "</body></html>")

    def __init__(self, hostname, port):
        self.acortadas = []
        self.hostname = hostname
        self.port = port
        webapp.webApp.__init__(self, hostname, port)


if __name__ == "__main__":
    acortadorurls = acortarApp("localhost", 1234)
