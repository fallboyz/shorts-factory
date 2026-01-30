import os
import shutil
import glob

def clean():
    print("Cleaning Images...")
    # Delete subdirectories in images/
    base_dir = 'data/images'
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            path = os.path.join(base_dir, item)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Deleted Dir: {path}")
                else:
                    os.remove(path)
                    print(f"Deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")

if __name__ == '__main__':
    clean()
