import os
import timeit
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt

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
    for i in range(1,101):
        file_path = os.path.join("text_files", str(size), str(size)+"_"+str(i)+".txt")

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                data = f.read()

            # Measure encryption time
            enc_time = timeit.timeit(lambda: encrypt_data(data), number=1000) / 1000
            encrypted_data = encrypt_data(data)
            arrayEnc[i-1] = enc_time
            # Measure decryption time
            dec_time = timeit.timeit(lambda: decrypt_data(encrypted_data), number=1000) / 1000
            arrayDec[i-1] = dec_time
            # Store results
            results[size]={'encryption_time':enc_time, 'decryption_time':dec_time}
            filename = str(size) + "_" + str(i) + ".txt"
            print(f"{filename:<8} | {size:<12} | {enc_time:.9f}         | {dec_time:.6f}")


import os
import timeit

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
            enc_time = timeit.timeit(lambda: encrypt_data(data), number=100) / 100
            encrypted_data = encrypt_data(data)
        except Exception as e:
            print(f"Error encrypting {file}: {e}")
            continue
        arrayEnc.append(enc_time)
        try:
            # Measure decryption time
            dec_time = timeit.timeit(lambda: decrypt_data(encrypted_data), number=100) / 100
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

    # Plot the encryption and decryption times
    plt.plot(arrayEnc, label='Encryption Time', color='blue', linestyle='-', marker='o', markersize=4)
    plt.plot(arrayDec, label='Decryption Time', color='red', linestyle='-', marker='x', markersize=4)

    # Adding labels and title
    plt.xlabel('Iteration')
    plt.ylabel('Time (seconds)')
    plt.title(f"Encryption and Decryption Times for {file}")
    plt.legend()

    # Display the plot
    plt.show()

def main():
    # Print results
    process_unique("64_5.txt",64)
    #print("Filename | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    #for size in sizes:
    #    process_all_files(size)
    
if __name__ == "__main__":
    main()
