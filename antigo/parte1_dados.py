# %% [markdown]
# # Projeto Final — CVRP: Otimização de Rotas de Entrega
# **MBA em Ciência de Dados — UNIFOR**
# **Disciplina: Pesquisa Operacional e Otimização em IA**
#
# **Problema:** Uma empresa de logística possui 1 centro de distribuição e precisa
# atender 10 clientes usando 2 veículos com capacidade máxima de 500kg cada.
# **Objetivo:** Minimizar a distância total percorrida.

# %% [markdown]
# ## 1. Instalação e Imports

# %%
!pip install pulp matplotlib numpy -q

# %%
import numpy as np
import matplotlib.pyplot as plt
from pulp import *
import random

random.seed(42)
np.random.seed(42)

# %% [markdown]
# ## 2. Geração dos Dados Fictícios

# %%
N_CLIENTES = 10
N_VEICULOS = 2
CAPACIDADE = 500  # kg por veículo

# Ponto 0 = Centro de Distribuição (CD), pontos 1-10 = clientes
nomes = ['CD'] + [f'C{i}' for i in range(1, N_CLIENTES + 1)]

# Coordenadas (x, y) em km — CD no centro
coordenadas = [(50, 50)]  # CD
for _ in range(N_CLIENTES):
    coordenadas.append((random.randint(0, 100), random.randint(0, 100)))

# Demanda de cada cliente (kg) — CD tem demanda 0
demandas = [0] + [random.randint(40, 150) for _ in range(N_CLIENTES)]

print("=" * 50)
print(f"{'Ponto':<6} {'Coord (x,y)':<16} {'Demanda (kg)'}")
print("=" * 50)
for i, nome in enumerate(nomes):
    print(f"{nome:<6} {str(coordenadas[i]):<16} {demandas[i]}")
print("=" * 50)
print(f"Demanda total: {sum(demandas)} kg")
print(f"Capacidade total frota: {N_VEICULOS * CAPACIDADE} kg")

# %% [markdown]
# ## 3. Matriz de Distâncias

# %%
N = len(coordenadas)  # 11 pontos (CD + 10 clientes)

def distancia(p1, p2):
    return round(np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2), 2)

dist = [[distancia(coordenadas[i], coordenadas[j]) for j in range(N)] for i in range(N)]

# %% [markdown]
# ## 4. Visualização dos Pontos

# %%
fig, ax = plt.subplots(figsize=(8, 8))

# CD
ax.scatter(*coordenadas[0], c='red', s=200, zorder=5, marker='s', label='CD')
ax.annotate('CD', coordenadas[0], textcoords="offset points", xytext=(8, 8), fontsize=10, fontweight='bold')

# Clientes
for i in range(1, N):
    ax.scatter(*coordenadas[i], c='steelblue', s=100, zorder=5)
    ax.annotate(f'{nomes[i]}\n({demandas[i]}kg)', coordenadas[i],
                textcoords="offset points", xytext=(8, 8), fontsize=8)

ax.set_title('Localização dos Clientes e Centro de Distribuição')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
