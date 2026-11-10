# FlyFood Melhorado & Benchmark Brasil58: Otimização Metaheurística de Rotas para Drones Urbanos 🚁

Este repositório contém a evolução do sistema **FlyFood**, uma solução de otimização de rotas para entregas via drones que resolve o Problema do Caixeiro-Viajante (PCV) através de uma abordagem metaheurística híbrida, combinando **Algoritmos Genéticos (AG)** via biblioteca DEAP com a técnica de busca local determinística **2-Opt**.

Desenvolvido como parte do Projeto Interdisciplinar (PISI II) do curso de Bacharelado em Sistemas de Informação (BSI) da Universidade Federal Rural de Pernambuco (UFRPE).

## 📌 O Problema e a Necessidade de Metaheurísticas

A abordagem exata por Força Bruta / Backtracking garante a rota ótima global, porém apresenta complexidade temporal fatorial $\mathcal{O}(n! \cdot n)$. Conforme o número de pontos de entrega cresce, a exploração exaustiva torna-se inviável em tempo hábil para a operação logística de drones:

* Na instância **FlyFood** ($14$ nós), o espaço de busca possui $14! \approx 8{,}7 \times 10^{10}$ caminhos possíveis.
* No benchmark **Brasil58** ($58$ nós), o espaço amostral salta para $58! \approx 4{,}05 \times 10^{78}$ permutações, tornando a busca exata absolutamente impraticável.

Para atender às restrições operacionais e preservar a bateria dos drones, o sistema emprega uma metaheurística estocástica de alta eficiência que converge rapidamente para soluções globais ou quase-ótimas em frações de segundo.

## 🧬 Algoritmo Genético Híbrido (DEAP + 2-Opt)

A arquitetura do sistema é baseada em um **Algoritmo Memético**, estruturado em três fases principais:

### 1. Representação e Mecânica Evolutiva

* **Cromossomo**: Permutação direta de índices inteiros correspondentes aos pontos de entrega.
* **Estratégia Evolutiva**: Algoritmo $(\mu + \lambda)$ (`eaMuPlusLambda`) onde:
  * Tamanho da população ($\mu$): $150$
  * Tamanho da prole ($\lambda$): $150$
  * Probabilidade de Crossover ($CXPB$): $0.7$
  * Probabilidade de Mutação ($MUTPB$): $0.3$
  * Número de Gerações ($NGEN$): $200$
* **Função de Fitness**: Avalia a distância total acumulada percorrida no circuito fechado (retornando ao ponto inicial).

### 2. Operadores Genéticos Customizados

* **Seleção**: Torneio estocástico (`selTournament`) com tamanho $k=3$.
* **Cruzamento**: *Order Crossover* (`cxOrdered` / OX), preservando a integridade das sequências sem duplicar ou omitir cidades.
* **Mutação Híbrida (`mutacao_2opt`)**: Aplica inversão de trechos (`mutInversion`) e, estocastically (10% de chance), insere um leve embaralhamento de índices (`mutShuffleIndexes`) seguido de otimização local 2-Opt no próprio indivíduo mutado.

### 3. Refinamento Pós-Evolutivo

Ao término do ciclo evolutivo, as melhores soluções retidas no *Hall of Fame* (HoF) passam por um refinamento final 2-Opt (`aplicar_2opt`). Este algoritmo analisa trocas de arestas e desfaz cruzamentos no espaço geométrico quando a variação de custo $\Delta < 0$, garantindo que a rota final seja localmente imbatível.

## 🇧🇷 O Benchmark Brasil58 e Validação de Escalabilidade

O **Brasil58** (`Matriz_Brasil58.tsp`) é uma matriz clássica de benchmark na literatura de otimização combinatória, contendo as distâncias simétricas entre 58 cidades brasileiras.

Neste projeto, o Brasil58 atua como um **teste de estresse e validação de generalização**:

* Demonstra que a abordagem memética desenvolvida não fica restrita a pequenas instâncias de entrega urbana.
* Comprova a capacidade do algoritmo de resolver problemas de escala continental em poucos segundos, superando a limitação fatorial do Backtracking.

## 📊 Estrutura dos Arquivos e Comparativo

| Arquivo | Descrição | Escala / Dimensão | Hall of Fame |
| ----- | ----- | ----- | ----- |
| `Caxeiro_FlyFood.py` | Script principal para resolução do problema de entregas FlyFood. | 14 cidades | `HoF(1)` |
| `Caxeiro_brasil58.py` | Script de teste de estresse e escalabilidade no benchmark nacional. | 58 cidades | `HoF(10)` |
| `Ferramentas.py` | Módulo utilitário com rotinas de leitura TSP, fitness e 2-Opt. | — | — |
| `Matriz_FlyFood.tsp` | Matriz simétrica de distâncias da instância FlyFood. | 14x14 | — |
| `Matriz_Brasil58.tsp` | Matriz simétrica de distâncias do benchmark Brasil58. | 58x58 | — |

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3.x e as bibliotecas de suporte instaladas:

```bash
pip install numpy deap
```

### Instalação e Execução

```bash
# 1. Clone o repositório
git clone https://github.com/thuliobandeira402/Backtracking-flyfood.git

# 2. Acesse a pasta do projeto
cd Backtracking-flyfood

# 3. Executar otimização para a matriz FlyFood (14 cidades)
python Caxeiro_FlyFood.py

# 4. Executar otimização para o benchmark Brasil58 (58 cidades)
python Caxeiro_brasil58.py
```

## 👨‍💻 Autores

* **Pedro Coutinho** — [pedro.coutinho@ufrpe.br](mailto:pedro.coutinho@ufrpe.br)
* **Renato Rodrigues** — [renato.filho@ufrpe.br](mailto:renato.filho@ufrpe.br)
* **Taryk Melo** — [taryk.melo@ufrpe.br](mailto:taryk.melo@ufrpe.br)
* **Thúlio Bandeira** — [thulio.roberto@ufrpe.br](mailto:thulio.roberto@ufrpe.br)