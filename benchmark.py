import csv
import os
import time
import threading
from pathlib import Path

import psutil

from insight.pipeline import run_pipeline

DATASETS = [
    'iris.csv',
    'retail_small.csv',
    'retail_big.csv',
]


def track_memory(func, *args, **kwargs):
    proc = psutil.Process()
    max_rss = 0
    result = None

    def target():
        nonlocal result
        result = func(*args, **kwargs)

    thread = threading.Thread(target=target)
    thread.start()
    while thread.is_alive():
        rss = proc.memory_info().rss
        max_rss = max(max_rss, rss)
        time.sleep(0.05)
    thread.join()
    max_rss = max(max_rss, proc.memory_info().rss)
    return result, max_rss


def count_rows(csv_path: str) -> int:
    with open(csv_path, 'r', newline='') as f:
        return sum(1 for _ in f) - 1


def benchmark(csv_path: str):
    start = time.perf_counter()
    pdf_path, max_rss = track_memory(run_pipeline, csv_path)
    secs = time.perf_counter() - start
    pdf_size_kb = os.path.getsize(pdf_path) / 1024 if os.path.exists(pdf_path) else 0
    rows = count_rows(csv_path)
    return {
        'dataset': Path(csv_path).name,
        'rows': rows,
        'secs': round(secs, 2),
        'mb_ram': round(max_rss / (1024 ** 2), 2),
        'pdf_kb': round(pdf_size_kb, 2),
    }


def main():
    with open('benchmark_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['dataset', 'rows', 'secs', 'mb_ram', 'pdf_kb'])
        writer.writeheader()
        for dataset in DATASETS:
            stats = benchmark(dataset)
            writer.writerow(stats)
            print(stats)


if __name__ == '__main__':
    main()
