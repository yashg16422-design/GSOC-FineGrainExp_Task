import time
import random
from system_monitor import BenchmarkMonitor
import atexit

from given import (
    RandomSeed,
    RandomReadCount,
    NumRecords,
    ChunkSize,
    SingleFileDir,
    ChunkedDir,
    IndividualDir,
)

from RandomDataCreate import generate_records
from storagestrat import single_file, chunked, individual


RunMode = input(" \n You  are always asked further to run time consuming individual strategy or not\n" \
"\n Please enter the benchmark mode in for all 3 strategies you can not choose to run individual file later\n" \
"\n WRITE only (press 1)->Enter," \
"\n READ only (press 2)," \
"\n BOTH modes(press 3), " \
"\n FULL( press 4(Includes automatic testin for individual files may take upto 20 mins) and BOTH modes)\n" \
"\nEnter from 1 , 2 , 3 , 4   ").strip().lower()    # "write", "read", "both"
FullRun = False
import os
# def drop_cache_windows():
#     cache_flush_path = "cache_flush.tmp"
#     with open(cache_flush_path, "wb") as f:
#         f.write(os.urandom(1024 * 1024 * 1024 * 2))  # 512MB to flood cache
#     os.remove(cache_flush_path)

def data_exists_and_not_empty():
    
   
    if not os.path.exists(SingleFileDir) or not os.listdir(SingleFileDir):
        return False

    if not os.path.exists(ChunkedDir) or not os.listdir(ChunkedDir):
        return False

    # if not os.path.exists(IndividualDir) or not os.listdir(IndividualDir):
    #     return False

    return True
def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start



def build_single_file_index(records):
    index = []
    offset = 0
    for record in records:
        size = len(record)
        index.append((offset, size))
        offset += size
    return index


def build_chunked_index(records, chunk_size):
    index = []
    chunk_id = 0
    offset = 0

    for i, record in enumerate(records):
        if i % chunk_size == 0:
            offset = 0
            if i != 0:
                chunk_id += 1

        size = len(record)
        index.append((chunk_id, offset, size))
        offset += size

    return index
m = BenchmarkMonitor()
p = BenchmarkMonitor()
p.start()

atexit.register(p.stop)
def main():
    global RunMode,FullRun

    if RunMode == "4":
        FullRun = True
    if FullRun:
        RunMode = "3"
    # Auto-switch to BOTH if files missing
    if RunMode == "2" and not data_exists_and_not_empty():
        print("\nData files missing or empty. Switching to BOTH mode.\n")
        RunMode = "3"

    print(f"\n  Storage I/O Experiment ({RunMode.upper()} MODE) \n")

    records = None
    if RunMode.strip().lower() in ("1", "2", "3","4"):
        records, _ = generate_records()
    random.seed(RandomSeed)
    random_ids = random.sample(range(NumRecords), RandomReadCount)

    print("#Single File Strategy...")
    m.start()
    if RunMode in ("1", "3"):
        index_single, t_write = measure_time(
            single_file.write,
            records,
            SingleFileDir
        )
        print(f"Write time        : {t_write:.4f} seconds   Avg Latency")
    else:
        index_single = build_single_file_index(records)

    if RunMode in ("2", "3"):
        _, t_seq = measure_time(
            single_file.read_sequential,
            index_single,
            SingleFileDir
        )
        print(f"Sequential read   : {t_seq:.4f} seconds")

        _, t_rand = measure_time(
            single_file.read_random,
            index_single,
            SingleFileDir,
            random_ids
        )
        print(f"Random read       : {t_rand:.4f} seconds \n\n Resource report for Single")
        m.stop()
    print()

    print("#Chunked File Strategy..")
    m.start()
    if RunMode in ("1", "3"):
        index_chunked, t_write = measure_time(
            chunked.write,
            records,
            ChunkedDir
        )
        print(f"Write time        : {t_write:.4f} seconds")
    else:
        index_chunked = build_chunked_index(records, ChunkSize)

    if RunMode in ("2", "3"):
        _, t_seq = measure_time(
            chunked.read_sequential,
            index_chunked,
            ChunkedDir
        )
        print(f"Sequential read   : {t_seq:.4f} seconds")
        # drop_cache_windows()   
        _, t_rand = measure_time(
            chunked.read_random,
            index_chunked,
            ChunkedDir,
            random_ids
        )
        print(f"Random read       : {t_rand:.4f} seconds \n\n Resource report for Chunked")
        m.stop()
    print()
    if not FullRun:
        run_individual = input(
            "Run Individual File Strategy? (y/n): "
        ).strip().lower()

        if run_individual != "y":
            print("\nSkipping Individual File Strategy.\n")
            print("=== Experiment Finished ===\n")
            return

    print("#Individual File Strategy...")

    # if RunMode in ("1", "3"):
    #     _, t_write = measure_time(
    #         individual.write,
    #         records,
    #         IndividualDir
    #     )
    #     print(f"Write time        : {t_write:.4f} seconds")

    if RunMode in ("2", "3"):
        _, t_seq = measure_time(
            individual.read_sequential,
            IndividualDir,
            NumRecords
        )
        print(f"Sequential read   : {t_seq:.4f} seconds")

        _, t_rand = measure_time(
            individual.read_random,
            IndividualDir,
            random_ids
        )
        print(f"Random read       : {t_rand:.4f} seconds")

    print("Experiment Finished.. \n Final Report...")
    

if __name__ == "__main__":
    main()
    