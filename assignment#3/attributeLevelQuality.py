import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Criando o DataFrame com os dados de Attribute-level Quality
attributes = [
    'sex', 'age', 'Marital-status', 'education',
    'Native-country', 'workclass', 'occupation'
]
data = {
    'Missings (%)':         [7.20774, 100.0, 100.0, 100.0, 7.20774, 7.20774, 100.0],
    'Gen. Intensity (%)':   [92.79226,   0.0,   0.0,   0.0,   92.79226,   46.39613,   0.0],
    'Granularity (%)':      [92.79226,   0.0,   0.0,   0.0,   92.79226,   66.28018,   0.0],
    'N.-U. entropy (%)':    [92.79226,   0.0,   0.0,   0.0,   62.55056,   39.56702,   0.0],
    'Squared Error (%)':    [92.79226,   0.0,   0.0,   0.0,   96.37,   82.1597,   0.0]
}
df_attr = pd.DataFrame(data, index=attributes)

# Plot do heatmap usando matplotlib
fig, ax = plt.subplots(figsize=(8, 5))
heatmap = ax.imshow(df_attr.values, interpolation='nearest', origin='lower', aspect='auto', cmap='viridis')

# Configuração dos ticks nos eixos
ax.set_xticks(np.arange(len(df_attr.columns)))
ax.set_yticks(np.arange(len(df_attr.index)))
ax.set_xticklabels(df_attr.columns, rotation=45, ha='right')
ax.set_yticklabels(df_attr.index)

# Anotações de valores em cada célula
for i in range(df_attr.shape[0]):
    for j in range(df_attr.shape[1]):
        ax.text(j, i, f"{df_attr.values[i, j]:.0f}", ha='center', va='center', color='white')

# Títulos e rótulos
ax.set_title('Attribute-level Quality Metrics for K=10 T=0.15')
ax.set_xlabel('Metrics')
ax.set_ylabel('Attributes')

# Colorbar
cbar = fig.colorbar(heatmap, ax=ax, label='Percentual (%)')

plt.tight_layout()
plt.show()
