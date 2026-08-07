import os, sys, shutil, re

# -- you have to set these!
BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
FOLDER_NAME = "backup-2026-06-09"
LIBRARY_THUMBNAIL_FILE = "../library.jpg"

COVERS_DIR = f"{BACKUP_LOCATION_PATH}covers/playlists/"
TARGET_DIR = f"{BACKUP_LOCATION_PATH}{FOLDER_NAME}/"
LIBRARY_LOGO_PATH = f"{COVERS_DIR}{LIBRARY_THUMBNAIL_FILE}"

shutil.copyfile(LIBRARY_LOGO_PATH, TARGET_DIR + "cover.jpg")

covers = os.listdir(COVERS_DIR)
for c in covers:
    playlist = re.search(".+(?=.jpg)", c).group()

    try:
        shutil.copyfile(COVERS_DIR + c, f"{TARGET_DIR}{playlist}/cover.jpg")
    except:
        print(f"Something went wrong with playlist '{playlist}'...")
