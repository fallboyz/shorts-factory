import os
import glob

def clean():
    print("Cleaning Marketing Metadata (TXT, JSON)...")
    targets = [
        'data/metadata/*.txt', 
        'data/metadata/*.json'
    ]
    for target in targets:
        for f in glob.glob(target):
            # Keep README.md
            if f.endswith('README.md'):
                continue
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

if __name__ == '__main__':
    clean()
