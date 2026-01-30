import os
import shutil
import glob

def clean():
    print("Cleaning Audio and Subtitles...")
    targets = ['data/audio/*.mp3', 'data/audio/*.vtt', 'data/subtitles/*.srt']
    for target in targets:
        for f in glob.glob(target):
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

if __name__ == '__main__':
    clean()
