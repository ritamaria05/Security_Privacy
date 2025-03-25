import os
import random
import string

def generate_random_file(folder, filename, size):
    file_path = os.path.join("text_files", folder, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
    
    random_content = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    with open(file_path, "w") as f:
        f.write(random_content)

file_sizes = [2, 4, 8, 16, 32, 64, 128, 512, 4096, 32768, 262144, 2097152]  # Adjust for RSA if needed
for size in file_sizes:
    folder_name = str(size)  # Folder named after size
    for i in range(1, 101):
        generate_random_file(folder_name, f"{size}_{i}.txt", size)
