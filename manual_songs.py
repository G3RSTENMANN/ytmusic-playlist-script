import re, sys, os, datetime, subprocess, time, shutil

## -- top-level paths
BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
SCRIPT_PATH = "/home/luca/srv/ripping/ytmusic-playlist-script/"
JS_RUNTIME = "deno:/home/luca/.deno/bin/deno"
LINKS_FILE_NAME = "links.txt"

BACKUP_FOLDER = "backup-2026-06-09"
TARGET_DIR = f"{BACKUP_LOCATION_PATH}{BACKUP_FOLDER}/"
LINKS_FILE = f"{TARGET_DIR}manual.txt"


print(f"Starting manual downloads:\n")

time_start = datetime.datetime.now()
errors = []

with open(LINKS_FILE, "r") as file:
    for song in file:

        print(f"Beginning download of next song...\n")
        success = False

        # extract information from the line
        idx = re.search("^[0-9]{4,4}", song).group()
        song_link = re.search("(?<=^[0-9]{4,4} ).+(?= #)", song).group()
        playlist_name = re.search("(?<= # ).+", song).group()

        # get corresponding ytmusic object
        ytdlp_command = f'yt-dlp --js-runtimes "{JS_RUNTIME}" -f "ba" --extract-audio --audio-format best --audio-quality 0 -o "{TARGET_DIR}/{playlist_name}/{idx} - %(title)s.%(ext)s" "{song_link}"'
        output = ""
        try:
            result = subprocess.run(ytdlp_command, check=True, shell=True, capture_output=True)
            output = result.stdout.decode("utf-8")
            print(output)
            success = True
            print(f"Completed Download of song with index {idx}!")
            print(f"Saved to file {re.search("(?<=\[ExtractAudio\] Destination: ).+\.opus", output).group()}")
            print(f"Timestamp: {datetime.datetime.now()}")
            print("------------------------------------------")
            print(f"Number of current errors: {len(errors)}.")
        except Exception as e:
            print("\nSOMETHING WENT WRONG WITH EXECUTING THE COMMAND!!!\n")
            print(e)
            print("\nOutput:")
            print(output)
            print("")

            errors.append(f"Song from playlist '{playlist_name}' with index {idx} has failed! Link: {song_link}")
        
        
        if (success):
            print("Continuing with the next song in 3 seconds...")
            time.sleep(3)
        else:
            print("There was an error when downloading this song!")
            input("Press any button to continue...")


print("\n-------------------------------------------------------\n")
print(f"Process finished with a total of {len(errors)} errors.\n")
print("-------------------------------------------------------\n\n")

print("\n\nThe following errors were encountered:\n")
for error in errors:
    print(error)

print("\nManual song fix finished successfully!")
print(f"Time passed: {datetime.datetime.now() - time_start}")
print("")
