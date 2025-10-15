# 🚚 Otimização de Rotas de Entrega com Algoritmo Genético

## Tech Challenge - Fase 2: Pós-Graduação em Arquitetura de Software

Este projeto é uma solução para o **Projeto 2 (Otimização de Rotas Médicas)** do Tech Challenge. O objetivo é desenvolver um sistema que otimiza as rotas de distribuição de medicamentos e insumos hospitalares, resolvendo o Problema do Caixeiro Viajante (TSP) com múltiplas restrições, conhecido como Vehicle Routing Problem (VRP).

A solução utiliza um **Algoritmo Genético** para encontrar as rotas mais eficientes e apresenta um **dashboard de desempenho interativo** construído com Pygame para visualizar a otimização em tempo real.

---

## 🚀 Principais Funcionalidades

* **Algoritmo Genético Avançado:** Implementação de um AG para resolver o VRP com operadores de seleção por torneio, crossover e múltiplos tipos de mutação.
* **Múltiplas Restrições de Negócio:** O algoritmo considera:
    * **Capacidade** limitada de cada veículo.
    * **Autonomia** (distância máxima) de cada veículo.
    * **Prioridade de Entrega**, penalizando soluções que atrasam entregas críticas.
* **Dashboard Interativo em Tempo Real:** Uma interface gráfica construída com Pygame que permite visualizar:
    * A melhor rota encontrada para cada veículo, com cores distintas.
    * O **Depósito** e os **Pontos de Entrega** (com destaque para os prioritários).
    * **Gráficos de Desempenho** que mostram a evolução do Custo (Fitness) e da Distância Pura a cada geração.
    * O **Status da Frota**, com barras de progresso mostrando a carga de cada veículo em tempo real.
* **Relatório Final:** Ao final da simulação, uma tela de resumo apresenta as métricas de desempenho da melhor solução encontrada.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Visualização:** Pygame
* **Estrutura:** Programação Orientada a Objetos (POO)

---

## 📁 Estrutura do Projeto

O projeto está organizado de forma modular para separação de responsabilidades:

```
PROJETO2_OTIMIZACAOROTAS/
│
├── .venv/                  # Ambiente virtual do Python
├── algorithms/
│   └── genetic_algorithm.py  # Contém toda a lógica do Algoritmo Genético
│
├── data/
│   └── example_data.py       # Funções para gerar dados de teste (frota, pontos de entrega)
│
├── models/
│   ├── delivery_point.py     # Classe que modela os Pontos de Entrega
│   └── vehicle.py            # Classe que modela os Veículos da frota
│
├── test_system.py          # Script principal para executar o dashboard de visualização
├── visualization.py        # Módulo com todas as funções de desenho do Pygame
└── requirements.txt        # Lista de dependências do projeto
```

---

## ⚙️ Instalação e Execução

Siga os passos abaixo para rodar o projeto em seu ambiente local.

### Pré-requisitos

* Python 3.11 ou superior instalado.

### Passos

1.  **Clone o repositório:**

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    
    # Ativar no Linux/macOS
    # source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Dashboard:**
    ```bash
    python test_system.py
    ```

A janela do dashboard será iniciada e a simulação começará automaticamente.

---

## 📊 Entendendo o Dashboard

A tela é dividida em duas seções principais:

### Lado Esquerdo: Visualização das Rotas

* **Ponto Azul Escuro:** O depósito central, de onde todas as rotas partem e retornam.
* **Pontos Vermelhos:** Os locais de entrega padrão.
* **Pontos com Anel Dourado:** Entregas de **alta prioridade**.
* **Linhas Coloridas:** A rota otimizada para cada veículo da frota.

### Lado Direito: Painel de Desempenho

1.  **Gráfico de Fitness (Custo Total):** Mostra a queda do "custo" da solução. O custo inclui a distância e as penalidades. Quanto menor, melhor.
2.  **Gráfico de Distância Pura:** Mostra a queda da distância total percorrida, sem considerar as penalidades.
3.  **Status da Frota:** Exibe a carga atual de cada veículo em relação à sua capacidade máxima. A barra muda de cor (verde -> amarelo -> vermelho) conforme se aproxima do limite.
4.  **Métricas Gerais:** Informações numéricas da melhor solução encontrada até o momento, incluindo o valor exato das penalidades.

---