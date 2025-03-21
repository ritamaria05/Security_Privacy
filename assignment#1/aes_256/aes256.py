#-- in progress - Max :) --#
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
import os
import timeit

key = os.urandom(32) # key of 32 bytes (256 bits)
iv = os.urandom(16) # iv has to be 16 bytes

# create directories for encryption and decryption files
encrypt_dir = "encrypted_files"
decrypt_dir = "decrypted_files"
os.makedirs(encrypt_dir, exist_ok=True)
os.makedirs(decrypt_dir, exist_ok=True)

def encrypt(file_path):
    file = open(file_path, "rb") # read input file and extract plaintext
    plaintext = file.read()

    # encrypt the plaintext using key and iv
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv)) # use cbc mode (fast and secure for regular text files)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    out_path = os.path.join(encrypt_dir, os.path.basename(file_path) + ".bin")
    f = open(out_path, "wb")
    f.write(ciphertext)

    return out_path


def decrypt(file_path):
    f = open(file_path, "rb") # read input file and extract ciphertext
    ciphertext = f.read()



    return

def main():
    # process all input files in one run
    for file in os.listdir("text_files"):
        file_path = os.path.join("text_files", file)
        #print(file_path)

        # encrypt and record time taken
        encryption_time = timeit.timeit(lambda: encrypt(file_path))
        encrypt_filepath = os.path.join(encrypt_dir, file + ".bin") # path of file to then decrypt
        print(f"Encrypted {file} : {encryption_time:.6f} seconds")

        # decrypt and record time taken
        decryption_time = timeit.timeit(lambda: decrypt(encrypt_filepath))
        print(f"Decrypted {file} : {decryption_time:.6f} seconds")


        # print 




if __name__ == "__main__":
    main()