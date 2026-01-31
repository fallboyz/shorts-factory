import os
import shutil
import glob

def clean():
    print("Cleaning all image resources (including source.png and slices)...")
    base_dir = 'data/images'
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            path = os.path.join(base_dir, item)
            # README.md는 데이터 구조 유지를 위해 제외
            if item.lower() == 'readme.md':
                continue
                
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Deleted Image Folder: {path}")
                else:
                    os.remove(path)
                    print(f"Deleted File: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")



if __name__ == '__main__':
    clean()
