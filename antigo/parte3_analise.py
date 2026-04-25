# %% [markdown]
# ## 9. Comparação: Rota Manual vs Otimizada

# %%
# Rota manual: distribuir clientes sequencialmente entre os veículos
clientes_shuffled = list(clientes)
random.shuffle(clientes_shuffled)
meio = len(clientes_shuffled) // 2
rota_manual = {
    0: [0] + clientes_shuffled[:meio] + [0],
    1: [0] + clientes_shuffled[meio:] + [0]
}

def calcular_distancia_rota(rota):
    return sum(dist[rota[i]][rota[i+1]] for i in range(len(rota)-1))

dist_manual = sum(calcular_distancia_rota(rota_manual[k]) for k in veiculos)
dist_otimizada = round(value(modelo.objective), 2)
economia = round((1 - dist_otimizada / dist_manual) * 100, 1)

print("=" * 55)
print("COMPARAÇÃO: ROTA MANUAL vs OTIMIZADA")
print("=" * 55)
for k in veiculos:
    print(f"\nRota Manual Veículo {k+1}: {' → '.join(nomes[i] for i in rota_manual[k])}")
    print(f"  Distância: {round(calcular_distancia_rota(rota_manual[k]), 2)} km")
for k in veiculos:
    print(f"\nRota Otimizada Veículo {k+1}: {' → '.join(nomes[i] for i in rotas[k])}")
    print(f"  Distância: {round(calcular_distancia_rota(rotas[k]), 2)} km")
print(f"\n{'─' * 55}")
print(f"Distância total MANUAL:    {round(dist_manual, 2)} km")
print(f"Distância total OTIMIZADA: {dist_otimizada} km")
print(f"Economia: {economia}%")
print("=" * 55)

# %%
# Gráfico comparativo
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

for ax, titulo, rotas_plot in [(axes[0], 'Rota Manual', rota_manual), (axes[1], 'Rota Otimizada', rotas)]:
    ax.scatter(*coordenadas[0], c='red', s=200, zorder=5, marker='s')
    ax.annotate('CD', coordenadas[0], textcoords="offset points", xytext=(8, 8), fontsize=10, fontweight='bold')
    for i in clientes:
        ax.scatter(*coordenadas[i], c='steelblue', s=100, zorder=5)
        ax.annotate(nomes[i], coordenadas[i], textcoords="offset points", xytext=(8, 8), fontsize=8)
    for k in veiculos:
        rota = rotas_plot[k]
        for idx in range(len(rota) - 1):
            i, j = rota[idx], rota[idx + 1]
            ax.annotate('', xy=coordenadas[j], xytext=coordenadas[i],
                         arrowprops=dict(arrowstyle='->', color=cores[k], lw=2))
    d = round(sum(calcular_distancia_rota(rotas_plot[k]) for k in veiculos), 2)
    ax.set_title(f'{titulo}\nDistância total: {d} km')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 10. Análise de Sensibilidade

# %% [markdown]
# ### Cenário A: 3 veículos em vez de 2

# %%
def resolver_cvrp(n_veiculos, coords, dem, cap, nomes_pontos):
    n = len(coords)
    cli = list(range(1, n))
    pts = list(range(n))
    veics = list(range(n_veiculos))
    d = [[distancia(coords[i], coords[j]) for j in range(n)] for i in range(n)]

    m = LpProblem(f"CVRP_{n_veiculos}v", LpMinimize)
    xv = LpVariable.dicts("x", (pts, pts, veics), cat='Binary')
    uv = LpVariable.dicts("u", (cli, veics), lowBound=1, upBound=len(cli), cat='Continuous')

    m += lpSum(d[i][j] * xv[i][j][k] for i in pts for j in pts for k in veics if i != j)

    for j in cli:
        m += lpSum(xv[i][j][k] for i in pts for k in veics if i != j) == 1
    for k in veics:
        m += lpSum(xv[0][j][k] for j in cli) <= 1
        m += lpSum(xv[j][0][k] for j in cli) <= 1
    for k in veics:
        for j in cli:
            m += lpSum(xv[i][j][k] for i in pts if i != j) == lpSum(xv[j][i][k] for i in pts if i != j)
    for k in veics:
        m += lpSum(dem[j] * lpSum(xv[i][j][k] for i in pts if i != j) for j in cli) <= cap
    for k in veics:
        for i in cli:
            for j in cli:
                if i != j:
                    m += uv[i][k] - uv[j][k] + len(cli) * xv[i][j][k] <= len(cli) - 1

    m.solve(PULP_CBC_CMD(msg=0))
    rotas_r = extrair_rotas(xv, pts, cli, veics)
    return m, rotas_r

modelo_3v, rotas_3v = resolver_cvrp(3, coordenadas, demandas, CAPACIDADE, nomes)
dist_3v = round(value(modelo_3v.objective), 2)

print(f"Distância com 2 veículos: {dist_otimizada} km")
print(f"Distância com 3 veículos: {dist_3v} km")
print(f"Redução: {round((1 - dist_3v / dist_otimizada) * 100, 1)}%")
print(f"\nCompensa adicionar 1 veículo? Depende do custo operacional vs economia de {round(dist_otimizada - dist_3v, 2)} km")

# %% [markdown]
# ### Cenário B: +1 cliente novo

# %%
coord_novo = (random.randint(0, 100), random.randint(0, 100))
demanda_novo = random.randint(40, 150)
coords_11 = coordenadas + [coord_novo]
demandas_11 = demandas + [demanda_novo]
nomes_11 = nomes + ['C11']

print(f"Novo cliente C11: coordenadas {coord_novo}, demanda {demanda_novo}kg")

modelo_11c, rotas_11c = resolver_cvrp(2, coords_11, demandas_11, CAPACIDADE, nomes_11)
dist_11c = round(value(modelo_11c.objective), 2)

print(f"\nDistância com 10 clientes: {dist_otimizada} km")
print(f"Distância com 11 clientes: {dist_11c} km")
print(f"Aumento: {round((dist_11c / dist_otimizada - 1) * 100, 1)}%")

# %% [markdown]
# ### Cenário C: apenas 1 veículo

# %%
# Verificar se a demanda total cabe em 1 veículo
demanda_total = sum(demandas)
print(f"Demanda total: {demanda_total}kg | Capacidade 1 veículo: {CAPACIDADE}kg")

if demanda_total > CAPACIDADE:
    print(f"\n⚠️ INVIÁVEL! Demanda total ({demanda_total}kg) excede capacidade de 1 veículo ({CAPACIDADE}kg)")
    print("Isso demonstra que a frota de 2 veículos é necessária.")
else:
    modelo_1v, rotas_1v = resolver_cvrp(1, coordenadas, demandas, CAPACIDADE, nomes)
    dist_1v = round(value(modelo_1v.objective), 2)
    print(f"\nDistância com 2 veículos: {dist_otimizada} km")
    print(f"Distância com 1 veículo:  {dist_1v} km")
    print(f"Aumento: {round((dist_1v / dist_otimizada - 1) * 100, 1)}%")
