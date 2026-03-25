import time

def stream_logs(file_path):
    with open(file_path, "r") as f:
        for line in f:
            time.sleep(1)
            yield line.strip()
