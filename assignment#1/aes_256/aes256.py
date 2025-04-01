#-- in progress - Max :) --#
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
import os
import timeit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
results = {}
key = os.urandom(32) # key of 32 bytes (256 bits)

# create directories for encryption and decryption files
'''encrypt_dir = "encrypted_files"
decrypt_dir = "decrypted_files"
os.makedirs(encrypt_dir, exist_ok=True)
os.makedirs(decrypt_dir, exist_ok=True)'''

def encrypt(data, size, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # bytes have to be a multiple of 16... if not add padding
    if size % 16 != 0:
        # Pad the data to the AES block size (128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return ct
    else:
        ct = encryptor.update(data) + encryptor.finalize()
        return ct


def decrypt(ciphertext, size, iv):
    # if not a size multiple of 16 it will have padding to be removed
    if size % 16 != 0:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data
    else:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        data = decryptor.update(ciphertext) + decryptor.finalize()
        return data

    
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

def processAllFiles(size):
    arrEnc = [0] * 100  # Array to store encryption times for 100 files
    arrDec = [0] * 100  # Array to store decryption times for 100 files
    for i in range(1, 101):
        file_path = os.path.join("text_files", str(size), f"{size}_{i}.txt")
        with open(file_path, "rb") as file:
            plaintext = file.read()
        iv = os.urandom(16)  # IV has to be 16 bytes

        # Encrypt and time encryption
        encrypt_timer = timeit.Timer(lambda: encrypt(plaintext, size, iv))
        enc_time = (encrypt_timer.timeit(number=100) / 100) * 1000000
        arrEnc[i - 1] = enc_time

        ciphertext = encrypt(plaintext, size, iv)
        '''out_path = os.path.join(encrypt_dir, f"{size}.bin")
        with open(out_path, "wb") as f:
            f.write(ciphertext)'''

        # Decrypt and time decryption
        decrypt_timer = timeit.Timer(lambda: decrypt(ciphertext, size, iv))
        dec_time = (decrypt_timer.timeit(number=100) / 100) * 1000000
        arrDec[i - 1] = dec_time

        '''decrypted_text = decrypt(ciphertext, size, iv)
        out_path = os.path.join(decrypt_dir, f"{size}.txt")
        with open(out_path, "w") as f:
            f.write(decrypted_text.decode('utf-8'))'''

        filename = f"{size}_{i}.txt"
        #print(f"{filename:<11} | {size:<12} | {enc_time:.9f}         | {dec_time:.9f}")

    confidenceEnc = get_confidence_interval(arrEnc)
    confidenceDec = get_confidence_interval(arrDec)
    print(f"{size} bytes:\tEncryption: ({confidenceEnc[0]:.2f}, {confidenceEnc[1]:.2f})\tDecryption: ({confidenceDec[0]:.2f}, {confidenceDec[1]:.2f})")
    # Store all times for the given size
    results[size] = {'encryption_time': arrEnc, 'decryption_time': arrDec}

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
        plt.title(f"Encryption and Decryption Times for AES ({folder_size} bytes)")
        
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

def plot_graph_avg(results):
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

    # Scatter plot for encryption and decryption times
    plt.scatter(sizes, avg_enc_times, marker='o', color='blue', label='Encryption Time (Bottom Right Label)')
    plt.scatter(sizes, avg_dec_times, marker='x', color='red', label='Decryption Time (Top Left Label)')
    
    # Add coordinate labels to each point
    for x, y, std in zip(sizes, avg_enc_times, std_enc_times):
        plt.text(x, y, f"({x}, {y:.2f})", fontsize=9, verticalalignment='bottom', horizontalalignment='right')
        plt.text(x, y + std+150, f"Std Dev: {std:.2f}", fontsize=9, color='blue', verticalalignment='bottom', horizontalalignment='center')

    for x, y, std in zip(sizes, avg_dec_times, std_dec_times):
        plt.text(x, y, f"({x}, {y:.2f})", fontsize=9, verticalalignment='top', horizontalalignment='left')
        plt.text(x, y + std+50, f"Std Dev: {std:.2f}", fontsize=9, color='red', verticalalignment='bottom', horizontalalignment='center')

    # Use a logarithmic scale for the x-axis
    plt.xscale('log')  # 'log' for better visualization
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for AES")
    plt.legend()
    plt.show()

def plot_graph_avg_bar(results):
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
        plt.text(i + bar_width / 2, avg_dec_times[i] + y_offset-100, f"Std Dev: {std_dec:.2f}", 
                 fontsize=10, color='red', verticalalignment='bottom', horizontalalignment='center')

    # Adding labels and title
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for AES")

    # Set the X-axis positions to the indices of sizes
    plt.xticks(index, sizes)  # Use the actual size values as x-axis labels

    # Display the bars and the legend
    plt.legend()
    plt.show()

def processUnique(file,size):
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
    for i in range(100):
        with open(file_path, "rb") as f:
            plaintext = f.read()
        iv = os.urandom(16)  # IV has to be 16 bytes
        # Encrypt and time encryption
        encrypt_timer = timeit.Timer(lambda: encrypt(plaintext, size, iv))
        enc_time = (encrypt_timer.timeit(number=1000) / 1000) * 1000000
        arrayEnc.append(enc_time)

        ciphertext = encrypt(plaintext, size, iv)
        '''out_path = os.path.join(encrypt_dir, f"{size}.bin")
        with open(out_path, "wb") as f:
            f.write(ciphertext)'''

        # Decrypt and time decryption
        decrypt_timer = timeit.Timer(lambda: decrypt(ciphertext, size, iv))
        dec_time = (decrypt_timer.timeit(number=1000) / 1000) * 1000000
        arrayDec.append(dec_time) 

        ''' decrypted_text = decrypt(ciphertext, size, iv)
        out_path = os.path.join(decrypt_dir, f"{size}.txt")
        with open(out_path, "w") as f:
            f.write(decrypted_text.decode('utf-8'))'''

    plot_results(arrayEnc, arrayDec, file)

def plot_results(arrayEnc, arrayDec, file):
    # Create a figure
    plt.figure(figsize=(12, 8))

    # Set the width of the bars
    bar_width = 0.35
    index = range(1, len(arrayEnc) + 1)  # Indices for X-axis
    
    # Plot the encryption and decryption times as bar charts
    plt.bar([i - bar_width / 2 for i in index], arrayEnc, bar_width, label='Encryption Time', color='blue')
    plt.bar([i + bar_width / 2 for i in index], arrayDec, bar_width, label='Decryption Time', color='red', alpha=0.6)

    # Compute standard deviation for encryption times
    std_enc = np.std(arrayEnc, ddof=1)  # ddof=1 for sample std deviation
    std_dec = np.std(arrayDec, ddof=1)  # ddof=1 for sample std deviation

    # Adding labels and title
    plt.xlabel('Iteration')
    plt.ylabel('Time (microseconds)')
    plt.title(f"AES Encryption and Decryption Times for {file}")
    
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

def main():
    # encrypt and decrypt a single given file
    processUnique("64_5.txt",64)

    #print("Filename    | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    # process all input files in one run

    print("Confidence Intervals (microseconds) for AES:")
    print("----------------------------------------------------------------------------")
    for size in sizes:
        processAllFiles(size)
    # Print a graph for each size folder
    plot_graph(results)
    plot_graph_avg(results)
    plot_graph_avg_bar(results)

    # process one given file various times
    #processUnique()


if __name__ == "__main__":
    main()