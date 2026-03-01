

import os
import shutil


def prepare_directory(output_dir):
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def write(records, output_dir):
  
    prepare_directory(output_dir)

    file_path = os.path.join(output_dir, "records.dat")
    index = []

    offset = 0

    with open(file_path, "wb") as f:
        for record in records:
            size = len(record)
            f.write(record)

            index.append((offset, size))
            offset += size

    return index


def read_sequential(index, input_dir):
    

    file_path = os.path.join(input_dir, "records.dat")

    with open(file_path, "rb") as f:
        for offset, size in index:
            f.seek(offset)
            f.read(size)


def read_random(index, input_dir, record_ids):
 
    file_path = os.path.join(input_dir, "records.dat")

    with open(file_path, "rb") as f:
        for rid in record_ids:
            offset, size = index[rid]
            f.seek(offset)
            f.read(size)