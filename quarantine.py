import os

QUARANTINE_DIR = "quarantine"

def quarantine_file(file_path):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    try:
        new_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
        os.rename(file_path, new_path)
    except Exception as e:
        print(f"Error quarantining file {file_path}: {e}")

def get_quarantined_files():
    if not os.path.exists(QUARANTINE_DIR):
        return []
    return os.listdir(QUARANTINE_DIR)
