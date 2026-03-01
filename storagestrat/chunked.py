import os
import shutil

from given import ChunkSize


def prepare_directory(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def write(records, output_dir):

    prepare_directory(output_dir)

    index = []

    chunk_id = 0
    offset = 0
    current_file = None

    for i, record in enumerate(records):
        if i % ChunkSize == 0:
            if current_file:
                current_file.close()

            offset = 0
            file_path = os.path.join(output_dir, f"chunk_{chunk_id}.dat")
            current_file = open(file_path, "wb")
            chunk_id += 1

        size = len(record)
        current_file.write(record)

        index.append((chunk_id - 1, offset, size))
        offset += size

    if current_file:
        current_file.close()

    return index


def read_sequential(index, input_dir):

    for chunk_id, offset, size in index:
        file_path = os.path.join(input_dir, f"chunk_{chunk_id}.dat")
        with open(file_path, "rb") as f:
            f.seek(offset)
            f.read(size)

def read_random(index, input_dir, record_ids):
    for rid in record_ids:
        chunk_id, offset, size = index[rid]
        file_path = os.path.join(input_dir, f"chunk_{chunk_id}.dat")

        with open(file_path, "rb") as f:
            f.seek(offset)
            f.read(size)