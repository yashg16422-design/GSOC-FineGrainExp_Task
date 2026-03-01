import random
import os

from given import (
    NumRecords,
    MinRecordSize,
    MaxRecordSize,
    RandomSeed,
)
def generate_records():

    random.seed(RandomSeed)

    records = []
    sizes = []

    for _ in range(NumRecords):
        size = random.randint(MinRecordSize, MaxRecordSize)
        data = os.urandom(size)

        records.append(data)
        sizes.append(size)

    return records, sizes


if __name__ == "__main__":
    records, sizes = generate_records()

    print("Data generation Acc to given parameters(gsoc)..")
    print(f"Total records   : {len(records)}")
    print(f"Min size (bytes): {min(sizes)}")
    print(f"Max size (bytes): {max(sizes)}")
    print(f"Avg size (bytes): {sum(sizes) /len(sizes):.2f}")