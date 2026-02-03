import os
import glob

def clean():
    print("Cleaning Subtitles (ASS, SRT, VTT)...")
    # Subtitles can be in data/subtitles or data/audio (temp vtt)
    targets = [
        'data/subtitles/*.ass', 
        'data/subtitles/*.srt', 
        'data/subtitles/*.vtt',
        'data/audio/*.vtt'  # Edge-tts sometimes leaves vtt in audio folder
    ]
    for target in targets:
        for f in glob.glob(target):
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

if __name__ == '__main__':
    clean()
