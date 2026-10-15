def custoCaminho(permutacao, dicDistancias):
	soma = 0
	for i in range(len(permutacao)-1):
		a = permutacao[i]
		b = permutacao[i+1]
		if (a,b) in dicDistancias:
			soma += dicDistancias[(a,b)]
		else:
			print(f"Erro! ({a},{b}) não existe no dicionario!")
			exit()
	soma += dicDistancias[(permutacao[-1],permutacao[0])]
	return soma

def inicializaPopulacao(tamanho, qtdeCidades):
	import random
	lista = []
	for i in range(tamanho):
		individuo = list(range(1, qtdeCidades+1))
		random.shuffle(individuo)
		lista.append(individuo)
	return lista

def calculaAptidao(populacao, dicDistancias):
	listaAptidao = []
	for elem in populacao:
		listaAptidao.append(custoCaminho(elem, dicDistancias))
	return listaAptidao