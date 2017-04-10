#!/usr/bin/python3

import webapp
import urllib.request


class CacheApp(webapp.webApp):

	cache = {}

	def parse(self, request):
		metodo = request.split(' ')[0]
		recurso = request.split(' ')[1][1:]
		
		return(metodo, recurso)

	def process (self, NameResource):

		metodo, url_recibida= NameResource
		print('metodo: ' + metodo)
		print('url: ' + url_recibida)
	
		url = 'http://' + url_recibida
		print(url)	
		if metodo == 'GET':

			try: 
				if url in self.cache.keys():
					htmlCode = "200 OK"
					htmlBody = self.cache[url]	
				else:
			
					f = urllib.request.urlopen(url)
					cuerpo = f.read().decode('utf-8')
					self.cache[url] = cuerpo
					busca_inicio = cuerpo.find("<body")
					busca_fin = cuerpo.find(">",busca_inicio)
					html = "<p><a href=" + url + ">Página original</a></p>" +\
							"<p><a href=" + url_recibida + ">Recargar</a></p>" +\
							"<p><a href=" + str(self.cache) + ">Cache</a></p>"
					htmlCode = "200 OK"
					htmlBody = str(cuerpo[:busca_fin + 1] + html + cuerpo[busca_fin + 1:])
			except urllib.error.URLError:
				htmlCode = "404 Not Found"
				htmlBody = "No URL"
			except UnicodeDecodeError:
				htmlCode = "404 Not Found"
				htmlBody = "<html><body>Decode Error. Can not show the site</body></html>"
			except IndexError:
				htmlCode = "404 Not Found"
				htmlBody = "Index Error"
		else:
			htmlCode = "405 Method not allowed"
			htmlBody = "Metodo no permitido"
			
		return(htmlCode, htmlBody)
			
			

if __name__ == "__main__":
	try:
		testWebApp = CacheApp("localhost", 1234)	
	except KeyboardInterrupt:
		print("End")
