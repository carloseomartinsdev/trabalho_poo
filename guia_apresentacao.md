# Guia da Apresentação — CVRP: Otimização de Rotas de Entrega

## Estrutura Geral

A apresentação possui **17 slides** organizados em 4 blocos:

1. **Introdução** (~2 min) — Slides 1 a 4
2. **Metodologia** (~3 min) — Slides 5 a 7
3. **Resultados e Insights** (~3 min) — Slides 8 a 13
4. **Conclusão** (~2 min) — Slides 14 a 17

Cada slide segue o formato **pergunta-resposta implícito**: o título é uma pergunta que o público naturalmente faria, e o conteúdo é a resposta.

---

## BLOCO 1: INTRODUÇÃO (~2 min)

### Slide 1: Capa

**O que apresentar:**
- Título: "Otimização de Rotas de Entrega"
- Subtítulo: CVRP — Capacitated Vehicle Routing Problem
- Tecnologias: Programação Inteira, PuLP + OSRM, Python

**O que falar:**
- Apresentar-se brevemente
- "Este projeto resolve um problema real de logística em Fortaleza/CE usando técnicas de Pesquisa Operacional"
- "Usamos coordenadas GPS reais e distâncias rodoviárias calculadas via API OSRM"

---

### Slide 2: Qual é o problema? (Introdução)

**O que apresentar:**
- Empresa de logística em Fortaleza/CE, 15 clientes, 2 veículos de 500kg
- Demanda de teste: 973 kg (com nota explicando que varia na prática)
- Distâncias reais via OSRM

**O que falar:**
- "Uma empresa precisa entregar mercadorias para 15 clientes diariamente"
- "As rotas são definidas manualmente, sem critério de otimização"
- "Usamos uma demanda de 973 kg para teste — na prática, esse valor varia diariamente"
- "As distâncias foram calculadas usando rotas rodoviárias reais, não linha reta"

---

### Slide 3: Onde estão os clientes? (Mapa)

**O que apresentar:**
- Imagem do mapa à esquerda (mapa_clientes.png)
- Informações à direita: 16 pontos reais, Fortaleza/CE, GPS, OSRM

**O que falar:**
- "Aqui vemos a localização real dos 15 clientes e do centro de distribuição"
- "Os pontos estão espalhados por Fortaleza e região metropolitana"
- "As distâncias entre cada par de pontos foram calculadas pela API OSRM — são rotas reais por estrada, considerando ruas, rodovias e sentido de mão"

---

### Slide 4: Por que isso importa para o negócio?

**O que apresentar:**
- Tabela de parâmetros: R$ 3,50/km, R$ 3.000/motorista, 22 dias úteis, vel. média 25 km/h
- Custo fixo: R$ 6.000/mês (2 motoristas)
- Custo oculto: tempo do motorista no trânsito (R$ 17,05/hora)

**O que falar:**
- "Cada km rodado custa R$ 3,50 em combustível, manutenção e depreciação"
- "Cada motorista custa R$ 3.000/mês — é um custo fixo por veículo"
- "Mas existe um custo oculto: o tempo que o motorista passa no trânsito. A R$ 17,05/hora, esse tempo desperdiçado tem um preço"
- "A pergunta-chave é: compensa adicionar um 3º veículo se a distância diminuir?"

---

## BLOCO 2: METODOLOGIA (~3 min)

### Slide 5: Como transformamos em modelo matemático?

**O que apresentar:**
- Técnica: Programação Inteira (PI)
- Modelo: CVRP
- Variável: x[i][j][k] binária
- Função objetivo: Minimizar Σ distância × x
- Ferramenta: Python + PuLP + OSRM

**O que falar:**
- "Transformamos o problema real em um modelo matemático de Programação Inteira"
- "A variável x[i][j][k] é binária: 1 se o veículo k vai do ponto i ao ponto j"
- "O objetivo é minimizar a soma de todas as distâncias percorridas"
- "Usamos PuLP com o solver CBC para resolver, e a API OSRM para as distâncias reais"

---

### Slide 6: Quais regras o modelo respeita?

**O que apresentar:**
- 5 restrições + fórmula MTZ
- Explicação de por que MTZ é necessária

**O que falar:**
- "Todo cliente deve ser atendido exatamente uma vez"
- "Os veículos partem do depósito e voltam ao depósito"
- "Se um veículo entra em um cliente, ele precisa sair"
- "Nenhum veículo pode carregar mais de 500kg"
- "A restrição MTZ evita que o solver crie mini-rotas desconectadas do depósito"
- Se perguntarem: "MTZ usa variáveis auxiliares u[i] para garantir a ordem de visita — é uma técnica clássica de Pesquisa Operacional"

---

### Slide 7: O que o modelo encontrou?

**O que apresentar:**
- Veículo 1: CD→C6→C7→C8→C11→C12→C9→C1→C13→CD (494/500kg, 91.17km, R$ 319,10)
- Veículo 2: CD→C4→C3→C10→C14→C15→C2→C5→CD (479/500kg, 100.34km, R$ 351,19)
- Total: 191.51 km/dia, R$ 670,28/dia

**O que falar:**
- "O veículo 1 atende 8 clientes com 494 kg, percorrendo 91 km"
- "O veículo 2 atende 7 clientes com 479 kg, percorrendo 100 km"
- "Ambos operam próximos da capacidade máxima — 494 e 479 de 500 kg"
- "Isso mostra que a capacidade é o gargalo — o solver não tem folga para redistribuir"

---

## BLOCO 3: RESULTADOS E INSIGHTS (~3 min)

### Slide 8: Quanto a empresa economiza?

**O que apresentar:**
- Manual: 343.43 km → R$ 1.202,01/dia
- Otimizada: 191.51 km → R$ 670,28/dia
- Economia: 44.2% → R$ 531,73/dia → R$ 11.698/mês → R$ 140.376/ano

**O que falar:**
- "A rota manual percorre 343 km por dia, custando R$ 1.202"
- "Com otimização, reduzimos para 191 km, custando R$ 670"
- "Economia de 44.2%, ou R$ 531 por viagem"
- "Em um ano, são R$ 140 mil de economia"
- **Este é o slide mais impactante — dar ênfase aos números**

---

### Slide 9: E o tempo no trânsito?

**O que apresentar:**
- 3 cenários: Pico (20 km/h), Média (25 km/h), Fora do pico (35 km/h)
- Economia combinada: ~R$ 634/dia → ~R$ 167.498/ano (19% a mais)

**O que falar:**
- "O motorista não percorre a rota toda na mesma condição de trânsito"
- "No pico, a rota manual leva ~17 horas somando os 2 veículos, a otimizada ~9.6 horas"
- "Quando somamos distância + tempo, a economia sobe para ~R$ 167 mil/ano"
- "Quanto pior o trânsito, mais valiosa é a otimização"

---

### Slide 10: E se adicionarmos um 3º veículo? (Distâncias)

**O que apresentar:**
- 2 veículos: 191.51 km (R$ 670,28/dia)
- 3 veículos: 188.88 km (R$ 661,08/dia)
- Redução: apenas 1.4% (2.63 km/dia)

**O que falar:**
- "Com 3 veículos, a distância cai de 191.51 para 188.88 km — apenas 1.4%"
- "Os 2 veículos já distribuem os clientes de forma quase ótima"
- "O 3º veículo agrega muito pouco em termos de rota"
- "Mas será que essa pequena economia compensa o custo extra?"

---

### Slide 11: Essa redução compensa o custo? (Financeiro)

**O que apresentar:**
- Economia km/mês: R$ 202,40
- Custo extra motorista: R$ 3.000/mês
- Saldo: -R$ 2.797/mês ❌ NÃO COMPENSA

**O que falar:**
- "A economia em km é de apenas R$ 202 por mês"
- "Mas o 3º motorista custa R$ 3.000 por mês"
- "Prejuízo de R$ 2.797 por mês — NÃO compensa"
- **Este é o trade-off mais importante do projeto**

---

### Slide 12: E se reduzirmos para 1 veículo?

**O que apresentar:**
- Demanda: 973 kg vs Capacidade: 500 kg
- INVIÁVEL

**O que falar:**
- "Com 1 veículo, é impossível — a demanda de 973 kg excede os 500 kg de capacidade"
- "A frota mínima de 2 veículos é obrigatória"
- "A capacidade é o gargalo escondido que mais impacta a operação"

---

### Slide 13: A demanda é fixa? (Janela de decisão)

**O que apresentar:**
- Tabela com 3 faixas: até 950 kg (2V com folga), 950-1.000 kg (2V apertado), acima de 1.000 kg (3V obrigatório)
- Folga atual: apenas 27 kg (2.7%)
- Insight estratégico

**O que falar:**
- "Na prática, a demanda varia diariamente"
- "Hoje estamos com 973 kg — apenas 27 kg abaixo do limite"
- "Se crescer 28 kg, o 3º veículo se torna obrigatório"
- "A análise de equilíbrio mostrou que NÃO EXISTE ponto onde 3 veículos são mais baratos que 2"
- "Enquanto 2 veículos forem viáveis, são SEMPRE mais baratos"
- "O 3º veículo só se justifica por VIABILIDADE operacional, nunca por economia"
- "Com 950 kg, ambas as frotas percorrem a mesma distância (186.72 km), mas 2 veículos custam R$ 3.000 a menos"
- "Acima de 1.000 kg, 2 veículos são inviáveis e o 3º é inevitável"
- "A recomendação é: monitorar a demanda diária e ter um plano para quando ultrapassar o limite"

---

## BLOCO 4: CONCLUSÃO (~2 min)

### Slide 14: O que aprendemos?

**O que apresentar:**
- 4 insights consolidados:
  1. Decisão subótima: 44.2% mais distância → R$ 140 mil/ano
  2. Custo oculto: tempo no trânsito → R$ 167 mil/ano
  3. Trade-off: 3º veículo não compensa (prejuízo R$ 2.797/mês)
  4. Gargalo: capacidade ~98% ocupada, 1 veículo inviável

**O que falar:**
- Resumir os 4 insights de forma direta
- "A otimização de rotas gera economia real e mensurável"
- "O 3º veículo não compensa financeiramente, mas pode ser necessário se a demanda crescer"
- "A capacidade dos veículos é o fator limitante — não a quantidade"

---

### Slide 15: Alguém validou?

**O que apresentar:**
- Espaço para depoimento

**O que falar:**
- Apresentar o depoimento (print, e-mail ou relato)
- Quem foi a pessoa, cargo, reação
- Faz sentido? Implementaria?

---

### Slide 16: Limitações e próximos passos

**O que apresentar:**
- Limitações: OSRM sem trânsito real, sem janelas de horário, custo fixo, velocidade estimada
- Próximos passos: Google Maps API, VRPTW, frota heterogênea, heurísticas

**O que falar:**
- "O modelo usa distâncias reais, mas não considera trânsito em tempo real"
- "Na prática, a janela de entrega varia ao longo do dia — o motorista pode sair no pico e terminar fora do pico"
- "Isso é exatamente o que o modelo VRPTW resolve — é o próximo passo natural"
- "Para instâncias maiores, heurísticas como Algoritmo Genético seriam mais eficientes"

---

### Slide 17: Encerramento

**O que falar:**
- Agradecer
- Abrir para perguntas

---

## Perguntas que o professor pode fazer

| Pergunta | Resposta sugerida |
|---|---|
| "Por que essa função objetivo?" | Minimizar distância = minimizar custo variável (R$ 3,50/km). É o objetivo mais direto e mensurável. |
| "Por que essas restrições?" | Cada uma garante viabilidade: visita única, retorno ao CD, capacidade, sem sub-rotas. |
| "O que a solução revelou?" | Rota manual desperdiça 44.2% da distância. 3º veículo não compensa. Capacidade é o gargalo. |
| "Fez análise de sensibilidade?" | Sim: 3 veículos (não compensa — prejuízo R$ 2.797/mês), +1 cliente, 1 veículo (inviável), variação de demanda (break-even). |
| "Qual o gargalo?" | Capacidade dos veículos — ambos a ~98%. Não existe ponto onde 3 veículos são mais baratos que 2. |
| "E se a demanda variar?" | Analisamos de 950 a 1.500 kg. Até 1.000 kg, 2 veículos são SEMPRE mais baratos. Acima, 3 são obrigatórios. |
| "E o trânsito?" | Usamos velocidade média de Fortaleza (20-35 km/h). No pico, a economia é ainda maior. Próximo passo: trânsito em tempo real. |
| "A janela de entrega é fixa?" | Não — o motorista pode sair no pico e terminar fora dele. Isso é uma limitação do modelo atual. O VRPTW resolveria. |
| "Implementaria?" | Sim, com ajustes: trânsito real, janelas de horário, monitoramento de demanda diária. |
| "Usou IA?" | Sim, para auxiliar na modelagem e análise. Na apresentação, defendo cada decisão com base nos resultados. |
