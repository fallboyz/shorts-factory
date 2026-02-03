import os
import sys

def run_script(name):
    script_path = os.path.join("scripts", name)
    print(f"--- Running {name} ---")
    os.system(f"python {script_path}")

if __name__ == '__main__':
    print("WARNING: This will delete ALL resources EXCEPT final output videos (.mp4).")
    print("This includes scripts, audio, images, and resetting the inventory.")
    try:
        confirm = input("Proceed? (y/n): ")
        if confirm.lower() == 'y':
            run_script('clean_02_scripts.py')
            run_script('clean_03_audio.py')
            run_script('clean_04_images.py')
            run_script('clean_07_subtitles.py')
            run_script('clean_08_metadata.py')
            run_script('clean_06_inventory.py')
            print("\nCleanup Complete. (Final MP4s and Fonts are preserved)")
        else:
            print("Cancelled.")
    except KeyboardInterrupt:
        print("\nCancelled.")


