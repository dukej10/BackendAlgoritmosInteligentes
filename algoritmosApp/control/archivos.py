from io import BytesIO
import os
import json
from xml.dom import minidom
import urllib.request
import xml.etree.cElementTree as e

#librerias para trabajar con PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import xlsxwriter
from urllib.request import urlopen

class archivosControl():
	def getExtensionFile(path):
		root, extension = os.path.splitext(path)
		return extension

	def xmlToJson(address):
		#file = minidom.parse(address)

		with urllib.request.urlopen(address) as url:
			archivo = url.read()
			codificado = archivo.decode("utf-8")
			file = minidom.parseString(codificado) 

		name = file.getElementsByTagName("grafoId")[0]
		grafoId =  int(name.firstChild.data)

		#name = file.getElementsByTagName("grafoName")[0]
		#grafoName = name.firstChild.data
		grafoName = "grafo "+str(grafoId)

		nodos = []
		links = []

		node = file.getElementsByTagName("node")
		for n in node:
			id = n.getElementsByTagName("id")[0]
			name = n.getElementsByTagName("name")[0]
			label = n.getElementsByTagName("label")[0]
			data = n.getElementsByTagName("data")[0]
			tipo = n.getElementsByTagName("type")[0]
			radius = n.getElementsByTagName("radius")[0]
			coordenates = n.getElementsByTagName("coordenates")[0]

			nodo = {
		      "id": int(id.childNodes[0].data),
		      "name": name.childNodes[0].data,
		      "label": label.childNodes[0].data,
		      "data": data.childNodes[0].data,
		      "type": None,
		      "radius": float(radius.childNodes[0].data),
		      "coordenates": None
			}

			nodos.append(nodo)

		link = file.getElementsByTagName("link")
		for l in link:
		  	source = l.getElementsByTagName("source")[0]
		  	target = l.getElementsByTagName("target")[0]
		  	distance = l.getElementsByTagName("distance")[0]

		  	arista = {
		      "source": int(source.childNodes[0].data),
		      "target": int(target.childNodes[0].data),
		      "distance": int(distance.childNodes[0].data)
		  	}

		  	links.append(arista)

		grafo = {
		    "grafoId": grafoId,
		    "grafoName": grafoName,
		    "nodes": nodos,
		    "links": links
		}
		
		return grafo

	def jsonToXML(d):
		r = e.Element("Graph")

		e.SubElement(r,"grafoId").text = str(d["grafoId"])                      # Edit the element's tail
		e.SubElement(r,"grafoName").text = str(d["grafoName"])

		nodes = e.SubElement(r,"nodes")
		links = e.SubElement(r,"links")

		for z in d["nodes"]:
		    nodo = e.SubElement(nodes,"node")
		    e.SubElement(nodo,"id").text = str(z["id"])
		    e.SubElement(nodo,"name").text = z["name"]
		    e.SubElement(nodo,"label").text = z["label"]
		    e.SubElement(nodo,"data").text = z["data"]
		    e.SubElement(nodo,"type").text = z["type"]
		    e.SubElement(nodo,"radius").text = str(z["radius"])
		    e.SubElement(nodo,"coordenates").text = str(z["coordenates"])

		for z in d["links"]:
		    link = e.SubElement(links,"link")
		    e.SubElement(link,"source").text = str(z["source"])
		    e.SubElement(link,"target").text = str(z["target"])
		    e.SubElement(link,"distance").text = str(z["distance"])

		a = e.ElementTree(r)
		xmlstr = (minidom.parseString(e.tostring(r)).toprettyxml(indent = "   "))
		return xmlstr

	def grafoToPDF(address):
		try:
			w, h = A4
			c = canvas.Canvas("././media/pdf/imagen.pdf", pagesize=(2034,1051))
			text = c.beginText(20,40)
			text.setFont("Courier", 18)
			text.setFillColor(colors.red)
			text.textLine("Grafo")
			c.drawText(text)
			img = ImageReader(address)
			img_w, img_h = img.getSize()
			#c.drawString(0, 0, "¡Hola, mundo!")
			c.drawImage(img, 20, 80, width=2034, height=500, mask='auto')
			c.save()

			direccion = {
				"link": "http://localhost:8000/media/pdf/imagen.pdf"
			}

			return direccion
		except ValueError:
			print("Oops!  problemas generando el pdf.  Try again...")

	def graphToExcel(address):
		try:
			print("IMAGEN ", address)
			workbook = xlsxwriter.Workbook('././media/excel/image.xlsx')
			worksheet = workbook.add_worksheet()
			#Widen the first column to make the text clearer.
			worksheet.set_column('A:A', 30)
			#Insert an image.
			worksheet.write('A1', 'Grafo')
			image_data = BytesIO(urlopen(address).read())
			print(image_data)
			worksheet.insert_image('A1', address, {'image_data': image_data})
			workbook.close()
			direccion = {
				"link": "http://localhost:8000/media/excel/image.xlsx"
			}
			return direccion
		except ValueError:
			print("Oops!  problemas generando el csv.  Try again...")