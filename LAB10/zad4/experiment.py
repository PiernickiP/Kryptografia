import time
import os
from stegano import lsb
import pandas as pd


def hide_message(image_path, message, output_path):
    start_time = time.time()
    secret_image = lsb.hide(image_path, message)
    end_time = time.time()
    secret_image.save(output_path)
    return end_time - start_time, os.path.getsize(output_path)

def reveal_message(image_path):
    start_time = time.time()
    message = lsb.reveal(image_path)
    end_time = time.time()
    return message, end_time - start_time

image_sizes = ['100kb', '1mb', '10mb']
message_lengths = [10, 100, 1000, 10000]

results = []

for image_size in image_sizes:
    original_image_path = f"image_{image_size}.jpg"
    for length in message_lengths:
        message = "A" * length
        output_image_path = f"hidden_{image_size}_{length}.png"
        
        encrypt_time, new_size = hide_message(original_image_path, message, output_image_path)
        revealed_message, decrypt_time = reveal_message(output_image_path)
        
        results.append({
            "image_size": image_size,
            "message_length": length,
            "encrypt_time": encrypt_time,
            "decrypt_time": decrypt_time,
            "new_image_size": new_size,
            "message_correct": message == revealed_message
        })

df = pd.DataFrame(results)

print(df)

