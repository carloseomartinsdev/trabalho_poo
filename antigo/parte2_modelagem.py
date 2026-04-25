# %% [markdown]
# ## 5. Modelagem CVRP — Programação Inteira (PuLP)

# %%
clientes = list(range(1, N))  # [1, 2, ..., 10]
pontos = list(range(N))        # [0, 1, ..., 10]
veiculos = list(range(N_VEICULOS))  # [0, 1]

# Modelo
modelo = LpProblem("CVRP", LpMinimize)

# Variáveis de decisão: x[i][j][k] = 1 se veículo k vai de i para j
x = LpVariable.dicts("x", (pontos, pontos, veiculos), cat='Binary')

# Variáveis MTZ para eliminação de sub-rotas
u = LpVariable.dicts("u", (clientes, veiculos), lowBound=1, upBound=N_CLIENTES, cat='Continuous')

# FUNÇÃO OBJETIVO: minimizar distância total
modelo += lpSum(dist[i][j] * x[i][j][k] for i in pontos for j in pontos for k in veiculos if i != j)

# RESTRIÇÃO 1: cada cliente é visitado exatamente 1 vez
for j in clientes:
    modelo += lpSum(x[i][j][k] for i in pontos for k in veiculos if i != j) == 1

# RESTRIÇÃO 2: cada veículo sai do CD no máximo 1 vez
for k in veiculos:
    modelo += lpSum(x[0][j][k] for j in clientes) <= 1

# RESTRIÇÃO 3: cada veículo retorna ao CD no máximo 1 vez
for k in veiculos:
    modelo += lpSum(x[j][0][k] for j in clientes) <= 1

# RESTRIÇÃO 4: conservação de fluxo — se veículo k entra em j, ele sai de j
for k in veiculos:
    for j in clientes:
        modelo += lpSum(x[i][j][k] for i in pontos if i != j) == lpSum(x[j][i][k] for i in pontos if i != j)

# RESTRIÇÃO 5: capacidade do veículo
for k in veiculos:
    modelo += lpSum(demandas[j] * lpSum(x[i][j][k] for i in pontos if i != j) for j in clientes) <= CAPACIDADE

# RESTRIÇÃO 6: eliminação de sub-rotas (MTZ)
for k in veiculos:
    for i in clientes:
        for j in clientes:
            if i != j:
                modelo += u[i][k] - u[j][k] + N_CLIENTES * x[i][j][k] <= N_CLIENTES - 1

# %% [markdown]
# ## 6. Resolução

# %%
modelo.solve(PULP_CBC_CMD(msg=1))

print(f"Status: {LpStatus[modelo.status]}")
print(f"Distância total otimizada: {round(value(modelo.objective), 2)} km")

# %% [markdown]
# ## 7. Extração das Rotas

# %%
cores = ['green', 'purple']

def extrair_rotas(x, pontos, clientes, veiculos):
    rotas = {}
    for k in veiculos:
        rota = [0]
        atual = 0
        while True:
            proximo = None
            for j in pontos:
                if j != atual and value(x[atual][j][k]) and value(x[atual][j][k]) > 0.5:
                    proximo = j
                    break
            if proximo is None or proximo == 0:
                rota.append(0)
                break
            rota.append(proximo)
            atual = proximo
        rotas[k] = rota
    return rotas

rotas = extrair_rotas(x, pontos, clientes, veiculos)

for k in veiculos:
    carga = sum(demandas[i] for i in rotas[k] if i != 0)
    rota_nomes = ' → '.join(nomes[i] for i in rotas[k])
    dist_rota = sum(dist[rotas[k][i]][rotas[k][i+1]] for i in range(len(rotas[k])-1))
    print(f"Veículo {k+1}: {rota_nomes}")
    print(f"  Carga: {carga}/{CAPACIDADE} kg | Distância: {round(dist_rota, 2)} km\n")

# %% [markdown]
# ## 8. Visualização das Rotas Otimizadas

# %%
fig, ax = plt.subplots(figsize=(8, 8))

# CD
ax.scatter(*coordenadas[0], c='red', s=200, zorder=5, marker='s', label='CD')
ax.annotate('CD', coordenadas[0], textcoords="offset points", xytext=(8, 8), fontsize=10, fontweight='bold')

# Clientes
for i in clientes:
    ax.scatter(*coordenadas[i], c='steelblue', s=100, zorder=5)
    ax.annotate(f'{nomes[i]}\n({demandas[i]}kg)', coordenadas[i],
                textcoords="offset points", xytext=(8, 8), fontsize=8)

# Rotas
for k in veiculos:
    rota = rotas[k]
    for idx in range(len(rota) - 1):
        i, j = rota[idx], rota[idx + 1]
        ax.annotate('', xy=coordenadas[j], xytext=coordenadas[i],
                     arrowprops=dict(arrowstyle='->', color=cores[k], lw=2))
    carga = sum(demandas[i] for i in rota if i != 0)
    ax.plot([], [], color=cores[k], lw=2, label=f'Veículo {k+1} ({carga}kg)')

ax.set_title('Rotas Otimizadas — CVRP')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
