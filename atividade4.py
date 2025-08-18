import numpy as np
from abc import ABC, abstractmethod

class Grafo(ABC):
    @abstractmethod
    def numero_de_vertices(self):
        pass

    @abstractmethod
    def numero_de_arestas(self):
        pass

    @abstractmethod
    def sequencia_de_graus(self):
        pass

    @abstractmethod
    def adicionar_aresta(self, u, v):
        pass

    @abstractmethod
    def remover_aresta(self, u, v):
        pass

    @abstractmethod
    def imprimir(self):
        pass

class GrafoDenso(Grafo):
    def __init__(self, vertices):
        self.vertices_labels = []
        if isinstance(vertices, list):
            self.vertices_labels = vertices
            self.num_vertices = len(vertices)
            self.label_to_index = {label: i for i, label in enumerate(vertices)}
        elif isinstance(vertices, int):
            self.num_vertices = vertices
            self.vertices_labels = [str(i) for i in range(vertices)]
            self.label_to_index = {label: i for i, label in enumerate(self.vertices_labels)}
        else:
            raise TypeError("Vértices deve ser uma lista de rótulos ou um número inteiro.")

        self.matriz_adjacencia = np.zeros((self.num_vertices, self.num_vertices), dtype=int)

    def numero_de_vertices(self):
        return self.num_vertices

    def numero_de_arestas(self):
        count = 0
        for i in range(self.num_vertices):
            for j in range(i, self.num_vertices):
                count += self.matriz_adjacencia[i, j]
        return count

    def sequencia_de_graus(self):
        return [sum(row) for row in self.matriz_adjacencia]

    def adicionar_aresta(self, u, v):
        if u not in self.label_to_index or v not in self.label_to_index:
            print("Erro: um ou mais vértices não existem no grafo.")
            return

        u_idx = self.label_to_index[u]
        v_idx = self.label_to_index[v]

        if self.matriz_adjacencia[u_idx, v_idx] == 0:
            self.matriz_adjacencia[u_idx, v_idx] = 1
            self.matriz_adjacencia[v_idx, u_idx] = 1
            print(f"Aresta adicionada entre {u} e {v}.")
        else:
            print(f"Aresta entre {u} e {v} já existe.")

    def remover_aresta(self, u, v):
        if u not in self.label_to_index or v not in self.label_to_index:
            print("Erro: um ou mais vértices não existem no grafo.")
            return

        u_idx = self.label_to_index[u]
        v_idx = self.label_to_index[v]

        if self.matriz_adjacencia[u_idx, v_idx] == 1:
            self.matriz_adjacencia[u_idx, v_idx] = 0
            self.matriz_adjacencia[v_idx, u_idx] = 0
            print(f"Aresta removida entre {u} e {v}.")
        else:
            print(f"Aresta entre {u} e {v} não existe.")

    def imprimir(self):
        print("Matriz de Adjacência:")
        header = " " + " ".join(self.vertices_labels)
        print(header)
        for i, label in enumerate(self.vertices_labels):
            row_str = " ".join(map(str, self.matriz_adjacencia[i]))
            print(f"{label} {row_str}")
            
if __name__ == "__main__":
    vertices = ["A", "B", "C", "D", "E"]
    grafo = GrafoDenso(vertices)
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("A", "C")
    grafo.adicionar_aresta("C", "D")
    grafo.adicionar_aresta("C", "E")
    grafo.adicionar_aresta("B", "D")
    grafo.imprimir()
    print("Número de vértices:", grafo.numero_de_vertices())
    print("Número de arestas:", grafo.numero_de_arestas())
    print("Sequência de graus:", grafo.sequencia_de_graus())
    grafo.remover_aresta("A", "C")
    grafo.imprimir()