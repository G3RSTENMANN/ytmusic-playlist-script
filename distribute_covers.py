import os, sys, shutil, re

BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
SCRIPT_PATH = "/home/luca/srv/ripping/ytmusic/"
LINKS_FILE_NAME = "links.txt"

COVERS_DIR = f"{BACKUP_LOCATION_PATH}covers/playlists/"
LIBRARY_LOGO_PATH = f"{COVERS_DIR}../library.jpg"
TARGET_DIR = f"{BACKUP_LOCATION_PATH}backup-2026-06-09/"
LOG_OUTPUT_PATH = f"{TARGET_DIR}log.txt"

shutil.copyfile(LIBRARY_LOGO_PATH, TARGET_DIR + "cover.jpg")

covers = os.listdir(COVERS_DIR)
for c in covers:
    playlist = re.search(".+(?=.jpg)", c).group()

    try:
        shutil.copyfile(COVERS_DIR + c, f"{TARGET_DIR}{playlist}/cover.jpg")
    except:
        print(f"Something went wrong with playlist '{playlist}'...")
