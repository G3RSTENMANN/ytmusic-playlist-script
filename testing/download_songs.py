import re, sys, os, datetime, subprocess, time, shutil

# -- top-level paths
BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
SCRIPT_PATH = "/home/luca/srv/ripping/ytmusic/"
JS_RUNTIME = "deno:/home/luca/.deno/bin/deno"

## functions & classes
def create_dir(name):
    try:
        os.mkdir(name)
    except:
        print("creating directory failed")
        sys.exit()

# (das ist bisschen scheise)
class Idx:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 1

    def inc(self):
        if self.z==9:
            self.z=0
            if self.y==9:
                self.y=0
                if self.x==9:
                    self.x=0
                    if self.w==9:
                        print("FATAL: Too many songs in the playlist")
                        sys.exit()
                    else:
                        self.w+=1
                else:
                    self.x+=1
            else:
                self.y+=1
        else:
            self.z+=1
    
    def get(self):
        return f"{self.w}{self.x}{self.y}{self.z}"

# -- prepare target directory
date = datetime.datetime.now().date()
root_dir = f"{BACKUP_LOCATION_PATH}backup-{date}/"
try:
    os.mkdir(root_dir)
except:
    print(f"Error when creating directory '{root_dir}'.")
    response = input("Try to delete it? (y/n):")
    if (response == "y"):
        shutil.rmtree(root_dir)
        os.mkdir(root_dir)
        print("Target directory overwritten.\n")
    else:
        print("exiting...")
        sys.exit()

# -- get playlist file-names
files = os.listdir(f"{SCRIPT_PATH}playlists/")
errors = []
skipped = []

# -- download songs for each playlist
for filename in files:
    # prepare playlist-specific vars
    pl_name = re.search(".+(?=.txt)", filename).group()
    create_dir(root_dir + pl_name)
    index = Idx()

    # iterate songs
    with open(f"{SCRIPT_PATH}playlists/{filename}", "r") as file:
        for song in file:

            print(f"Beginning download of next song...\n")
            retries = 0
            success = False

            while not success and retries <= 5:

                if retries != 0:
                    print("Retry download after 10 seconds...")
                    time.sleep(3)
                    print(f"Retrying now ({retries}/5):\n")

                # check if the link is busted
                if re.findall("(?<=v=)None", song):
                    # skip broken link but still increment index
                    print(f"Broken link with index {index.get()} was skipped!\n")
                    skipped.append(f"Song {index.get()} in playlist {pl_name}")
                else:
                    # get corresponding ytmusic object
                    ytdlp_command = f'yt-dlp --js-runtimes "{JS_RUNTIME}" --extract-audio --audio-format mp3 -o "{root_dir}/{pl_name}/{index.get()} - %(title)s.%(ext)s" "{song}"'
                    result = ""
                    try:
                        result = subprocess.run(ytdlp_command, check=True, shell=True, capture_output=True)
                        output = result.stdout.decode("utf-8")
                        print(output)
                        if ("ERROR" in output):
                            if (retries==5):
                                errors.append(f"Song from playlist '{pl_name}' with index {index} has failed!\nAdditional information: {output}")
                        else:
                            success = True
                            print(f"Completed Download of song with index {index.get()}!")
                            print("------------------------------------------")
                            print(f"Number of current errors: {len(errors)}.")
                            print(f"Number of skipped songs so far: {len(skipped)}")
                    except:
                        print("\nSOMETHING WENT WRONG WITH EXECUTING THE COMMAND!!!\n")
                        if (retries==5):
                            errors.append(f"Song from playlist '{pl_name}' with index {index} has failed!")
                
                retries += 1

            print("Continuing with the next song in 3 seconds...")
            time.sleep(3)
            index.inc()

print("\n-------------------------------------------------------\n")
print(f"Process finished with a total of {len(errors)} errors.\n")
print("-------------------------------------------------------\n\n")

print("The following songs were skipped:")
for s in skipped:
    print(f" - {s}")

print("\n\nThe following errors were encountered:")
for error in errors:
    print(error)
    print("\n")

print("\nFinished Backup!")