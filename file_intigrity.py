import os
import json
import hashlib

BASELINE_FILE = "baseline.json"

def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def scan_directory(directory):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hashes[path] = calculate_hash(path)

    return file_hashes


def create_baseline(directory):
    hashes = scan_directory(directory)

    with open(BASELINE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

    print("Baseline created successfully.")


def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {}

    with open(BASELINE_FILE, "r") as f:
        return json.load(f)


def check_integrity(directory):
    baseline = load_baseline()
    current = scan_directory(directory)

    # Detect modified and deleted files
    for file, old_hash in baseline.items():
        if file not in current:
            print(f"[DELETED] {file}")

        elif current[file] != old_hash:
            print(f"[MODIFIED] {file}")

    # Detect new files
    for file in current:
        if file not in baseline:
            print(f"[NEW FILE] {file}")


if __name__ == "__main__":
    directory = input("Enter directory path: ")

    print("\n1. Create Baseline")
    print("2. Check Integrity")

    choice = input("Select option: ")

    if choice == "1":
        create_baseline(directory)

    elif choice == "2":
        check_integrity(directory)

    else:
        print("Invalid choice.")