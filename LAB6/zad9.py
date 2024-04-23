import os
import hashlib
import time

def generate_file_hash(file_path, hash_algo):
    try:
        hash_function = hashlib.new(hash_algo)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")
    
    try:
        with open(file_path, "rb") as file:
            for block in iter(lambda: file.read(4096), b""):
                hash_function.update(block)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

    return hash_function.hexdigest()

sizes = [100, 250, 500]  
for size in sizes:
    with open(f'file_{size}MB.txt', 'wb') as f:
        f.write(os.urandom(size * 1024 * 1024))  

algorithms = ['md5', 'sha256', 'blake2s']
for size in sizes:
    file_path = f'file_{size}MB.txt'
    for algo in algorithms:
        start_time = time.time()
        generate_file_hash(file_path, algo)
        duration = time.time() - start_time
        print(f'Czas dla {algo} na pliku {size}MB: {duration:.2f} sekund')

file_path = 'example.txt'
hash_algo = 'sha256'

with open(file_path, 'w') as file:
    file.write("To jest przykładowy tekst do testowania.")
result1 = generate_file_hash(file_path, hash_algo)

with open(file_path, 'r+') as file:
    content = file.read()
    file.seek(0)
    file.write(content.replace("przykładowy", "zmodyfikowany"))
    file.truncate()
print("Plik został nieco zmodyfikowany.")

result2 = generate_file_hash(file_path, hash_algo)

if result1 == result2:
    print("Integralność pliku została zweryfikowana!")
else:
    print("Plik został zmodyfikowany lub uszkodzony!")
