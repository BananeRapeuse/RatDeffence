import os
import time

def scan_directory(directory, progress_callback, result_callback):
    total_files = sum([len(files) for r, d, files in os.walk(directory)])
    scanned_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            scanned_files += 1
            file_path = os.path.join(root, file)
            # Simulated virus scan
            time.sleep(0.1)  # Simulate scan delay
            if "virus" in file.lower():
                result_callback(file_path)
            progress_callback(scanned_files, total_files)
