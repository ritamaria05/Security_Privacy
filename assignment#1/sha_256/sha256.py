import os
import timeit
import hashlib
import matplotlib.pyplot as plt
import numpy as np

sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
std_dev = {}

#Gerar a hash SHA-256 
def calculate_sha256_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()


#Problemas com o windows para abrir as subpastas e econtrar o caminho correto
def find_correct_path():
    possible_paths = [
        os.path.join("sha_256", "text_files"),
        os.path.join("assignment#1", "sha_256", "text_files"),
        "text_files",
        os.path.abspath(os.path.join(".", "text_files"))
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Diretório text_files não encontrado")

def get_confidence_interval(data, confidence=0.95):
    # Parameters: confidence (float): The confidence level (default is 0.95).
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    se = std_dev / np.sqrt(n)
    
    # 95% confidence, using the normal distribution approximation: the z-score is 1.96.
    z = 1.96  
    margin_error = z * se
    return (mean - margin_error, mean + margin_error)

#Processar os ficheiros de um determinado tamanho
def process_files(base_dir, size):
    size_dir = os.path.join(base_dir, str(size))
    hash_times = []
    
    for i in range(1, 101):
        file_path = os.path.join(size_dir, f"{size}_{i}.txt")
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                file_data = file.read()
                
                timer = timeit.Timer(lambda: calculate_sha256_hash(file_data))
                hash_time = (timer.timeit(number=100) / 100) * 1000000
                hash_times.append(hash_time)

    confidenceHash = get_confidence_interval(hash_times)
    print(f"{size} bytes:\tHashing: ({confidenceHash[0]:.2f}, {confidenceHash[1]:.2f})")

    std_hash = np.std(hash_times, ddof=1)  # ddof=1 for sample std deviation
    std_dev[size] = std_hash
    # Gráfico de distribuição
    plt.figure(figsize=(10, 6))
    plt.text(0.75, 1.05, f"Std Dev: {std_hash:.2f}", fontsize=12, color='blue',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    tick_positions = range(0, 101, 10)  # Show ticks every 10 iterations
    plt.xticks(tick_positions)  # Set X-axis to display only 10th iterations
    # Set the width of the bars
    bar_width = 0.35
    index = range(1, len(hash_times) + 1)  # Indices for X-axis
    plt.bar([i - bar_width / 2 for i in index], hash_times, bar_width, label='Encryption Time', color='blue')
    plt.ylabel('Tempo de hash (µs)')
    plt.xlabel('Iterações')
    plt.title(f'Tempos de Hashing SHA ({size} bytes)')
    #plt.savefig(f'{file_name}_performance.png', dpi=120)
    plt.show()
    plt.close()

    return sum(hash_times)/len(hash_times) if hash_times else None


#Processa um arquivo específico para análise individual
def process_unique_file(file_name, size):
    base_dir = find_correct_path()
    file_path = os.path.join(base_dir, str(size), file_name)
    
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado!")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    hash_times = []
    for _ in range(100):
        timer = timeit.Timer(lambda: calculate_sha256_hash(data))
        hash_time = (timer.timeit(number=100) / 100) * 1000000
        hash_times.append(hash_time)

    # Resultados individuais
    #print(f"\nAnálise para o ficheiro {file_name}:")
    #print(f"Melhor tempo: {min(hash_times):.2f} µs")
    #print(f"Pior tempo: {max(hash_times):.2f} µs")
    #print(f"Média: {sum(hash_times)/len(hash_times):.2f} µs")

    # Gráfico de distribuição
    plt.figure(figsize=(10, 6))
    std_hash = np.std(hash_times, ddof=1)  # ddof=1 for sample std deviation
    # Gráfico de distribuição
    plt.figure(figsize=(10, 6))
    plt.text(0.75, 1.05, f"Std Dev: {std_hash:.2f}", fontsize=12, color='blue',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    tick_positions = range(0, 101, 10)  # Show ticks every 10 iterations
    plt.xticks(tick_positions)  # Set X-axis to display only 10th iterations
    # Set the width of the bars
    bar_width = 0.35
    index = range(1, len(hash_times) + 1)  # Indices for X-axis
    plt.bar([i - bar_width / 2 for i in index], hash_times, bar_width, label='Encryption Time', color='blue')
    plt.ylabel('Tempo de hash (µs)')
    plt.xlabel('Iterações')
    plt.title(f'Distribuição de tempos - {file_name}')
    #plt.savefig(f'{file_name}_performance.png', dpi=120)
    plt.show()
    plt.close()


#Desempenho gráfico da SHA-256
def plot_sha256_performance(results, std_devs):
    x_values = list(results.keys())
    y_values = list(results.values())
    std_values = list(std_devs.values())

    plt.figure(figsize=(12, 7))
    plt.plot(x_values, y_values, 'bo-', linewidth=2)
    plt.xscale('log')

# Add standard deviation as labels above each point
    for i, txt in enumerate(std_values):
        plt.annotate(f'{txt:.2f}', (x_values[i], y_values[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, color='red')

    
    plt.xlabel('Tamanho do arquivo (bytes)', fontsize=12)
    plt.ylabel('Tempo médio de hash (µs)', fontsize=12)
    plt.title('Desempenho do SHA-256 por Tamanho de Arquivo', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(x_values, [str(x) for x in x_values], rotation=45)

    plt.tight_layout()
    #plt.savefig('sha256_performance.png', dpi=300)
    plt.show()
    plt.close()

def main():
    base_dir = find_correct_path()
    results = {}    
    #Processamento dos ficheiros
    print("Confidence Intervals (microseconds) for SHA:")
    print("----------------------------------------------------------------------------")
    for size in sizes:
        size_path = os.path.join(base_dir, str(size))
        if os.path.exists(size_path):
            if avg_time := process_files(base_dir, size):
                results[size] = avg_time
    
    #Analise de ficheiro individual
    process_unique_file("4096_1.txt", 4096)
    
    plot_sha256_performance(results, std_dev)
    
    print("\nRESULTADOS GLOBAIS:")
    print(f"{'Tamanho':<10} | {'Média (µs)':<10}")
    print("-" * 25)
    for size, time in sorted(results.items()):
        print(f"{size:<10} | {time:.2f}")

if __name__ == "__main__":
    main()
