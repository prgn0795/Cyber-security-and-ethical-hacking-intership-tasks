import os
import hashlib
import json
import argparse

def calculate_file_hash(filepath, algorithm="sha256"):
    """Calculate the hash of a file."""
    try:
        hasher = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error calculating hash for {filepath}: {e}")
        return None

def generate_baseline(target_dir, baseline_file, algorithm="sha256"):
    """Generate a baseline of file hashes."""
    baseline = {}
    print(f"Generating baseline for directory: {target_dir}")
    
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            # Standardize path separators for consistency
            rel_path = os.path.relpath(filepath, target_dir).replace('\\', '/')
            
            # Skip the baseline file itself if it's in the target directory
            if os.path.abspath(filepath) == os.path.abspath(baseline_file):
                continue
                
            file_hash = calculate_file_hash(filepath, algorithm)
            if file_hash:
                baseline[rel_path] = file_hash
                
    with open(baseline_file, 'w') as f:
        json.dump(baseline, f, indent=4)
        
    print(f"Baseline successfully generated and saved to {baseline_file}")
    print(f"Total files hashed: {len(baseline)}")

def check_integrity(target_dir, baseline_file, algorithm="sha256"):
    """Check current files against the saved baseline."""
    print(f"Checking integrity of directory: {target_dir} using baseline: {baseline_file}")
    
    if not os.path.exists(baseline_file):
        print(f"Error: Baseline file '{baseline_file}' does not exist.")
        return
        
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return

    with open(baseline_file, 'r') as f:
        try:
            baseline = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Baseline file '{baseline_file}' is invalid or corrupted.")
            return

    current_files = {}
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, target_dir).replace('\\', '/')
            
            # Skip the baseline file itself if it's in the target directory
            if os.path.abspath(filepath) == os.path.abspath(baseline_file):
                continue
                
            file_hash = calculate_file_hash(filepath, algorithm)
            if file_hash:
                current_files[rel_path] = file_hash

    new_files = []
    modified_files = []
    deleted_files = []

    # Check for modified and new files
    for filepath, current_hash in current_files.items():
        if filepath not in baseline:
            new_files.append(filepath)
        elif baseline[filepath] != current_hash:
            modified_files.append(filepath)

    # Check for deleted files
    for filepath in baseline:
        if filepath not in current_files:
            deleted_files.append(filepath)

    # Report findings
    print("\n" + "="*40)
    print("INTEGRITY CHECK RESULTS")
    print("="*40)
    
    if not new_files and not modified_files and not deleted_files:
        print("✅ NO CHANGES DETECTED. File integrity is intact.")
    else:
        if modified_files:
            print("\n[!] MODIFIED FILES DETECTED:")
            for f in modified_files:
                print(f"  - {f}")
                
        if new_files:
            print("\n[+] NEW FILES DETECTED:")
            for f in new_files:
                print(f"  - {f}")
                
        if deleted_files:
            print("\n[-] DELETED FILES DETECTED:")
            for f in deleted_files:
                print(f"  - {f}")

    print("\n" + "="*40)

def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("action", choices=["generate", "check"], help="Action to perform: 'generate' a baseline or 'check' integrity")
    parser.add_argument("--target", required=True, help="Target directory to monitor")
    parser.add_argument("--baseline", required=True, help="Path to the baseline JSON file")
    parser.add_argument("--algorithm", default="sha256", choices=["md5", "sha1", "sha256", "sha512"], help="Hashing algorithm to use (default: sha256)")
    
    args = parser.parse_args()
    
    if args.action == "generate":
        generate_baseline(args.target, args.baseline, args.algorithm)
    elif args.action == "check":
        check_integrity(args.target, args.baseline, args.algorithm)

if __name__ == "__main__":
    main()
