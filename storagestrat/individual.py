import os
import shutil


def prepare_directory(output_dir):

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def write(records, output_dir):
    prepare_directory(output_dir)

    for record_id, record in enumerate(records):
        file_path = os.path.join(
            output_dir,
            f"record_{record_id:06d}.dat"
        )

        with open(file_path, "wb") as f:
            f.write(record)


def read_sequential(input_dir, num_records):
    for record_id in range(num_records):
        file_path = os.path.join(
            input_dir,
            f"record_{record_id:06d}.dat"
        )

        with open(file_path, "rb") as f:
            f.read()
        if record_id % 10000 == 0:
            print(f"Read {record_id} files...")
    


def read_random(input_dir, record_ids):

    for record_id in record_ids:
        file_path = os.path.join(
            input_dir,
            f"record_{record_id:06d}.dat"
        )

        with open(file_path, "rb") as f:
            f.read()