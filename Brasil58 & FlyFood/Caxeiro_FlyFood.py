import os
from Ferramentas import*
from Edge_Recombination import crossover_erx
import pygad

pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(pasta_atual, "Matriz_FlyFood.tsp")

objArq = open(caminho_arquivo, "r")

distancias = {}
qtd_cidades = 14

for i in range(1, 14): #linhas 1 a 57 pois a 58 nao terá aresta
	linha = objArq.readline() #le só uma linha do arquivo
	#transformando a linha em lista de strings:
	lista = linha.split() #obs: lista de strings (não int)

	for j in range(i+1, 15): #colunas i+1 a 58
		if len(lista) > 0:
			peso = int(lista.pop(0)) #obs: peso int, poderia ser float em outro problema
		else:
			print(f"Erro! linha {i} do arquivo não possui elementos suficientes")
			exit()
			
		distancias[(i,j)] = peso
		distancias[(j,i)] = peso
objArq.close()

population = inicializaPopulacao(100, qtd_cidades)
aptidao_atual = calculaAptidao(population, distancias)
custo_caminhos = custoCaminho(population[0], distancias)

ga_instance = pygad.GA(
	num_generations=300,
	num_parents_mating=20,
	sol_per_pop=50,
	num_genes=qtd_cidades,
	gene_space=list(range(1, qtd_cidades + 1)),
	allow_duplicate_genes=False,


	fitness_func=lambda ga, sol, idx:-custoCaminho(sol, distancias),
	crossover_type=crossover_erx,
	mutation_type='swap',
	mutation_percent_genes=15, 
	gene_type=int,
)
ga_instance.run()

melhor_rota, melhor_fitness, _ = ga_instance.best_solution()
print(melhor_rota, melhor_fitness)
