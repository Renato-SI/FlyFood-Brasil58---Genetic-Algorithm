import os
from Ferramentas import*
from Edge_Recombination import crossover_erx

pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(pasta_atual, "Matriz_Brasil58.tsp")

objArq = open(caminho_arquivo, "r")

distancias = {}
qtd_cidades = 58

for i in range(1, 58): #linhas 1 a 57 pois a 58 nao terá aresta
	linha = objArq.readline() #le só uma linha do arquivo
	#transformando a linha em lista de strings:
	lista = linha.split() #obs: lista de strings (não int)

	for j in range(i+1, 59): #colunas i+1 a 58
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
print(population)
print(aptidao_atual)