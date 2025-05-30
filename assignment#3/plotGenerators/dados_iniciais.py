import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1) Definições de modelo e dados iniciais
all_models = ['Prosecutor', 'Journalist', 'Marketer']
metrics_initial = {
    'Records at Risk (%)': [68.40064, 68.40064, 0.0],
    'Highest Risk (%)':   [100.0,    100.0,    0.0],
    'Success Rate (%)':   [55.3279,  55.3279,  55.3279]
}

# 2) Thresholds por métrica
thresholds = {
    'Records at Risk (%)': 5,
    'Highest Risk (%)':   20,
    'Success Rate (%)':    5
}

# 3) Palette suave para barras (sem legenda)
model_colors = {
    'Prosecutor': '#1f77b4',
    'Journalist': '#ff7f0e',
    'Marketer':   '#2ca02c'
}
threshold_color = '#d62728'

# 4) Loop para gerar gráficos com apenas a legenda de threshold
for metric_name, values in metrics_initial.items():
    # Filtra modelos com valores > 0
    models = [m for m, v in zip(all_models, values) if v > 0]
    vals   = [v for v in values if v > 0]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    # Plot das barras
    ax.bar(models, vals, color=[model_colors[m] for m in models])
    
    # Configurações do gráfico
    ax.set_title(f'{metric_name} — Cenário Inicial', fontsize=12, pad=10)
    ax.set_ylabel(metric_name)
    ax.set_ylim(0, max(vals + [thresholds[metric_name]]) * 1.2)
    ax.tick_params(axis='x', rotation=45)
    
    # Desenha threshold e adiciona mini-legenda
    th = thresholds[metric_name]
    line = ax.axhline(th, color=threshold_color, linestyle='--', linewidth=1)
    legend_handle = [Line2D([0], [0], color=threshold_color, linestyle='--')]
    ax.legend(legend_handle, ['Threshold'], loc='best')
    
    # Anota valores nas barras
    for bar in ax.patches:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}',
                    xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()
