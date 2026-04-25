# %% [markdown]
# ## 11. Resumo dos Resultados

# %%
print("=" * 60)
print("RESUMO FINAL DOS RESULTADOS")
print("=" * 60)
print(f"\n📊 Cenário Base (2 veículos, 10 clientes):")
print(f"   Distância otimizada: {dist_otimizada} km")
print(f"   Distância manual:    {round(dist_manual, 2)} km")
print(f"   Economia:            {economia}%")
print(f"\n📊 Cenário A — 3 veículos:")
print(f"   Distância: {dist_3v} km (redução de {round((1 - dist_3v/dist_otimizada)*100,1)}%)")
print(f"\n📊 Cenário B — +1 cliente:")
print(f"   Distância: {dist_11c} km (aumento de {round((dist_11c/dist_otimizada-1)*100,1)}%)")
print(f"\n📊 Cenário C — 1 veículo:")
if demanda_total > CAPACIDADE:
    print(f"   INVIÁVEL — demanda ({demanda_total}kg) > capacidade ({CAPACIDADE}kg)")
else:
    print(f"   Distância: {dist_1v} km (aumento de {round((dist_1v/dist_otimizada-1)*100,1)}%)")
print("=" * 60)

# %% [markdown]
# ## 12. Conclusões
#
# **Insights descobertos:**
#
# 1. **Decisão subótima:** A rota manual gera uma distância significativamente maior
#    que a rota otimizada, demonstrando o valor da otimização matemática.
#
# 2. **Trade-off revelado:** Adicionar um 3º veículo reduz a distância, mas o ganho
#    precisa ser comparado com o custo operacional adicional (motorista, combustível, manutenção).
#
# 3. **Gargalo escondido:** A capacidade dos veículos é a restrição que mais impacta
#    a distribuição dos clientes entre as rotas.
#
# 4. **Viabilidade:** Com apenas 1 veículo, dependendo da demanda total, o cenário
#    pode ser inviável — reforçando a necessidade da frota mínima de 2 veículos.
#
# **Limitações do modelo:**
# - Não considera trânsito, tempo de descarga ou janelas de horário
# - Distâncias euclidianas (linha reta), não distâncias reais de ruas
# - Dados fictícios — em produção, usar API de mapas (Google Maps, OSRM)
#
# **Próximos passos:**
# - Incluir janelas de tempo (VRPTW)
# - Usar distâncias reais via API
# - Testar com dados reais da operação
# - Avaliar heurísticas (Genetic Algorithm, Simulated Annealing) para instâncias maiores
