# Projeto Final — Pesquisa Operacional e Otimização em IA

## Tema: CVRP — Otimização de Rotas de Entrega com Veículos Capacitados

---

## 1. Contexto do Problema
- Empresa de logística com 1 centro de distribuição (CD)
- 10 clientes para atender diariamente
- 2 veículos disponíveis, cada um com capacidade máxima de 500kg
- Cada cliente possui uma demanda (peso em kg)
- Objetivo: **minimizar a distância total percorrida**, reduzindo tempo e custo

---

## 2. Modelagem Matemática (Programação Inteira)

### Variáveis de decisão
- `x[i][j][k]` = 1 se o veículo k percorre o arco (i → j), 0 caso contrário
- `u[i]` = variável auxiliar para eliminação de sub-rotas (MTZ)

### Função objetivo
- Minimizar Σ distância[i][j] * x[i][j][k] para todos i, j, k

### Restrições
1. Cada cliente é visitado exatamente 1 vez
2. Cada veículo sai do CD e retorna ao CD
3. Conservação de fluxo (se entra, sai)
4. Capacidade máxima de cada veículo respeitada
5. Eliminação de sub-rotas (Miller-Tucker-Zemlin)

---

## 3. Entregas

| # | Entrega | Formato | Status |
|---|---------|---------|--------|
| 1 | Apresentação | Slides PDF | ⬜ |
| 2 | Relatório | Documento 2-3 páginas | ⬜ |
| 3 | Notebook Python | Google Colab (.ipynb) | ⬜ |

---

## 4. Estrutura do Notebook

1. **Instalação e imports**
2. **Geração dos dados fictícios** (CD + 10 clientes + demandas)
3. **Visualização dos pontos no mapa**
4. **Modelagem CVRP com PuLP**
5. **Resolução e extração das rotas**
6. **Visualização das rotas otimizadas**
7. **Comparação: rota manual vs otimizada**
8. **Análise de sensibilidade:**
   - Cenário A: 3 veículos em vez de 2
   - Cenário B: 1 cliente novo adicionado
   - Cenário C: apenas 1 veículo disponível
9. **Conclusões e insights**

---

## 5. Análise de Sensibilidade (Cenários)

| Cenário | Descrição | Pergunta-chave |
|---------|-----------|----------------|
| A | 3 veículos | Compensa o custo de mais um veículo? |
| B | +1 cliente | Quanto impacta na distância total? |
| C | 1 veículo só | É viável? Qual o aumento de distância? |

---

## 6. Possíveis Insights Esperados
- Gargalo escondido (capacidade do veículo limita a rota)
- Decisão subótima (rota manual vs otimizada)
- Trade-off revelado (mais veículos vs custo operacional)
- Análise de sensibilidade (impacto de mudanças nos parâmetros)

---

## 7. Ferramentas
- Python 3.x
- PuLP (otimização)
- Matplotlib (visualização)
- NumPy (cálculos)
