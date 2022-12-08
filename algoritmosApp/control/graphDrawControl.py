# librerias para dibujo
import networkx as nx
import matplotlib.pyplot as plt

# librerias para trabajar con json
import json
import ast

class grapDrawControl():
	def __init__(self, texto):
		self.texto = texto
		self.grafo = nx.Graph()

	def __toJson(self):
		res = json.dumps(self.texto)
		d = json.loads(res)
		res = ast.literal_eval(d)
		return res

	def __getGrafoID(self):
		return str(self.__toJson().get('grafoId'))

	def __getNodos(self):
		return ast.literal_eval(self.__toJson().get('nodos'))

	def __getAristas(self):
		aristas = self.__toJson().get('aristas')
		aristas = ast.literal_eval(aristas)
		return aristas

	def __createNodes(self, nodos):
		for nodo,posicion in nodos.items():
			self.grafo.add_node(nodo,pos=posicion)
		 
	def __createEdges(self,aristas):
		for i in aristas:
			self.grafo.add_edge(i[0],i[1])
	 
	def getImageGraph(self):
		fig = plt.figure(figsize=(10,10))
		ax = plt.subplot(111)
		ax.set_title('Grafo', fontsize=12)

		self.__createNodes(self.__getNodos())
		self.__createEdges(self.__getAristas())

		nx.draw_networkx(self.grafo,node_size=2000, node_color='yellow', font_size=16, font_weight='bold')
	
		#plt.tight_layout()
		id = self.__getGrafoID()
		imagen = plt.savefig(str("algoritmosApp/static/GrafoFinal"+id+".png"),dpi=300, bbox_inches='tight', format="PNG")
		return str("http://127.0.0.1:8000/static/GrafoFinal"+id+".png")
		#plt.show(block=False)
		#plt.close('all')