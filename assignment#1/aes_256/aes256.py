#-- in progress - Max :) --#
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
import os
import timeit

sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
results = {}
key = os.urandom(32) # key of 32 bytes (256 bits)
iv = os.urandom(16) # iv has to be 16 bytes

# create directories for encryption and decryption files
encrypt_dir = "encrypted_files"
decrypt_dir = "decrypted_files"
os.makedirs(encrypt_dir, exist_ok=True)
os.makedirs(decrypt_dir, exist_ok=True)

def encrypt(data, size):
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



def decrypt(ciphertext, size):
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



def main():
    print("Filename    | Size (bytes) | Encryption Time (s) | Decryption Time (s)")
    # process all input files in one run
    for size in sizes:
        file_path = os.path.join("text_files", str(size) + ".txt")
        #print(file_path)
        file = open(file_path, "rb") # read input file and extract plaintext
        plaintext = file.read()
        #print(plaintext)

        # encrypt
        # time of encryption (average over 1000 iterations)
        encrypt_timer = timeit.Timer(lambda: encrypt(plaintext,size))
        enc_time = encrypt_timer.timeit(number=1000) / 1000

        ciphertext = encrypt(plaintext,size)
        out_path = os.path.join(encrypt_dir, str(size) + ".bin")
        f = open(out_path, "wb")
        f.write(ciphertext) # write the encrypted message to file

        # decrypt
        # Time decryption (average over 1000 iterations)
        decrypt_timer = timeit.Timer(lambda: decrypt(ciphertext, size))
        dec_time = decrypt_timer.timeit(number=1000) / 1000

        decrypted_text = decrypt(ciphertext, size)
        out_path = os.path.join(decrypt_dir, str(size) + ".txt")
        f = open(out_path, "w")
        f.write(decrypted_text.decode('utf-8')) # write the encrypted message to file

        results[size] = {'encryption_time': enc_time, 'decryption_time': dec_time}
        filename = str(size) + ".txt"
        print(f"{filename:<11} | {size:<12} | {enc_time:.9f}         | {dec_time:.9f}")

        '''print(f"File size: {size} bytes")
        print(f"  Average encryption time: {enc_time:.6f} seconds")
        print(f"  Average decryption time: {dec_time:.6f} seconds\n")'''


if __name__ == "__main__":
    main()