import os
import timeit
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# folder of random text files for RSA
folder_path = "text_files" 

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
results = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            data = f.read()

        # Measure encryption time
        enc_time = timeit.timeit(lambda: encrypt_data(data), number=10) / 10
        encrypted_data = encrypt_data(data)

        # Measure decryption time
        dec_time = timeit.timeit(lambda: decrypt_data(encrypted_data), number=10) / 10

        # Store results
        results.append((filename, len(data), enc_time, dec_time))

# 🔹 Print results
print("Filename | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
for filename, size, enc_time, dec_time in results:
    print(f"{filename:<10} | {size:<12} | {enc_time:.6f}         | {dec_time:.6f}")