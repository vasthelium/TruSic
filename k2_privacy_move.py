import os
import pathlib
import shutil
from k2_privacy_killswitch import privacy_switch


def movefiles():
    _, speech_files = privacy_switch() #throwaway, dont care about first return
    audio_files = "/Users/hussain/raw_soundfiles"

    moved_count = 0
    
    for files in speech_files:
        file_name = files["file_name"]
        full_ab_path = os.path.join(audio_files, file_name)
        if os.path.exists(full_ab_path):
            shutil.move(full_ab_path, "/Users/hussain/raw_soundfiles_trash")
            moved_count +=1
        else:
            print (f"File not found: {full_ab_path}")

    print(f"Files moved: {moved_count}")

if __name__ == "__main__":
    movefiles()
