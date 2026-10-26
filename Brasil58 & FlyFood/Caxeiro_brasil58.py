import os
import random
import time
import numpy as np
from deap import base, creator, tools, algorithms
from Ferramentas import*

QTD_CIDADES = 58
pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_matriz = os.path.join(pasta_atual, "Matriz_Brasil58.tsp")
matriz_distancias = carregar_matriz_distancias(caminho_matriz, QTD_CIDADES)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("indices", random.sample, range(QTD_CIDADES), QTD_CIDADES)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", avaliar_rota, matriz_dist=matriz_distancias)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutInversion)
toolbox.register("select", tools.selTournament, tournsize=3)

# Execução
def rodar_ag():
    populacao = toolbox.population(n=200)
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", np.min)

    CXPB, MUTPB, NGEN = 0.8, 0.25, 5000

    print("Iniciando DEAP com Order Crossover (OX)...")
    inicio = time.time()
    
    populacao, logbook = algorithms.eaSimple(
        populacao, 
        toolbox, 
        cxpb=CXPB, 
        mutpb=MUTPB, 
        ngen=NGEN, 
        stats=stats, 
        halloffame=hof, 
        verbose=False
    )
    
    tempo_ga = time.time() - inicio
    melhor_ga = hof[0]
    custo_ga = melhor_ga.fitness.values[0]

    melhor_refinado = aplicar_2opt(melhor_ga, matriz_distancias)
    custo_final = avaliar_rota(melhor_refinado, matriz_distancias)[0]

    # Mapeamento para exibição das cidades
    rota_exibicao = [cidade + 1 for cidade in melhor_refinado]

    print("\n================ Resultado: Matriz Brasil58 ================")
    print(f"Tempo de Execução (GA): {tempo_ga:.2f} segundos")
    print(f"Custo de Saída do DEAP (GA Puro): {custo_ga:.0f}")
    print(f"Custo Final Otimizado (DEAP + 2-Opt): {custo_final:.0f}")
    print(f"Rota Final (Cidades 1 a 58):\n{rota_exibicao}")

if __name__ == "__main__":
    rodar_ag()