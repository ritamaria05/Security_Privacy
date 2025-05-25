import matplotlib.pyplot as plt

# 1) Definições de cenário e dados
scenarios = ['k=3,l=2', 'k=5,l=4', 'k=10,l=2']
metrics = {
    'Records at Risk (%)': {
        'Prosecutor':  [0.21308, 0, 0],
        'Journalist':  [0.21308, 0, 0],
        'Marketer':    [0, 0, 0],
    },
    'Highest Risk (%)': {
        'Prosecutor':  [33.33333, 0, 10],
        'Journalist':  [33.33333, 0, 10],
        'Marketer':    [0, 0, 0],
    },
    'Success Rate (%)': {
        'Prosecutor':  [1.36373, 0, 0.65659],
        'Journalist':  [1.36373, 0, 0.65659],
        'Marketer':    [1.36373, 0, 0.65659],
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
    ax.set_xlabel('Configuração (k, l)')
    ax.set_ylabel(metric_name)
    ax.set_xticks(scenarios)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()
