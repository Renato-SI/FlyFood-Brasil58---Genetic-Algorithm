import numpy as np
import random
from deap import tools

def carregar_matriz_distancias(caminho_arquivo, qtd_cidades):
    matriz = np.zeros((qtd_cidades, qtd_cidades), dtype=int)
    with open(caminho_arquivo, "r") as f:
        for i in range(qtd_cidades - 1):
            linha = f.readline().split()
            for j in range(i + 1, qtd_cidades):
                peso = int(linha.pop(0))
                matriz[i, j] = peso
                matriz[j, i] = peso
    return matriz

def avaliar_rota(individual, matriz_dist):
    ind = np.array(individual)
    proximos = np.roll(ind, -1)
    custo_total = np.sum(matriz_dist[ind, proximos])
    return (custo_total,)

def aplicar_2opt(rota, matriz_dist):
    best_rota = np.array(rota)
    n = len(best_rota)
    improved = True
    while improved:
        improved = False
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = best_rota[i - 1], best_rota[i]
                c, d = best_rota[j], best_rota[(j + 1) % n]
                delta = (matriz_dist[a, c] + matriz_dist[b, d]) - (matriz_dist[a, b] + matriz_dist[c, d])
                if delta < 0:
                    best_rota[i:j+1] = best_rota[i:j+1][::-1]
                    improved = True
    return best_rota

    
def mutacao_2opt(individual, matriz_dist):
    tools.mutInversion(individual)
    
    if random.random() < 0.10:
        tools.mutShuffleIndexes(individual, indpb=0.05)
        rota_refinada = aplicar_2opt(individual, matriz_dist)
        individual[:] = rota_refinada.tolist()
    return individual,
