#Aluno: Gabrielle Arruda Rodrigues
#Matricula: 2312130129

import sys
from abc import ABC, abstractmethod
from itertools import permutations
import itertools

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

    @abstractmethod
    def is_simples(self):
        pass

    @abstractmethod
    def is_nulo(self):
        pass

    @abstractmethod
    def is_completo(self):
        pass

    @abstractmethod
    def get_vertices(self):
        pass

    @abstractmethod
    def get_arestas(self):
        pass

    @abstractmethod
    def is_subgrafo(self, outrografo):
        pass
    
    @abstractmethod
    def is_subgrafo_gerador(self, outrografo):
        pass

    @abstractmethod
    def is_subgrafo_induzido(self, grafo):
        pass

    @abstractmethod
    def is_isomorfo(self, outrografo):
        pass


class GrafoDenso(Grafo):
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.labels = labels
            self.num_vertices = len(labels)
            self.mapa_labels = {label: i for i, label in enumerate(labels)}
        elif num_vertices:
            self.num_vertices = num_vertices
            self.labels = [str(i) for i in range(num_vertices)]
            self.mapa_labels = {str(i): i for i in range(num_vertices)}
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        self.matriz = [[0] * self.num_vertices for _ in range(self.num_vertices)]

    def numero_de_vertices(self):
        return self.num_vertices

    def numero_de_arestas(self):
        count = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    count += 1
        return count

    def sequencia_de_graus(self):
        return sorted([sum(row) for row in self.matriz])

    def _obter_indice(self, vertice):
        if isinstance(vertice, str) and vertice in self.mapa_labels:
            return self.mapa_labels[vertice]
        elif isinstance(vertice, int) and 0 <= vertice < self.num_vertices:
            return vertice
        else:
            raise ValueError(f"Vértice '{vertice}' é inválido.")

    def adicionar_aresta(self, u, v):
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)
            self.matriz[idx_u][idx_v] = 1
            self.matriz[idx_v][idx_u] = 1
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v):
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)
            self.matriz[idx_u][idx_v] = 0
            self.matriz[idx_v][idx_u] = 0
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        print("\nMatriz de Adjacência:")
        header = "   " + "  ".join(self.labels)
        print(header)
        print("─" * len(header))
        for i, linha in enumerate(self.matriz):
            print(f"{self.labels[i]} |", "  ".join(map(str, linha)))
        print()

    def is_simples(self):
        for i in range(self.num_vertices):
            if self.matriz[i][i] != 0:
                return False
        return True

    def is_nulo(self):
        return self.numero_de_arestas() == 0 and self.num_vertices > 0

    def is_completo(self):
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i != j and self.matriz[i][j] == 0:
                    return False
        return True

    def get_vertices(self):
        return self.labels

    def get_arestas(self):
        arestas = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    arestas.append((self.labels[i], self.labels[j]))
        return arestas

    def is_subgrafo(self, outrografo):
        return set(self.get_vertices()).issubset(set(outrografo.get_vertices())) and \
               set(self.get_arestas()).issubset(set(outrografo.get_arestas()))

    def is_subgrafo_gerador(self, outrografo):
        return set(self.get_vertices()) == set(outrografo.get_vertices()) and \
               set(self.get_arestas()).issubset(set(outrografo.get_arestas()))

    def is_subgrafo_induzido(self, outrografo):
        if not set(self.get_vertices()).issubset(set(outrografo.get_vertices())):
            return False
        for u in self.get_vertices():
            for v in self.get_vertices():
                if u != v:
                    tem_aresta_aqui = (u, v) in self.get_arestas() or (v, u) in self.get_arestas()
                    tem_aresta_lá = (u, v) in outrografo.get_arestas() or (v, u) in outrografo.get_arestas()
                    if tem_aresta_aqui != tem_aresta_lá:
                        return False
        return True

    def is_isomorfo(self, outrografo):
        if self.numero_de_vertices() != outrografo.numero_de_vertices():
            return False
        if self.numero_de_arestas() != outrografo.numero_de_arestas():
            return False
        if self.sequencia_de_graus() != outrografo.sequencia_de_graus():
            return False

        vertices1 = list(self.get_vertices())
        vertices2 = list(outrografo.get_vertices())

        for perm in itertools.permutations(vertices2):
            mapping = dict(zip(vertices1, perm))
            if self._checa_mapeamento_preserva_adjacencia(self, outrografo, mapping):
                return True
        return False

    def _checa_mapeamento_preserva_adjacencia(self, grafo1, grafo2, mapping):
        for u in grafo1.get_vertices():
            for v in grafo1.get_vertices():
                if (u,v) in grafo1.get_arestas():
                    if (mapping[u], mapping[v]) not in grafo2.get_arestas() and \
                        (mapping[v], mapping[u]) not in grafo2.get_arestas():
                        return False
        return True


class GrafoEsparso(Grafo):
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.vertices = labels
        elif num_vertices:
            self.vertices = [str(i) for i in range(num_vertices)]
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)
        self.lista_adj = {vertice: [] for vertice in self.vertices}

    def numero_de_vertices(self):
        return len(self.vertices)

    def numero_de_arestas(self):
        return int(sum([len(vizinhos) for vizinhos in self.lista_adj.values()]) / 2)

    def sequencia_de_graus(self):
        return sorted([len(values) for values in self.lista_adj.values()])

    def _validar_vertice(self, vertice):
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True

    def adicionar_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
            if v not in self.lista_adj[u]:
                self.lista_adj[u].append(v)
            if u not in self.lista_adj[v]:
                self.lista_adj[v].append(u)
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
            if v in self.lista_adj[u]:
                self.lista_adj[u].remove(v)
            if u in self.lista_adj[v]:
                self.lista_adj[v].remove(u)
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        print("\nLista de Adjacências:")
        for vertice, vizinhos in self.lista_adj.items():
            print(f"  {vertice} -> {vizinhos}")
        print()

    def is_simples(self):
        for u, vizinhos in self.lista_adj.items():
            if u in vizinhos:
                return False
        return True

    def is_nulo(self):
        return self.numero_de_arestas() == 0 and len(self.vertices) > 0

    def is_completo(self):
        for u in self.vertices:
            for v in self.vertices:
                if u != v and v not in self.lista_adj[u]:
                    return False
        return True

    def get_vertices(self):
        return list(self.vertices)

    def get_arestas(self):
        arestas = []
        for u in self.lista_adj:
            for v in self.lista_adj[u]:
                if (v, u) not in arestas:
                    arestas.append((u, v))
        return arestas

    def is_subgrafo(self, outrografo):
        return set(self.get_vertices()).issubset(set(outrografo.get_vertices())) and \
               set(self.get_arestas()).issubset(set(outrografo.get_arestas()))

    def is_subgrafo_gerador(self, outrografo):
        return set(self.get_vertices()) == set(outrografo.get_vertices()) and \
               set(self.get_arestas()).issubset(set(outrografo.get_arestas()))

    def is_subgrafo_induzido(self, outrografo):
        if not set(self.get_vertices()).issubset(set(outrografo.get_vertices())):
            return False
        for u in self.get_vertices():
            for v in self.get_vertices():
                if u != v:
                    tem_aresta_aqui = (u, v) in self.get_arestas() or (v, u) in self.get_arestas()
                    tem_aresta_lá = (u, v) in outrografo.get_arestas() or (v, u) in outrografo.get_arestas()
                    if tem_aresta_aqui != tem_aresta_lá:
                        return False
        return True

    def is_isomorfo(self, outrografo):
        if self.numero_de_vertices() != outrografo.numero_de_vertices():
            return False
        if self.numero_de_arestas() != outrografo.numero_de_arestas():
            return False
        if self.sequencia_de_graus() != outrografo.sequencia_de_graus():
            return False

        vertices_self = self.get_vertices()
        vertices_other = outrografo.get_vertices()

        for perm in permutations(vertices_other):
            mapping = dict(zip(vertices_self, perm))
            arestas_mapeadas = {(mapping[u], mapping[v]) if mapping[u] < mapping[v] else (mapping[v], mapping[u])
                                for u, v in self.get_arestas()}
            if arestas_mapeadas == set(outrografo.get_arestas()):
                return True
        return False
    
    def colorir_grafo(self):
        vertices = self.get_vertices()
        n = len(vertices)
        cores = {}
        max_cores = n

        def e_valido(vertice, cor):
            for vizinho in self.lista_adj[vertice]:
                if vizinho in cores and cores[vizinho] == cor:
                    return False
            return True
        
        def backtracking(indice):
            if indice == n:
                return True
            v = vertices[indice]
            for cor in range(1, max_cores + 1):
                if e_valido(v, cor):
                    cores[v] = cor
                    if backtracking(indice + 1):
                        return True
                    cores.pop(v)
            return False
        
        backtracking(0)
        numero_de_cores = max(cores.values())
        return numero_de_cores, cores


if __name__ == "__main__":

    aulas = ['M', 'A', 'C', 'F', 'Q', 'P']
    g = GrafoEsparso(labels=aulas)

    g.adicionar_aresta('C','F')
    g.adicionar_aresta('C','A')
    g.adicionar_aresta('F','A')
    g.adicionar_aresta('M','P')
    g.adicionar_aresta('M','A')
    g.adicionar_aresta('P','A')
    g.adicionar_aresta('Q','F')

    for v_origin, v_dest in g.get_arestas():
        print(f"- Aula {v_origin} tem conflito com: {v_dest}")
    print("-" * 30)

    numero_minimo_horarios, cores_atribuidas = g.colorir_grafo()
    print(f"Número mínimo de horários necessários: {numero_minimo_horarios}")
    print(cores_atribuidas)