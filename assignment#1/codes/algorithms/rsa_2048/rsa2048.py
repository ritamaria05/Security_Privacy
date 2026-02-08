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

# Calculate and return the confidence interval for the given data.
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
            #print(f"{filename:<8} | {size:<12} | {enc_time:.9f}         | {dec_time:.6f}")
    
    confidenceEnc = get_confidence_interval(arrayEnc)
    confidenceDec = get_confidence_interval(arrayDec)
    print(f"{size} bytes:\tEncryption: ({confidenceEnc[0]:.2f}, {confidenceEnc[1]:.2f})\tDecryption: ({confidenceDec[0]:.2f}, {confidenceDec[1]:.2f})")


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
    #print(f"{file:<8}:")
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
        #print(f"Encryption Time: {arrayEnc[i]:.9f} s | Decryption Time: {arrayDec[i]:.6f} s")
    plot_results(arrayEnc, arrayDec, file)

def plot_results(arrayEnc, arrayDec, file): # works well
    plt.figure(figsize=(12, 8))
    # Set the width
    bar_width = 1
    index = range(1, len(arrayEnc) + 1)  # Indices for X-axis
    
    # Plot the lines
    plt.plot([i - bar_width / 2 for i in index], arrayEnc, '-', linewidth=2, color='blue', label='Encryption Time')
    plt.plot([i - bar_width / 2 for i in index], arrayDec, '-', linewidth=2, color='red',label='Decryption Time')

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

    # Display both standard deviations below the title and above the bars
    plt.text(0.25, 1.05, f"Std Dev (Encryption): {std_enc:.2f}", fontsize=12, color='blue',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    
    plt.text(0.75, 1.05, f"Std Dev (Decryption): {std_dec:.2f}", fontsize=12, color='red',
             verticalalignment='bottom', horizontalalignment='center', transform=plt.gca().transAxes)
    # Display the plot
    plt.show()


# plot to show times for each size folder 
def plot_graph(results):
    # Loop através dos resultados para cada pasta/tamanho
    for folder_size, times in results.items():
        # Criar um novo gráfico para cada tamanho de pasta
        plt.figure(figsize=(12, 8))  # Definir o tamanho da figura

        bar_width = 1
        index = range(1, len(times['encryption_time']) + 1)  # Indices for X-axis
        # Plotando o tempo de encriptação
        plt.plot([i - bar_width / 2 for i in index], times['encryption_time'], '-', linewidth=2, color='blue', label='Encryption Time')
        
        # Plotando o tempo de decriptação
        plt.plot([i - bar_width / 2 for i in index], times['decryption_time'], '-', linewidth=2, color='red', label='Decryption Time')
        
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

    for s in sizes:
        avg_enc = sum(results[s]['encryption_time']) / len(results[s]['encryption_time'])
        avg_dec = sum(results[s]['decryption_time']) / len(results[s]['decryption_time'])
        # Calculate the standard deviation for encryption and decryption times
        avg_enc_times.append(avg_enc)
        avg_dec_times.append(avg_dec)


    plt.figure(figsize=(12, 8))
    
    # Line plot for encryption and decryption times
    plt.plot(sizes, avg_enc_times, marker='o', color='blue', label='Encryption Time')
    plt.plot(sizes, avg_dec_times, marker='x', color='red', label='Decryption Time')

    # Adding labels and title
    plt.xscale('log')  # 'log' for better visualization
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for RSA")
    plt.xticks(sizes, [str(x) for x in sizes])
    # Display the bars and the legend
    plt.legend()
    plt.show()



def main():
    # Print results of an unique file
    process_unique("64_5.txt",64)
    # Process results for each folder
    #print("Filename | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    print("Confidence Intervals (microseconds) for RSA:")
    print("----------------------------------------------------------------------------")
    for size in sizes:
        process_all_files(size)
    # Print a graph for each size folder
    plot_graph(results)
    # Print a graph for the average of each size folder
    plot_graph_avg(results)
    
if __name__ == "__main__":
    main()
