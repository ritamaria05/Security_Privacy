import os
import timeit
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# folder of random text files for RSA
folder_path = "text_files"

sizes = [2,4,8,16,32,64,128]

# Generate RSA Key Pair (2048-bit)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Function to encrypt data
def encrypt_data(data):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Function to decrypt data
def decrypt_data(encrypted_data):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


results = {}

# Process all files in each size folder
def process_all_files(size):
    arrayEnc = [0]*100
    arrayDec = [0]*100
    results[size] = {'encryption_time': [], 'decryption_time': []}
    for i in range(1,101):
        file_path = os.path.join("text_files", str(size), str(size)+"_"+str(i)+".txt")

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                data = f.read()

            # Measure encryption time
            enc_time = (timeit.timeit(lambda: encrypt_data(data), number=100) / 100)* 1_000_000 
            encrypted_data = encrypt_data(data)
            arrayEnc[i-1] = enc_time
            # Measure decryption time
            dec_time = (timeit.timeit(lambda: decrypt_data(encrypted_data), number=100) / 100)* 1_000_000
            arrayDec[i-1] = dec_time
            # Store results
            results[size]['encryption_time'].append(enc_time)
            results[size]['decryption_time'].append(dec_time)
            filename = str(size) + "_" + str(i) + ".txt"
            print(f"{filename:<8} | {size:<12} | {enc_time:.9f}         | {dec_time:.6f}")


# Process an unique file to see its variations in time
            
def process_unique(file,size):
    file_path = os.path.join("text_files", str(size), file)
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} not found.")
        return
    # Read the file only once
    with open(file_path, "rb") as f:
        data = f.read()
    # Arrays to store encryption and decryption times
    arrayEnc = []
    arrayDec = []
    print(f"{file:<8}:")
    for i in range(100):  # Run 100 times for accuracy
        try:
            # Measure encryption time
            enc_time = (timeit.timeit(lambda: encrypt_data(data), number=100) / 100)* 1_000_000
            encrypted_data = encrypt_data(data)
        except Exception as e:
            print(f"Error encrypting {file}: {e}")
            continue
        arrayEnc.append(enc_time)
        try:
            # Measure decryption time
            dec_time = (timeit.timeit(lambda: decrypt_data(encrypted_data), number=100) / 100)* 1_000_000
        except Exception as e:
            print(f"Error decrypting {file}: {e}")
            continue
        arrayDec.append(dec_time)
    # Print averaged results
        print(f"Encryption Time: {arrayEnc[i]:.9f} s | Decryption Time: {arrayDec[i]:.6f} s")
    
    plot_results(arrayEnc, arrayDec, file)

def plot_results(arrayEnc, arrayDec, file): # works well
    # Create a figure
    plt.figure(figsize=(10, 6))

    # Set the width of the bars
    bar_width = 0.35
    index = range(1, len(arrayEnc) + 1)  # Indices for X-axis
    
    # Plot the encryption and decryption times as bar charts
    plt.bar([i - bar_width / 2 for i in index], arrayEnc, bar_width, label='Encryption Time', color='blue')
    plt.bar([i + bar_width / 2 for i in index], arrayDec, bar_width, label='Decryption Time', color='red', alpha=0.6)

    std_enc = np.std(arrayEnc, ddof=1)  # ddof=1 for sample std deviation
    std_dec = np.std(arrayDec, ddof=1)  # ddof=1 for sample std deviation

    # Adding labels and title

    plt.xlabel('Iteration')
    plt.ylabel('Time (microseconds)')
    plt.title(f"RSA Encryption and Decryption Times for {file}")
    
    # Set X-axis labels to the index of iterations
    tick_positions = range(0, 101, 10)  # Show ticks every 10 iterations
    plt.xticks(tick_positions)  # Set X-axis to display only 10th iterations
    plt.legend(loc='upper right')

    # Get the max x-axis value for proper alignment
    max_x = len(arrayEnc)  # Assuming both lists have the same length
    y_offset = max(arrayEnc) * 0.1  # Adjust vertical spacing dynamically

    # Display both standard deviations below the title and above the bars
    plt.text(0.25, 1.05, f"Std Dev (Encryption): {std_enc:.2f}", fontsize=12, color='blue',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    
    plt.text(0.75, 1.05, f"Std Dev (Decryption): {std_dec:.2f}", fontsize=12, color='red',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    # Display the plot
    plt.show()

# Define a list of 14 colors (hex codes or named colors)
colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf',  # blue-teal
    '#aec7e8',  # light blue
    '#ffbb78',  # light orange
    '#98df8a',  # light green
    '#ff9896'   # light red
]

# plot to show times for each size folder 
def plot_graph(results):
    # Loop através dos resultados para cada pasta/tamanho
    for folder_size, times in results.items():
        # Criar um novo gráfico para cada tamanho de pasta
        plt.figure(figsize=(12, 8))  # Definir o tamanho da figura

        # Eixo X: Índices dos arquivos
        x_axis = range(1, len(times['encryption_time']) + 1)  # Índice dos arquivos (1 a N)

        # Largura da barra
        bar_width = 0.35
        
        # Plotando o tempo de encriptação
        plt.bar([i - bar_width / 2 for i in x_axis], times['encryption_time'], bar_width, label='Encryption Time', color='blue')
        
        # Plotando o tempo de decriptação
        plt.bar([i + bar_width / 2 for i in x_axis], times['decryption_time'], bar_width, label='Decryption Time', color='red', alpha=0.6)
        
        # Calculate the standard deviation for encryption and decryption times
        std_enc = np.std(times['encryption_time'], ddof=1)
        std_dec = np.std(times['decryption_time'], ddof=1)

        # Ajustar os rótulos e título para o gráfico
        plt.xlabel('File Index')
        plt.ylabel('Time (Microseconds)')
        plt.title(f"Encryption and Decryption Times for RSA ({folder_size} bytes)")
        
        # Definir os ticks no eixo X para mostrar a cada 10 arquivos
        tick_positions = range(0, 101, 10)  # Mostrar ticks a cada 10 iterações
        plt.xticks(tick_positions)
        
        # Adicionar a legenda
        plt.legend()

        # Display both standard deviations below the title and above the bars
        plt.text(0.25, 1.05, f"Std Dev (Encryption): {std_enc:.2f}", fontsize=12, color='blue',
                verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
        
        plt.text(0.75, 1.05, f"Std Dev (Decryption): {std_dec:.2f}", fontsize=12, color='red',
                verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)

        # Exibir o gráfico
        plt.show()
    

# plot to show average times for each size files

def plot_graph_avg(results): # works well, corrigir avg dec 
    # For each size, compute the average encryption and decryption time
    sizes = sorted(results.keys())
    avg_enc_times = []
    avg_dec_times = []
    std_enc_times = []
    std_dec_times = []
    
    for s in sizes:
        avg_enc = sum(results[s]['encryption_time']) / len(results[s]['encryption_time'])
        avg_dec = sum(results[s]['decryption_time']) / len(results[s]['decryption_time'])
        # Calculate the standard deviation for encryption and decryption times
        std_enc = np.std(results[s]['encryption_time'], ddof=1)
        std_dec = np.std(results[s]['decryption_time'], ddof=1)
        avg_enc_times.append(avg_enc)
        avg_dec_times.append(avg_dec)
        std_enc_times.append(std_enc)
        std_dec_times.append(std_dec)

    plt.figure(figsize=(12, 8))

    # Set the width of the bars
    bar_width = 0.35
    index = range(len(sizes))  # Indices for X-axis
    
    # Plot the bars for encryption and decryption times
    plt.bar([i - bar_width / 2 for i in index], avg_enc_times, bar_width, label='Encryption Time', color='blue')
    plt.bar([i + bar_width / 2 for i in index], avg_dec_times, bar_width, label='Decryption Time', color='red')
    
    # Display the standard deviation as text on the plot (just like in the other function)
    y_offset = max(max(avg_enc_times), max(avg_dec_times)) * 0.1  # Adjust vertical spacing

    # Add standard deviation text for encryption and decryption times
    for i, (std_enc, std_dec) in enumerate(zip(std_enc_times, std_dec_times)):
        plt.text(i - bar_width / 2, avg_enc_times[i] + y_offset, f"Std Dev: {std_enc:.2f}", 
                 fontsize=10, color='blue', verticalalignment='bottom', horizontalalignment='center')
        plt.text(i + bar_width / 2, avg_dec_times[i] + y_offset, f"Std Dev: {std_dec:.2f}", 
                 fontsize=10, color='red', verticalalignment='bottom', horizontalalignment='center')

    # Adding labels and title
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for RSA")

    # Set the X-axis positions to the indices of sizes
    plt.xticks(index, sizes)  # Use the actual size values as x-axis labels

    # Display the bars and the legend
    plt.legend()
    plt.show()



def main():
    # Print results of an unique file
    process_unique("64_5.txt",64)
    # Process results for each folder
    print("Filename | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    for size in sizes:
        process_all_files(size)
    # Print a graph for each size folder
    plot_graph(results)
    # Print a graph for the average of each size folder
    plot_graph_avg(results)
    
if __name__ == "__main__":
    main()
