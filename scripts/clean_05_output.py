import os
import shutil
import glob

def clean():
    print("Cleaning Output Videos...")
    targets = ['data/output/*.mp4']
    for target in targets:
        for f in glob.glob(target):
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

if __name__ == '__main__':
    clean()
