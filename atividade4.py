import sys
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
    def is_subgrafo_induzido(self, outrografo):
        pass

class GrafoDenso(Grafo):
    # Definição do grafo
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

        self.matriz = [[0] * self.num_vertices for i in range(self.num_vertices)]
        
    
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
            print(f"Aresta adicionada entre {u} e {v}.")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")


    def remover_aresta(self, u, v):
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)
            if self.matriz[idx_u][idx_v] == 0:
                print(f"Aresta entre {u} e {v} não existe.")
                return
            self.matriz[idx_u][idx_v] = 0
            self.matriz[idx_v][idx_u] = 0
            print(f"Aresta removida entre {u} e {v}.")
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
        return int(sum([len(vizinhos) for vizinhos in self.lista_adj.values()])/2)

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
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def remover_aresta(self, u, v, peso=None):
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


if __name__ == "__main__":
    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    g1 = GrafoEsparso(labels=vertices_labels)
    g1.adicionar_aresta('A', 'B')
    g1.adicionar_aresta('A', 'C')
    g1.adicionar_aresta('C', 'D')
    g1.adicionar_aresta('C', 'E')
    g1.imprimir()
    print("Vértices:", g1.get_vertices())
    print("Arestas:", g1.get_arestas())
