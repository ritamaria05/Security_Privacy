import os
import timeit
import hashlib
import matplotlib.pyplot as plt

sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

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
                hash_time = (timer.timeit(number=100) / 100) * 1e6
                hash_times.append(hash_time)
            break
    
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
        hash_time = (timer.timeit(number=1000) / 1000) * 1e6
        hash_times.append(hash_time)

    # Resultados individuais
    print(f"\nAnálise para o ficheiro {file_name}:")
    print(f"Melhor tempo: {min(hash_times):.2f} µs")
    print(f"Pior tempo: {max(hash_times):.2f} µs")
    print(f"Média: {sum(hash_times)/len(hash_times):.2f} µs")

    # Gráfico de distribuição
    plt.figure(figsize=(10, 6))
    plt.hist(hash_times, bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Tempo de hash (µs)')
    plt.ylabel('Frequência')
    plt.title(f'Distribuição de tempos - {file_name}')
    plt.savefig(f'{file_name}_performance.png', dpi=120)
    plt.show()
    plt.close()


#Desempenho gráfico da SHA-256
def plot_sha256_performance(results):
    x_values = list(results.keys())
    y_values = list(results.values())

    plt.figure(figsize=(12, 7))
    plt.plot(x_values, y_values, 'bo-', linewidth=2)
    plt.xscale('log')

    
    plt.xlabel('Tamanho do arquivo (bytes)', fontsize=12)
    plt.ylabel('Tempo médio de hash (µs)', fontsize=12)
    plt.title('Desempenho do SHA-256 por Tamanho de Arquivo', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(x_values, [str(x) for x in x_values], rotation=45)

    plt.tight_layout()
    plt.savefig('sha256_performance.png', dpi=300)
    plt.show()
    plt.close()

def main():
    base_dir = find_correct_path()
    results = {}
    
    #Processamento dos ficheiros
    for size in sizes:
        size_path = os.path.join(base_dir, str(size))
        if os.path.exists(size_path):
            if avg_time := process_files(base_dir, size):
                results[size] = avg_time
    
    #Analise de ficheiro individual
    process_unique_file("4096_1.txt", 4096)
    
    plot_sha256_performance(results)
    
    print("\nRESULTADOS GLOBAIS:")
    print(f"{'Tamanho':<10} | {'Média (µs)':<10}")
    print("-" * 25)
    for size, time in sorted(results.items()):
        print(f"{size:<10} | {time:.2f}")

if __name__ == "__main__":
    main()
