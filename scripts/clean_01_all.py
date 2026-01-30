import os
import sys

def run_script(name):
    script_path = os.path.join("scripts", name)
    print(f"--- Running {name} ---")
    os.system(f"python {script_path}")

if __name__ == '__main__':
    print("WARNING: This will delete ALL data (Scripts, Audio, Images, Output).")
    try:
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            run_script('clean_02_scripts.py')
            run_script('clean_03_audio.py')
            run_script('clean_04_images.py')
            run_script('clean_05_output.py')
            print("\nAll Cleaned.")
        else:
            print("Cancelled.")
    except KeyboardInterrupt:
        print("\nCancelled.")
