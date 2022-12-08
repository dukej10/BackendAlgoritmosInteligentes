from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pyrsistent import T
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import numpy as np
from algoritmosApp.models import Graphs
from algoritmosApp.serializers import GrafoSerializer
import time
import networkx as nx
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
import urllib.request
import json
import random
import algoritmosApp.control.eight_puzzle as ep
import algoritmosApp.control.a_estrella as a_e
from datetime import datetime

#from algoritmosApp.Control.algorithms import inicializar
#from algoritmosApp.Control.archivos import archivosControl
#from algoritmosApp.Control.algorithms import inicializarCluster

def clustering(request, id=0):
    cantidad_clusters = JSONParser().parse(request)
    nclusters = int(cantidad_clusters["ncluster"])
    #print("LLEGÓ ", nclusters)
    graphs = Graphs.objects.get(grafoId=id)
    grafos_serializer = GrafoSerializer(graphs, many=False)

    nodos = []
    aristas = []

    grafo =  grafos_serializer.data

    nodes = grafo["nodes"]
    links = grafo["links"]

    for client in nodos:
        if client["id"] not in nodes:
          nodos.append(client["id"])

    for client in links:
        dictD = (client["source"],client["target"])
        aristas.append(dictD)

    G=nx.Graph()
    G.add_nodes_from(nodos)
    G.add_edges_from(aristas)
    #A = nx.adjacency_matrix(G)
    print("/")
    print("/")
    print("/")
    arr = nx.to_numpy_array(G)
    print("NCLUSTER ", nclusters)
    print("ADYACENCIAS ", arr)
    tiempoInicio = time.time()
    clusters = inicializarCluster(arr, nclusters)
    tiempoTotal = time.time() - tiempoInicio
    nodos = list(G.nodes)
    print("")
    print("")
    print("")
    index = []
    listas =[]
    for clave, valor in clusters.items():  
        for posicion in valor:
            index.append(nodos[posicion])
        listas.append(index)
        index = []
        
    print("Listas ", listas)
    print("CLUSTER")
    print(clusters)
    print("")
    print("")
    print("")
    grafo = Graphs(grafoName= id+ " C", nodes=nodes, links=links)
    k = 0
    aux = None
    aristas = []
    for i in listas:
        k = 0
        print("CLUSTER ", i)
        #print("CANTIDAD ARISTAS ", len(grafo.links))
        while k < len(grafo.links):
                if grafo.links[k]["source"] in i and grafo.links[k]["target"] in i:
                    print("Aristas ",grafo.links[k])
                    aristas.append(grafo.links[k])
                k = k+1
    #print("LINKS ", aristas)
    indice = 0
    for clave in clusters.keys():
        clusters[clave] = listas[indice]
        indice = indice +1
        
    return JsonResponse({ "grafoId": grafo.grafoId,
                         "nodes": nodes,
                         "links": aristas,
        "tiempo": tiempoTotal,
                         "segmentos": str(clusters)}, safe=False)

def queyrannne(request, id=0):
    graphs = Graphs.objects.get(grafoId=id)
    grafos_serializer = GrafoSerializer(graphs, many=False)

    nodos = []
    aristas = []

    grafo =  grafos_serializer.data

    nodes = grafo["nodes"]
    links = grafo["links"]

    for client in nodos:
        if client["id"] not in nodes:
          nodos.append(client["id"])

    for client in links:
        dictD = (client["source"],client["target"])
        aristas.append(dictD)

    G=nx.Graph()
    G.add_nodes_from(nodos)
    G.add_edges_from(aristas)
    #A = nx.adjacency_matrix(G)
    arr = nx.to_numpy_array(G)
    tiempoInicio = time.time()
    segmentos = inicializar(arr)
    tiempoTotal = time.time() - tiempoInicio
    cortar = segmentos[len(segmentos)-1] # nodo a cortar
    #print("NODOS ", G.nodes)
    nodos = list(G.nodes)
    posicion = cortar[0]
    nodocort = nodos[posicion-1]
    lista = list(segmentos)
    print("TENGO ", segmentos)
    print("TENGO ", lista[0])
    text = "("
    for i in lista[0]:
        print(i)
        text+= str(nodos[i-1]) +", "
    text+="), ("
    #print("TEXTO ", text)
    for i in lista[1]:
        text+= str(nodos[i-1]) +", "
    text+=")"
    print("YA ", text)
    print("NODO CORTAR ", nodocort)
    print("TIEMPO ", tiempoTotal)
    
    k = 0
    aux = None
    grafo = Graphs(grafoName= id+ " Q", nodes=nodes, links=links)
    #print("TAMAÑO NODOS", len(grafo.nodes))
    while k < len(grafo.links):
            if grafo.links[k]["source"] == nodocort or grafo.links[k]["target"] == nodocort:
                aux = grafo.links[k]
            if aux is not None:
                grafo.links.remove(aux)
            k = k+1
    return JsonResponse({ "grafoId": grafo.grafoId,
                         "nodes": grafo.nodes,
                         "links": grafo.links,
        "tiempo": tiempoTotal,
                         "segmentos": text}, safe=False)


def export_matriz(request, id = 0):
    graphs = Graphs.objects.get(grafoId=id)
    grafos_serializer = GrafoSerializer(graphs, many=False)

    nodos = []
    aristas = []

    grafo =  grafos_serializer.data

    nodes = grafo["nodes"]
    
    links = grafo["links"]

    for client in nodos:
        if client["id"] not in nodes:
          nodos.append(client["id"])

    for client in links:
        dictD = (client["source"],client["target"])
        aristas.append(dictD)

    G=nx.Graph()
    G.add_nodes_from(nodos)
    G.add_edges_from(aristas)
    print("NODOS ", G.nodes)
    A = nx.adjacency_matrix(G)
    arr = nx.to_numpy_array(G)
    rows = arr.shape[0]
    cols = arr.shape[1]
    # print("")
    # print("")
    # print("")
    print("//XX")
    # print(arr)
    # print("")
    # print("")
    # print("")
    # #print(arr)
    # print("SSSS")   

    return JsonResponse("funciona", safe=False)

def export_xml(request, id=0):
    graphs = Graphs.objects.get(grafoId=id)
    grafos_serializer = GrafoSerializer(graphs, many=False)

    d = grafos_serializer.data
    xmlstr = archivosControl.jsonToXML(d)

    with open("./media/xml_export/json_to_xml_"+str(graphs.grafoId)+".xml", "w") as f:
        f.write(xmlstr)

    info = {
        "grafoId": graphs.grafoId,
        "link": "http://127.0.0.1:8000/media/xml_export/json_to_xml_"+str(graphs.grafoId)+".xml"
    }

    return JsonResponse(info, safe=False)


def random_graph(request):
    grafo_data = JSONParser().parse(request)
    print(grafo_data)
    cantidad_nodos = int(grafo_data['cant_nodos'])
    cantidad_aristas = int(grafo_data['cant_aristas'])

    nodos = []
    links = []
    nodos_id = []
    combinaciones = []

    for i in range(1, cantidad_nodos+1):
        nodos_id.append(i)
        nodo = {
            "id": i,
            "name": "Nodo "+str(i),
            "label": "N"+str(i),
            "data": "{}",
            "type": "",
            "radius": 12,
            "coordenates": None
        }

        nodos.append(nodo)
    aux = cantidad_aristas
    while len(combinaciones) < cantidad_aristas:
        combinacion = random.choices(nodos_id, k=2)
        if combinacion[0] != combinacion[1]:
            if [combinacion[0], combinacion[1]] not in combinaciones and [combinacion[1], combinacion[0] not in combinaciones]:
                combinaciones.append(combinacion)
                #print("COMBINACION ssss ", len(combinaciones))

    for i in combinaciones:
        link = {
            "source": i[0],
            "target": i[1],
            "distance": random.randint(1, 200)
        }
        links.append(link)

    grafoName = "Random"+str(format(datetime.now()))

    grafo = Graphs(grafoName=grafoName, nodes=nodos, links=links)
    grafo.save()

    grafos_serializer = GrafoSerializer(grafo, many=False)
    return JsonResponse(grafos_serializer.data, safe=False)


def img_upload(request):
    myfile = request.FILES['myfile']
    print(myfile)
    fs = FileSystemStorage()
    filename = fs.save(myfile.name+".jpg", myfile)
    upload_file_url = fs.url(filename)

    link_servidor = "http://localhost:8000"
    direccion = str(link_servidor+str(upload_file_url))
    print(direccion)
    resultado = archivosControl.grafoToPDF(direccion)

    return JsonResponse(resultado, safe=False)


def img_ex(request):
    myfile = request.FILES['myfile']
    print(myfile)
    fs = FileSystemStorage()
    filename = fs.save(myfile.name+".jpg", myfile)
    upload_file_url = fs.url(filename)

    link_servidor = "http://localhost:8000"
    direccion = str(link_servidor+str(upload_file_url))
    print(direccion)
    resultado = archivosControl.graphToExcel(direccion)

    return JsonResponse(resultado, safe=False)


def simple_upload(request):
    myfile = request.FILES['myfile']
    print(myfile)
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    upload_file_url = fs.url(filename)

    link_servidor = "http://localhost:8000"
    direccion = str(link_servidor+str(upload_file_url))

    data = None

    if archivosControl.getExtensionFile(direccion) == '.json':
        with urllib.request.urlopen(direccion) as url:
            s = url.read()
            my_json = s.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            print(type(data))

    elif archivosControl.getExtensionFile(direccion) == '.xml':
        data = archivosControl.xmlToJson(direccion)
        #data = json.dumps(s)
        print(data)

    data['grafoName'] = 'grafo ' + str(data['grafoId'])

    if data['grafoId'] != None and data['grafoName'] != None:
        grafo = Graphs(grafoName=data['grafoName'],
                       nodes=data['nodes'], links=data['links'])
        grafo.save()

        grafos_serializer = GrafoSerializer(grafo, many=False)
        return JsonResponse(grafos_serializer.data, safe=False)

# Create your views here.


def algoritmo_estrella(request):
    grafo_data = JSONParser().parse(request)
    estado_inicial = grafo_data['inicial']
    estado_objetivo = grafo_data['objetivo']
    estado_inicial = estado_inicial.split(",")
    estado_objetivo = estado_objetivo.split(",")
    #print(estado_inicial)
    X = ep.HUECO
    for num in estado_inicial:
        if(num == "X"):
            num = X
    print(estado_inicial)
    for num in estado_objetivo:
        if(num == "x"):
            num = X
            print("CAMBIAR")
    print(estado_objetivo)
    estado0 = ((
        (int(estado_inicial[0]), int(estado_inicial[1]), int(estado_inicial[2])),
        (int(estado_inicial[3]), int(estado_inicial[4]), int(estado_inicial[5])),
        (int(estado_inicial[6]), int(estado_inicial[7]), int(estado_inicial[8])),
    ))
    

    estadoF = ((
        (int(estado_objetivo[0]), int(estado_objetivo[1]), int(estado_objetivo[2])),
        (int(estado_objetivo[3]), int(estado_objetivo[4]), int(estado_objetivo[5])),
        (int(estado_objetivo[6]), int(estado_objetivo[7]), int(estado_objetivo[8])),
    ))
    # ep.graficar_estado(estado0)
    ruta = a_e.buscar_con_a_estrella(estado0, ep.gen_estados_alcanzables,
                                 heuristica=ep.dist_hamming)
    lista = {}
    lista = {"movimientos": _formatoRuta(ruta)}
    ep.graficar_ruta(ruta)
    print(f'Solución de {len(ruta)} pasos')
    print(estado0)
    print(estadoF)
    return  JsonResponse(lista, safe=False)

def _formatoRuta(ruta):
    lista_movimientos = []
    movimiento_aux = []
    text_mov = ""
    text_aux = ""
    lista_aux = list(ruta)
    # print(lista)
    for i in range(len(lista_aux)):
        text_aux = str(lista_aux[i]).replace("(", "").replace(")", "") +";"
        text_mov += text_aux

    movimiento_aux = text_mov.split(";")
    print("MOVIMIENTOS")
    print(text_mov)
    print("MOVS")
    for i in movimiento_aux:
        if i != "":
            lista_movimientos.append(i)
    print(lista_movimientos)
    return lista_movimientos


@csrf_exempt
def graphApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            graphs = Graphs.objects.all()
            grafos_serializer = GrafoSerializer(graphs, many=True)
            return JsonResponse(grafos_serializer.data, safe=False)
        elif id != 0 and id != None:
            graphs = Graphs.objects.get(grafoId=id)
            grafos_serializer = GrafoSerializer(graphs, many=False)
            #print("Grafo ", grafos_serializer.data)
            return JsonResponse(grafos_serializer.data, safe=False)

    elif request.method == 'POST':
        grafo_data = JSONParser().parse(request)
        grafos_serializer = GrafoSerializer(data=grafo_data)
        if grafos_serializer.is_valid():
            grafos_serializer.save()

            graphs = Graphs.objects.all()
            grafo_serializer = GrafoSerializer(graphs, many=True)
            return JsonResponse(grafo_serializer.data, safe=False)

        return JsonResponse("fallo el añadido", safe=False)

    elif request.method == 'PUT':
        print("PETICION PUT")
        grafo_data = JSONParser().parse(request)
        grafo = Graphs.objects.get(grafoId=grafo_data['grafoId'])
        # print(grafo_data)
        if grafo_data['tarea'] == "back":
            grafo.nodes = grafo_data["nodes"]
            grafo.links = grafo_data["links"]
        if grafo_data['tarea'] == "reset":
            #print("Llegó ", grafo_data)
            grafo.nodes = grafo_data["nodes"]
            grafo.links = grafo_data["links"]
        if grafo_data['tarea'] == "addNode":
            exist = False
            i = 0
            while i < len(grafo.nodes) and exist is False:
                if grafo.nodes[i]["id"] == grafo_data["id"]:
                    exist = True
                i = i + 1
            if exist is False:
                grafo.nodes.append({"id": grafo_data["id"],
                                    "name": "Nodo "+str(grafo_data["id"]),
                                    "label": "N"+str(grafo_data["id"]),
                                    "data": {},
                                    "type": "",
                                    "radius": grafo_data["radius"],
                                    "coordenates": None
                                    })
        elif grafo_data['tarea'] == "updateNode":
            i = 0
            changed = False
            while i < len(grafo.nodes) and changed is False:
                if grafo.nodes[i]["id"] == grafo_data["id"]:
                    if "name" in grafo_data:
                        grafo.nodes[i]["name"] = grafo_data["name"]
                        changed = True
                    if "label" in grafo_data:
                        grafo.nodes[i]["label"] = grafo_data["label"]
                        changed = True
                    if "radius" in grafo_data and grafo_data["radius"] > 0:
                        grafo.nodes[i]["radius"] = grafo_data["radius"]
                        changed = True
                    if "data" in grafo_data:
                        grafo.nodes[i]["data"] = grafo_data["data"]
                        changed = True
                    if "type" in grafo_data:
                        grafo.nodes[i]["type"] = grafo_data["type"]
                        changed = True
                    if "coordenates" in grafo_data:
                        grafo.nodes[i]["coordenates"] = grafo_data["coordenates"]
                        changed = True
                i = i+1
        elif grafo_data['tarea'] == "addLinks":
            #print("Llegó ", grafo_data)
            exist = False
            i = 0
            cont = 0
            while i < len(grafo.nodes) and cont < 2:  # comprobar que sea nodos existentes
                if grafo_data["source"] == grafo.nodes[i]["id"]:
                    cont = cont + 1
                if grafo_data["target"] == grafo.nodes[i]["id"]:
                    cont = cont + 1
                i = i + 1
            #print("	nodos ", cont)
            if cont == 2:  # los nodos existen
                i = 0
                while i < len(grafo.links) and exist is False:
                    if grafo.links[i]["source"] == grafo_data["source"] and grafo.links[i]["target"] == grafo_data["target"]:
                        exist = True
                    i = i + 1
                if exist is False:  # la arista no existe
                    grafo.links.append({"source": grafo_data["source"],
                                        "target": grafo_data["target"],
                                        "distance": grafo_data["distance"]})

        if grafo_data['tarea'] == "updateLink":
            if "distance" in grafo_data:
                k = 0
                changed = False
                while k < len(grafo.links) and changed is False:
                    if grafo.links[k]["source"] == grafo_data["source"] and grafo.links[k]["target"] == grafo_data["target"]:
                        #print(grafo.links[k]["source"], " / ", grafo.links[k]["target"])
                        grafo.links[k]["distance"] = grafo_data["distance"]
                        changed = True
                    k = k + 1

        if grafo_data['tarea'] == "removeLink":
            k = 0
            removed = False
            aux = None
            while k < len(grafo.links) and removed is False:
                if grafo.links[k]["source"] == grafo_data["source"] or grafo.links[k]["target"] == grafo_data["target"]:
                    aux = grafo.links[k]
                    removed = True
                k = k+1
            if aux is not None:
                grafo.links.remove(aux)
        if grafo_data['tarea'] == "removeNode":
            aux = None
            i = 0
            j = 0
            auxL = []
            while i < len(grafo.nodes) and aux is None:
                # print(grafo.nodes[i]["id"])
                if grafo.nodes[i]["id"] == grafo_data["id"]:
                    aux = grafo.nodes[i]
                    # print(aux)
                i = i + 1
            if aux is not None:
                grafo.nodes.remove(aux)
            #print("TAMAÑO ",len(grafo.links))
            while j < len(grafo.links):
                print(grafo.links[j]["target"])
                if grafo.links[j]["source"] == grafo_data["id"] or grafo.links[j]["target"] == grafo_data["id"]:
                    #print("entró ",grafo.links[j])
                    auxL.append(grafo.links[j])
                j = j+1
            if len(auxL) > 0:
                for el in auxL:
                    grafo.links.remove(el)
        grafo.save()
        grafos_serializer = GrafoSerializer(grafo, many=False)
        #print("RESPUESTA ", grafos_serializer)
        return JsonResponse(grafos_serializer.data, safe=False)

    elif request.method == 'DELETE':
        grafo = Graphs.objects.get(grafoId=id)
        grafo.delete()
        graphs = Graphs.objects.all()
        grafo_serializer = GrafoSerializer(graphs, many=True)
        return JsonResponse(grafo_serializer.data, safe=False)
