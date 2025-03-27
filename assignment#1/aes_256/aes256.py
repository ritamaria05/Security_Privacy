#-- in progress - Max :) --#
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
import os
import timeit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
results = {}
key = os.urandom(32) # key of 32 bytes (256 bits)

# create directories for encryption and decryption files
encrypt_dir = "encrypted_files"
decrypt_dir = "decrypted_files"
os.makedirs(encrypt_dir, exist_ok=True)
os.makedirs(decrypt_dir, exist_ok=True)

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

## **** edit to store values in an arrayand then at end   **** ##
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
        out_path = os.path.join(encrypt_dir, f"{size}.bin")
        with open(out_path, "wb") as f:
            f.write(ciphertext)

        # Decrypt and time decryption
        decrypt_timer = timeit.Timer(lambda: decrypt(ciphertext, size, iv))
        dec_time = (decrypt_timer.timeit(number=100) / 100) * 1000000
        arrDec[i - 1] = dec_time

        decrypted_text = decrypt(ciphertext, size, iv)
        out_path = os.path.join(decrypt_dir, f"{size}.txt")
        with open(out_path, "w") as f:
            f.write(decrypted_text.decode('utf-8'))

        filename = f"{size}_{i}.txt"
        print(f"{filename:<11} | {size:<12} | {enc_time:.9f}         | {dec_time:.9f}")

    # Store all times for the given size
    results[size] = {'encryption_time': arrEnc, 'decryption_time': arrDec}

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
    for idx, (s, times) in enumerate(results.items()):
        color = colors[idx % len(colors)]
        x_axis = range(1, len(times['encryption_time']) + 1)
        plt.plot(x_axis, times['encryption_time'], label=f'Encryption Time for size {s}',
                 color=color, linestyle='-', marker='o', markersize=4)
        plt.plot(x_axis, times['decryption_time'], label=f'Decryption Time for size {s}',
                 color=color, linestyle='--', marker='x', markersize=4)
    
    plt.xlabel('File Index')
    plt.ylabel('Time (Microseconds)')
    plt.title("Encryption and Decryption Times for AES")
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

    # Scatter plot for encryption and decryption times
    plt.scatter(sizes, avg_enc_times, marker='o', color='blue', label='Encryption Time (Bottom Right Label)')
    plt.scatter(sizes, avg_dec_times, marker='x', color='red', label='Decryption Time (Top Left Label)')
    
    # Add coordinate labels to each point
    for x, y in zip(sizes, avg_enc_times):
        plt.text(x, y, f"({x}, {y:.2f})", fontsize=9, verticalalignment='bottom', horizontalalignment='right')

    for x, y in zip(sizes, avg_dec_times):
        plt.text(x, y, f"({x}, {y:.2f})", fontsize=9, verticalalignment='top', horizontalalignment='left')

    # Use a logarithmic scale for the x-axis
    plt.xscale('log')  # 'log' for better visualization
    plt.xlabel('Size (Bytes)')
    plt.ylabel('Time (Microseconds)')
    plt.title("Average Encryption and Decryption Times for AES")
    plt.legend()
    plt.show()


def processUnique():
    arrEnc = [0] * 100  # Creates a list with 100 elements initialized to 0
    arrDec = [0] * 100 

def main():
    print("Filename    | Size (bytes) | Encryption Time (s) | Decryption Time (s)")

    # process all input files in one run
    for size in sizes:
        processAllFiles(size)
    plot_graph(results)
    plot_graph_avg(results)

    # process one given file various times
    #processUnique()


if __name__ == "__main__":
    main()