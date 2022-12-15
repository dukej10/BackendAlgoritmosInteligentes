from django.shortcuts import render
# from pyrsistent import T
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import algoritmosApp.eight_puzzle as ep
import algoritmosApp.control.a_estrella as estrella
import algoritmosApp.control.anchura as anchura
import algoritmosApp.control.profundidad as profundidad
import algoritmosApp.control.primero_mejor as primero_mejor


def _inicializarEstado(estado):
    estado = ((
        (int(estado[0]), int(estado[1]), int(estado[2])),
        (int(estado[3]), int(estado[4]), int(estado[5])),
        (int(estado[6]), int(estado[7]), int(estado[8])),
    ))
    return estado

def algoritmo_estrella(request):
    grafo_data = JSONParser().parse(request)
    estado_inicial = grafo_data['inicial']
    estado_objetivo = grafo_data['objetivo']
    estado_inicial = estado_inicial.split(",")
    estado_objetivo = estado_objetivo.split(",")
    X = ep.HUECO
    print(estado_objetivo)
    
    estado0 = _inicializarEstado(estado_inicial)
    estadoF = _inicializarEstado(estado_objetivo)
    ruta, num= estrella.buscar_estrella(estado0, estadoF,ep.gen_estados_alcanzables,
                                 heuristica=ep.dist_hamming)
    lista = {}
    lista = {"movimientos": _formatoRuta(ruta), "cantidad": num, "longitudSol": len(ruta)}
    print(f'Solución de {len(ruta)} pasos')
    print(estado0)
    print(estadoF)
    return  JsonResponse(lista, safe=False)

def algoritmo_anchura(request): 
    grafo_data = JSONParser().parse(request)
    estado_inicial = grafo_data['inicial']
    estado_objetivo = grafo_data['objetivo']
    estado_inicial = estado_inicial.split(",")
    estado_objetivo = estado_objetivo.split(",")
    X = ep.HUECO
    
    estado0 = _inicializarEstado(estado_inicial)
    estadoF = _inicializarEstado(estado_objetivo)
    ruta, num = anchura.buscar_en_anchura(estado0, ep.gen_estados_alcanzables,
                             ep.es_estado_objetivo, estadoF)
    lista = {}
    lista = {"movimientos": _formatoRuta(ruta),"cantidad": num, "longitudSol": len(ruta)}    
    print(f'Solución de {len(ruta)} pasos')
    return  JsonResponse(lista, safe=False)

def algoritmo_profundidad(request):
    grafo_data = JSONParser().parse(request)
    estado_inicial = grafo_data['inicial']
    estado_objetivo = grafo_data['objetivo']
    estado_inicial = estado_inicial.split(",")
    estado_objetivo = estado_objetivo.split(",")
    X = ep.HUECO
    estado0 = _inicializarEstado(estado_inicial)
    estadoF = _inicializarEstado(estado_objetivo)
    ruta, num= profundidad.buscar_en_profundidad(
        estado0, ep.gen_estados_alcanzables, ep.es_estado_objetivo, estadoF)
    lista = {}
    print(ruta)
    lista = {"movimientos": _formatoRuta(ruta),"cantidad": num, "longitudSol": len(ruta)}   
    #print(f'Solución de {len(ruta)} pasos')
    return  JsonResponse(lista, safe=False)

def algoritmo_primero(request):
    grafo_data = JSONParser().parse(request)
    estado_inicial = grafo_data['inicial']
    estado_objetivo = grafo_data['objetivo']
    estado_inicial = estado_inicial.split(",")
    estado_objetivo = estado_objetivo.split(",")
    X = ep.HUECO
    estado0 = _inicializarEstado(estado_inicial)
    estadoF = _inicializarEstado(estado_objetivo)
    ruta, num = primero_mejor.buscar_primero(estado0, ep.gen_estados_alcanzables,
                             estadoF,heuristica=ep.dist_hamming,)
    lista = {}
    lista = {"movimientos": _formatoRuta(ruta),"cantidad": num, "longitudSol": len(ruta)}    
    print(f'Solución de {len(ruta)} pasos')
    print(f'Solución de {len(ruta)} pasos')
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
