import os
import json
import time
import uuid
import gcsfs
import psutil
import tracemalloc

from datetime import datetime

from .write_data import write_results


def monitor_it(
    func,
    sf: int,
    n_partitions: int,
    query_number: int,
    system: str,
    session_id: str,
    *args,
    **kwargs,
):
    process = psutil.Process()

    # Start tracing memory allocations
    tracemalloc.start()

    # Calculate CPU usage before and after running the function
    cpu_usage_start = process.cpu_percent(interval=None)
    start_time = time.time()

    write_results(func(*args, **kwargs), sf, n_partitions, system, 1)

    elapsed_time = time.time() - start_time
    cpu_usage_end = process.cpu_percent(interval=None)

    # Get memory usage data
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_cpu = (cpu_usage_end - cpu_usage_start) / (elapsed_time / 100)

    data = {
        "session_id": session_id,
        "system": system,
        "timestamp": datetime.utcnow().isoformat(),
        "sf": sf,
        "n_partitions": n_partitions,
        "query_number": query_number,
        "execution_seconds": elapsed_time,
        "peak_cpu": peak_cpu,
        "peak_memory": peak / 1024**3,
    }

    write_monitor_results(data)


def write_monitor_results(results, cloud=True):
    dir_name = get_timings_dir(cloud=cloud)

    if cloud:
        fs = gcsfs.GCSFileSystem()
        with fs.open(f"gs://ibis-benchy/{dir_name}/{uuid.uuid4()}.json", "w") as f:
            json.dump(results, f)
    else:
        with open(f"{dir_name}/{uuid.uuid4()}.json", "w") as f:
            json.dump(results, f)


def get_timings_dir(cloud=True):
    dir_name = "benchy_logs_v0"

    if not cloud:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

    return dir_name
