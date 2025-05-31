import matplotlib.pyplot as plt

# 1) Definições de modelo e dados iniciais
models_initial = {
    'Prosecutor': [68.40064, 100, 55.3279],
    'Journalist': [68.40064, 100, 55.3279],
    'Marketer':   [0.0,      0.0,   55.3279]
}
all_metrics = ['Records at Risk', 'Highest Risk', 'Success Rate']

# 2) Cores para cada métrica
metric_colors = {
    'Records at Risk': '#1f77b4',
    'Highest Risk':    '#ff7f0e',
    'Success Rate':    '#2ca02c'
}

for model_name, values in models_initial.items():
    # opcional: filtrar zeros (se quiser retirar métricas = 0)
    names, vals = zip(*[(m, v) for m, v in zip(all_metrics, values) if v > 0])

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(names, vals, color=[metric_colors[m] for m in names])

    ax.set_title(f'{model_name} — Cenário Inicial', fontsize=12, pad=10)
    ax.set_ylabel('Valor (%)')
    ax.set_ylim(0, max(vals) * 1.2)
    ax.tick_params(axis='x', rotation=45)

    for bar in ax.patches:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}',
                    xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
