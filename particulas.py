from particula import Particula
import json
from pprint import pformat
from pprint import pprint
from collections import deque

# Administrador de Particulas

class Particulas:
    def __init__(self):
        self.__particulas = [] # Lista
    
    def agregar_inicio(self, particula:Particula):
        self.__particulas.insert(0, particula)

    def agregar_final(self, particula:Particula):
        self.__particulas.append(particula)
    
    def mostrar(self):
        for particula in self.__particulas:
            print(particula)

    def __str__(self):
        return "".join(
            str(particula) + "\n" for particula in self.__particulas
        )

    def dictionary(self,grafo):

        for particula in self.__particulas:
            key = (particula.origen_x, particula.origen_y) 
            value = ((particula.destino_x, particula.destino_y), particula.distancia)
            key_2 = (particula.destino_x, particula.destino_y)
            value_2 = ((particula.origen_x, particula.origen_y), particula.distancia)
            if key in grafo:
                grafo[key].append(value)
            else:
                grafo[key] = [value]
            if key_2 in grafo:
                grafo[key_2].append(value_2)
            else:
                grafo[key_2] = [value_2]
        str = pformat(grafo, width=40, indent=1)
        return str
    
    def metodo_profundidad(self, grafo, origen_x=0, origen_y=0):
        self.dictionary(grafo)
        key = (origen_x, origen_y)

        if key in grafo:
            pila = []
            visitados = []
            recorrido = []

            pila.append(key)
            visitados.append(key)

            while len(pila) > 0:
                vertice = pila[-1]
                recorrido.append(vertice)
                pila.pop()
                adyacente = grafo[vertice]
                for i in adyacente:
                    if not i[0] in visitados:
                        visitados.append(i[0])
                        pila.append(i[0])
            return recorrido
        else:
            return 0

    def metodo_amplitud(self, grafo, origen_x=0, origen_y=0):
        self.dictionary(grafo)
        key = (origen_x, origen_y)

        if key in grafo:
            cola = deque()
            visitados = []
            recorrido = []

            cola.appendleft(key)
            visitados.append(key)

            while len(cola) > 0:
                vertice = cola[-1]
                recorrido.append(vertice)
                cola.pop()
                adyacente = grafo[vertice]
                for i in adyacente:
                    if not i[0] in visitados:
                        visitados.append(i[0])
                        cola.appendleft(i[0])
            return recorrido
        else:
            return 0

    def __len__(self):
        return len(self.__particulas)
    
    def __iter__(self):
        self.contador = 0

        return self
    
    def __next__(self):
        if self.contador < len(self.__particulas):
            particula = self.__particulas[self.contador]
            self.contador += 1
            return particula
        else:
            raise StopIteration
    
    def guardar(self, ubicacion):
        try:
            with open(ubicacion, "w") as archivo:
                Lista = [particula.to_dict() for particula in self.__particulas]
                json.dump(Lista, archivo, indent=5)
            return 1
        except:
            return 0
    
    def abrir(self, ubicacion):
        try:
            with open(ubicacion, "r") as archivo:
                Lista = json.load(archivo)
                self.__particulas = [Particula(**particula) for particula in Lista]
            return 1
        except:
            return 0