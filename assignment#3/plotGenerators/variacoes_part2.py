import matplotlib.pyplot as plt

# 1) Definições de cenário e dados
scenarios = ['10%', '50%', '100%']
metrics = {
    'Records at Risk (%)': {
        'Prosecutor':  [0, 0, 0],
        'Journalist':  [0, 0, 0],
        'Marketer':    [0, 0, 0],
    },
    'Highest Risk (%)': {
        'Prosecutor':  [0.05811, 0.05811, 0.05811],
        'Journalist':  [0.05811, 0.05811, 0.05811],
        'Marketer':    [0, 0, 0],
    },
    'Success Rate (%)': {
        'Prosecutor':  [0.01697, 0.01697, 0.01697],
        'Journalist':  [0.01697, 0.01697, 0.01697],
        'Marketer':    [0.01697, 0.01697, 0.01697],
    }
}

# 2) Estilos para cada modelo
styles = {
    'Prosecutor': {'marker':'o', 'linestyle':'-', 'color':'blue'},
    'Journalist': {'marker':'s', 'linestyle':'--','color':'green'},
    'Marketer':   {'marker':'d', 'linestyle':'-.','color':'red'},
}

# 3) Loop que gera um gráfico por métrica, filtrando modelos com todos valores zero
for metric_name, data in metrics.items():
    fig, ax = plt.subplots(figsize=(6, 4))
    for model, values in data.items():
        # pula se todos os valores forem zero
        if all(v == 0 for v in values):
            continue
        ax.plot(scenarios, values,
                label=model,
                marker=styles[model]['marker'],
                linestyle=styles[model]['linestyle'],
                color=styles[model]['color'])
    ax.set_title(metric_name, fontsize=12, pad=10)
    ax.set_xlabel('Suppression Limit')
    ax.set_ylabel(metric_name)
    ax.set_xticks(range(len(scenarios)))
    ax.set_xticklabels(scenarios, rotation=0, ha='center')
    ax.tick_params(axis='x', rotation=0)
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()
