import os
import timeit
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

# Process each file in the folder
results = {}

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

def plot_graph(results):
    plt.figure(figsize=(12, 8))

    # Loop through the results and assign a unique color per set
    bar_width = 0.35  # Set the width of the bars
    for idx, (s, times) in enumerate(results.items()):
        color = colors[idx % len(colors)]
        x_axis = range(1, len(times['encryption_time']) + 1)  # X-axis is the file index

        # Plot the bars for encryption and decryption times
        plt.bar([i - bar_width / 2 for i in x_axis], times['encryption_time'], bar_width,
                label=f'Encryption Time for size {s}', color=color)
        plt.bar([i + bar_width / 2 for i in x_axis], times['decryption_time'], bar_width,
                label=f'Decryption Time for size {s}', color=color, alpha=0.6)

    # Set labels, title and x-axis ticks
    plt.xlabel('File Index')
    plt.ylabel('Time (Microseconds)')
    plt.title("Encryption and Decryption Times for RSA")

    # Set X-axis to show values from 0 to 100 with steps of 10
    tick_positions = range(1, 101, 10)  # Show ticks every 10 iterations
    plt.xticks(tick_positions)  # Set X-axis to display only 10th iterations (0, 10, 20, ..., 100)

    plt.legend()
    plt.show()


def plot_graph_avg(results):
    # For each size, compute the average encryption and decryption time
    sizes = sorted(results.keys())
    avg_enc_times = []
    avg_dec_times = []
    
    for s in sizes:
        avg_enc = sum(results[s]['encryption_time']) / len(results[s]['encryption_time'])
        avg_dec = sum(results[s]['decryption_time']) / len(results[s]['decryption_time'])
        avg_enc_times.append(avg_enc)
        avg_dec_times.append(avg_dec)

    plt.figure(figsize=(12, 8))

    # Set the width of the bars
    bar_width = 0.35
    index = range(len(sizes))  # Indices for X-axis
    
    # Plot the bars for encryption and decryption times
    plt.bar([i - bar_width / 2 for i in index], avg_enc_times, bar_width, label='Encryption Time', color='blue')
    plt.bar([i + bar_width / 2 for i in index], avg_dec_times, bar_width, label='Decryption Time', color='red')

    # Adding labels and title
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for RSA")

    # Set the X-axis positions to the indices of sizes
    plt.xticks(index, sizes)  # Use the actual size values as x-axis labels

    # Display the bars and the legend
    plt.legend()
    plt.show()


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

def plot_results(arrayEnc, arrayDec, file):
    # Create a figure
    plt.figure(figsize=(10, 6))

    # Set the width of the bars
    bar_width = 0.35
    index = range(1, len(arrayEnc) + 1)  # Indices for X-axis
    
    # Plot the encryption and decryption times as bar charts
    plt.bar([i - bar_width / 2 for i in index], arrayEnc, bar_width, label='Encryption Time', color='blue')
    plt.bar([i + bar_width / 2 for i in index], arrayDec, bar_width, label='Decryption Time', color='red', alpha=0.6)

    # Adding labels and title

    plt.xlabel('Iteration')
    plt.ylabel('Time (microseconds)')
    plt.title(f"Encryption and Decryption Times for {file}")
    
    # Set X-axis labels to the index of iterations
    tick_positions = range(0, 101, 10)  # Show ticks every 10 iterations
    plt.xticks(tick_positions)  # Set X-axis to display only 10th iterations
    plt.legend(loc='upper right')

    # Display the plot
    plt.show()




def main():
    # Print results
    process_unique("64_5.txt",64)
    print("Filename | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    for size in sizes:
        process_all_files(size)
    plot_graph(results)
    plot_graph_avg(results)
    
if __name__ == "__main__":
    main()
