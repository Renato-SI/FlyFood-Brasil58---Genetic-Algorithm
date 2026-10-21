import random
import numpy as np
def crossover_erx(parents, offspring_size, ga_instance):
    filhos = []
    total_filhos = offspring_size[0]
    quantidade_pais = len(parents)

    for i in range(total_filhos):
        p1 = parents[i % quantidade_pais]
        p2 = parents[(i + 1) % quantidade_pais]

        adjacencias = {cidade: set() for cidade in p1} 
        for pai in [p1, p2]:
            tamanho = len(pai)
            for k in range(tamanho):
                cidade_atual = pai[k]
                adjacencias[cidade_atual].add(pai[k - 1])
    
                adjacencias[cidade_atual].add(pai[(k + 1) % tamanho])
        filho = []
        cidades_restantes = set(p1)
        actual_plus_city = p1[0]

        while len(cidades_restantes) > 0:
            filho.append(actual_plus_city)
            cidades_restantes.remove(actual_plus_city)

            for vizinho_set in adjacencias.values():
                vizinho_set.discard(actual_plus_city)

            
            vizinhos_disponiveis = adjacencias[actual_plus_city]

            if len(vizinhos_disponiveis) > 0:
                menor_qtd_arestas = 99999
                for vizinho in vizinhos_disponiveis:
                    qtd_arestas = len(adjacencias[vizinho])
                    if qtd_arestas < menor_qtd_arestas:
                        menor_qtd_arestas = qtd_arestas
                candidatos = []
                for vizinho in vizinhos_disponiveis:
                    if len(adjacencias[vizinho]) == menor_qtd_arestas:
                        candidatos.append(vizinho)

                actual_plus_city = random.choice(candidatos)

            elif len(cidades_restantes) > 0:
                actual_plus_city = random.choice(list(cidades_restantes))

        filhos.append(filho)

    return np.array(filhos)