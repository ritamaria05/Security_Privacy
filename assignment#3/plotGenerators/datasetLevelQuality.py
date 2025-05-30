import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    """
    Plots a heatmap using matplotlib for a given DataFrame.
    - df: DataFrame where rows are heatmap y-axis (e.g., quality metrics)
          and columns are heatmap x-axis (e.g., parameter values).
    - title: Title of the plot.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    """
    plt.figure(figsize=(8, 5))
    plt.imshow(df.values, interpolation='nearest', origin='lower', aspect='auto')
    plt.xticks(range(len(df.columns)), df.columns)
    plt.yticks(range(len(df.index)), df.index)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar(label='Value (%)')
    plt.tight_layout()
    plt.show()

# 1) Cria o DataFrame para suppression limit
data_sup = {
    'k=3, l=2': [9.07627, 12.13012,7.22233, 15.46884, 99.76286, 7.62272,10.64182, 0.0],
    'k=5, l=4': [0.0,0.0, 0.0, np.nan, np.nan,0.0, 0.0, 0.0],
    'k=10, l=2': [58.92237, 62.76138,35.10996, 83.39336, 99.50102,41.7976,30.98822, 0.0]
}
index_sup = [
    'Gen-Intensity',
    'Granularity',
    'N.-U. entropy',
    'Discernibility',
    'Avg Eq Class Size',
    'Record-level MSE',
    'Attribute-level MSE',
    'Aggregation-specific MSE'
]
df_sup = pd.DataFrame(data_sup, index=index_sup)

# 2) Exibe o heatmap
plot_heatmap(
    df_sup,
    title='Quality vs. Configuração (k,l)',
    xlabel='Configuração (k,l)',
    ylabel='Quality Metric'
)
