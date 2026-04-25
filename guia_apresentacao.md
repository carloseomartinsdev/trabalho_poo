# Guia da Apresentação — CVRP: Otimização de Rotas de Entrega

## Estrutura Geral

A apresentação possui **17 slides** organizados em 4 blocos conforme a estrutura exigida pela avaliação:

1. **Contexto** (~2 min) — Slides 1 a 4
2. **Modelagem** (~3 min) — Slides 5 e 6
3. **Resultados e Insights** (~3 min) — Slides 7 a 14
4. **Validação** (~2 min) — Slides 15 a 17

---

## Slide 1: Capa

**O que apresentar:**
- Título do projeto: "Otimização de Rotas de Entrega"
- Subtítulo: CVRP — Capacitated Vehicle Routing Problem
- Disciplina e instituição
- Tecnologias utilizadas: Programação Inteira, PuLP + OSRM, Python

**O que falar:**
- Apresentar-se brevemente
- Explicar que o projeto resolve um problema real de logística usando técnicas de otimização
- Mencionar que as distâncias foram calculadas usando rotas rodoviárias reais via API OSRM

---

## Slide 2: Contexto

**O que apresentar:**
- O problema: empresa de logística em Fortaleza/CE com 15 clientes
- 2 veículos com capacidade de 500kg cada
- Demanda total: 973 kg
- Objetivo: minimizar distância total percorrida

**O que falar:**
- Descrever o cenário: "Uma empresa precisa entregar mercadorias para 15 clientes diariamente, partindo de um centro de distribuição"
- Destacar que as rotas são definidas manualmente, sem critério de otimização
- Explicar por que isso é um problema: desperdício de combustível, tempo e dinheiro

---

## Slide 3: Parâmetros de Custo

**O que apresentar:**
- Tabela com todos os parâmetros financeiros:
  - R$ 3,50/km (custo operacional)
  - R$ 3.000/mês por motorista
  - 22 dias úteis/mês
  - 2 veículos de 500kg
  - 973 kg de demanda total
  - Distâncias calculadas via OSRM API (rotas reais)

**O que falar:**
- Explicar cada parâmetro e sua origem
- Destacar que o custo fixo mensal com 2 motoristas é R$ 6.000
- Explicar que o custo variável depende da distância percorrida
- Mencionar que usar distâncias reais (OSRM) em vez de euclidianas torna o modelo muito mais preciso

---

## Slide 4: Por que otimizar rotas?

**O que apresentar:**
- 4 benefícios: combustível, tempo, sustentabilidade, escala
- Pergunta-chave: "Compensa adicionar um 3º veículo?"

**O que falar:**
- Explicar cada benefício brevemente
- Introduzir a pergunta central da análise de sensibilidade: se adicionar um veículo custa R$ 3.000/mês a mais em salário, a redução de km precisa compensar esse custo
- Isso será respondido nos slides de análise de sensibilidade

---

## Slide 5: Modelagem — CVRP

**O que apresentar:**
- Técnica: Programação Inteira (PI)
- Tipo: CVRP — Capacitated Vehicle Routing Problem
- Variável de decisão: x[i][j][k] = 1 se veículo k vai do ponto i ao ponto j
- Função objetivo: Minimizar Σ distância(i,j) × x[i][j][k]
- Ferramenta: Python + PuLP (solver CBC) + OSRM API

**O que falar:**
- Explicar que transformamos o problema real em um modelo matemático
- A variável x[i][j][k] é binária: 1 se o veículo k percorre o arco de i para j, 0 caso contrário
- O objetivo é minimizar a soma de todas as distâncias percorridas
- Destacar que usamos PuLP (biblioteca Python) com o solver CBC para resolver
- As distâncias foram obtidas via API OSRM, que calcula rotas rodoviárias reais

---

## Slide 6: Restrições do Modelo

**O que apresentar:**
- 5 restrições:
  1. Cada cliente visitado exatamente 1 vez
  2. Cada veículo sai e retorna ao CD
  3. Conservação de fluxo (se entra, sai)
  4. Capacidade máxima de 500kg por veículo
  5. Eliminação de sub-rotas (MTZ)
- Fórmula MTZ

**O que falar:**
- Explicar cada restrição de forma simples:
  - "Todo cliente deve ser atendido, e apenas uma vez"
  - "Os veículos partem do depósito e voltam ao depósito"
  - "Se um veículo entra em um cliente, ele precisa sair"
  - "Nenhum veículo pode carregar mais de 500kg"
  - "A restrição MTZ evita que o solver crie sub-rotas desconectadas"
- Se perguntarem sobre MTZ: é uma técnica clássica que usa variáveis auxiliares u[i] para garantir a ordem de visita

---

## Slide 7: Resultados

**O que apresentar:**
- 3 cards grandes:
  - Distância Manual: **343.43 km** → R$ 1.202,01/dia
  - Distância Otimizada: **191.51 km** → R$ 670,28/dia
  - Economia: **44.2%** → R$ 531,73/dia
- Impacto financeiro: R$ 11.698,06/mês → R$ 140.376,72/ano
- Custo mensal total: Manual R$ 32.444,22 vs Otimizado R$ 20.746,16

**O que falar:**
- "A rota manual percorre 343 km por dia, custando R$ 1.202"
- "Com otimização, reduzimos para 191 km, custando R$ 670"
- "Isso representa uma economia de 44.2%, ou R$ 531 por viagem"
- "Em um mês, são quase R$ 12 mil de economia. Em um ano, R$ 140 mil"
- "O custo mensal total cai de R$ 32 mil para R$ 20 mil"
- **Este é o slide mais impactante — dar ênfase aos números**

---

## Slide 8: Rotas Otimizadas

**O que apresentar:**
- Detalhes dos 2 veículos:
  - V1: CD → C6 → C7 → C8 → C11 → C12 → C9 → C1 → C13 → CD (494/500 kg, 91.17 km, R$ 319,10)
  - V2: CD → C4 → C3 → C10 → C14 → C15 → C2 → C5 → CD (479/500 kg, 100.34 km, R$ 351,19)
- Custo diário total: R$ 670,28
- Custo mensal total: R$ 20.746,16

**O que falar:**
- "O veículo 1 atende 8 clientes com 494 kg de carga, percorrendo 91 km"
- "O veículo 2 atende 7 clientes com 479 kg, percorrendo 100 km"
- "Ambos operam próximos da capacidade máxima (494 e 479 de 500 kg)"
- "Isso mostra que a capacidade é o gargalo — o solver não tem muita folga para redistribuir"

---

## Slide 9: Manual vs Otimizada

**O que apresentar:**
- Comparação lado a lado: Manual (343.43 km) vs Otimizada (191.51 km)
- Economia de 44.2% → R$ 140.376,72/ano

**O que falar:**
- "Na rota manual, os clientes são distribuídos sem critério, gerando cruzamentos e idas e vindas desnecessárias"
- "Na rota otimizada, os clientes são agrupados por proximidade geográfica"
- "A diferença é de quase 152 km por dia — isso é muito significativo"

---

## Slide 10: Insights Descobertos

**O que apresentar:**
- 3 insights:
  1. Decisão subótima: rota manual gera 44.2% mais distância → R$ 140 mil/ano
  2. Trade-off revelado: 3º veículo reduz apenas 1.4% → não compensa
  3. Gargalo escondido: capacidade dos veículos (494/500 e 479/500 kg)

**O que falar:**
- "O primeiro insight é que a rota manual desperdiça quase metade da distância"
- "O segundo é que adicionar um 3º veículo não compensa financeiramente — vamos ver isso em detalhe"
- "O terceiro é que o verdadeiro gargalo é a capacidade dos veículos, não a quantidade"

---

## Slide 11: Análise de Sensibilidade — Resumo

**O que apresentar:**
- Tabela com 3 cenários:
  - A: 3 veículos → redução de 1.4%
  - B: +1 cliente (C16) → distância 147.06 km (-23.2%)
  - C: 1 veículo → INVIÁVEL (973kg > 500kg)

**O que falar:**
- "Testamos 3 cenários para entender como mudanças na frota ou demanda afetam o resultado"
- "Vamos detalhar o cenário A em dois slides"

---

## Slide 12: Cenário A — Parte 1: Distâncias

**O que apresentar:**
- 3 cards:
  - 2 veículos: 191.51 km (R$ 670,28/dia)
  - 3 veículos: 188.88 km (R$ 661,08/dia)
  - Redução: 1.4% (apenas 2.63 km/dia)

**O que falar:**
- "Com 3 veículos, a distância cai de 191.51 para 188.88 km — apenas 1.4%"
- "Isso acontece porque os 2 veículos já conseguem distribuir os clientes de forma quase ótima"
- "O 3º veículo agrega muito pouco em termos de rota"
- "Mas será que essa pequena economia compensa o custo extra?"

---

## Slide 13: Cenário A — Parte 2: Análise Financeira

**O que apresentar:**
- 3 cards:
  - Economia em km/mês: R$ 202,40
  - Custo extra 3º motorista: R$ 3.000/mês
  - Saldo: **- R$ 2.797,60/mês ❌**
- Veredicto: NÃO COMPENSA
- Custo mensal: 2 veículos R$ 20.746,16 vs 3 veículos R$ 23.543,76

**O que falar:**
- "A economia em km é de apenas R$ 202 por mês"
- "Mas o 3º motorista custa R$ 3.000 por mês"
- "O saldo é negativo: prejuízo de R$ 2.797 por mês"
- "Portanto, NÃO compensa adicionar o 3º veículo"
- "O custo mensal total sobe de R$ 20.746 para R$ 23.543"
- **Este é o trade-off mais importante do projeto**

---

## Slide 14: Cenário C — 1 Veículo

**O que apresentar:**
- Demanda total: 973 kg vs Capacidade 1 veículo: 500 kg
- INVIÁVEL

**O que falar:**
- "Com apenas 1 veículo, é impossível atender todos os clientes"
- "A demanda total é 973 kg, mas o veículo só carrega 500 kg"
- "Isso demonstra que a frota mínima de 2 veículos é necessária"
- "A capacidade é o gargalo escondido que mais impacta a operação"

---

## Slide 15: Validação

**O que apresentar:**
- Espaço para depoimento de alguém do trabalho

**O que falar:**
- Apresentar o depoimento (print de WhatsApp, e-mail ou relato verbal)
- Explicar quem foi a pessoa (nome e cargo)
- Qual foi a reação: faz sentido? Implementaria? O que mudaria?

---

## Slide 16: Limitações e Próximos Passos

**O que apresentar:**
- Limitações:
  - Distâncias OSRM (sem trânsito em tempo real)
  - Sem janelas de horário
  - Custo por km fixo
- Próximos passos:
  - Integrar dados de trânsito
  - Incluir janelas de tempo (VRPTW)
  - Testar frota heterogênea
  - Avaliar heurísticas para escalar

**O que falar:**
- "O modelo usa distâncias reais por estrada, mas não considera trânsito em tempo real"
- "Também não temos janelas de horário — quando o cliente pode receber"
- "Como próximos passos, poderíamos integrar dados de trânsito e testar com veículos de diferentes capacidades"
- "Para instâncias maiores, heurísticas como Algoritmo Genético seriam mais eficientes"

---

## Slide 17: Encerramento

**O que falar:**
- Agradecer a atenção
- Abrir para perguntas
- Estar preparado para responder:
  - "Por que essa função objetivo e não outra?" → Minimizar distância é o objetivo mais direto para reduzir custos
  - "Por que essas restrições?" → Cada uma garante viabilidade operacional
  - "O que a análise de sensibilidade revelou?" → Que 2 veículos é o ponto ótimo entre custo fixo e variável

---

## Perguntas que o professor pode fazer

| Pergunta | Resposta sugerida |
|---|---|
| "Por que essa é a função objetivo e não outra?" | Minimizar distância total é equivalente a minimizar custo variável (R$ 3,50/km). Poderíamos minimizar tempo, mas distância é mais mensurável. |
| "Por que escolheu essas restrições?" | Cada restrição garante viabilidade: visita única, retorno ao CD, capacidade respeitada, sem sub-rotas. |
| "O que a solução revelou?" | Que a rota manual desperdiça 44.2% da distância, e que adicionar um 3º veículo não compensa financeiramente. |
| "Fez análise de sensibilidade?" | Sim, 3 cenários: 3 veículos (não compensa), +1 cliente, 1 veículo (inviável). |
| "Qual o gargalo?" | A capacidade dos veículos — ambos operam a ~98% da capacidade. |
| "Implementaria na prática?" | Sim, com ajustes: incluir trânsito em tempo real e janelas de horário. |
| "Usou IA?" | Sim, para auxiliar na modelagem e análise. Na apresentação, defendo cada decisão com base nos resultados. |
