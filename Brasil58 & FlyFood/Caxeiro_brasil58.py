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
toolbox.register("mutate", mutacao_2opt, matriz_dist=matriz_distancias)
toolbox.register("select", tools.selTournament, tournsize=3)

# Execução
def rodar_ag():
    populacao = toolbox.population(n=300)
    hof = tools.HallOfFame(10)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", np.min)

    CXPB, MUTPB, NGEN = 0.7, 0.3, 200

    print("Iniciando DEAP com Order Crossover (OX)...")
    inicio = time.time()
    
    populacao, logbook = algorithms.eaMuPlusLambda(
        populacao, 
        toolbox, 
        mu=150,
        lambda_=600,
        cxpb=CXPB, 
        mutpb=MUTPB, 
        ngen=NGEN, 
        stats=stats, 
        halloffame=hof, 
        verbose=True
    )
    
    tempo_ga = time.time() - inicio


    melhor_refinado = None
    custo_final = float('inf')
    for individuo in hof:
        rota_refinada = aplicar_2opt(individuo, matriz_distancias)
        custo_refinado = avaliar_rota(rota_refinada, matriz_distancias)[0]
        if custo_refinado < custo_final:
            melhor_refinado = rota_refinada
            custo_final = custo_refinado

    # Mapeamento para exibição das cidades
    rota_exibicao = [int(cidade) + 1 for cidade in melhor_refinado]

    print("\n================ Resultado: Matriz Brasil58 ================")
    print(f"Tempo de Execução (GA): {tempo_ga:.2f} segundos")
    print(f"Custo Final Otimizado (DEAP + 2-Opt): {custo_final:.0f}")
    print(f"Rota Final (Cidades 1 a 58):\n{rota_exibicao}")

if __name__ == "__main__":
    rodar_ag()