from ytmusicapi import YTMusic
import re, sys, os, datetime, subprocess, time, shutil
from functools import reduce

## -- top-level paths & vars
BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
#BACKUP_LOCATION_PATH = "/home/luca/srv/ripping/lehramt-gang/"
SCRIPT_PATH = "/home/luca/srv/ripping/ytmusic-playlist-script/"
JS_RUNTIME = "deno:/home/luca/.deno/bin/deno"
LINKS_FILE_NAME = "links.txt"

SONG_DELAY = 3  # time to wait before the download of the next song
EMBED_METADATA = False
EMBED_THUMBNAIL = True

# decide which batches are to be downloaded; 0 is equivalent to all batches
# BATCH = ["TEST"]  
# BATCH = [0]
BATCH = [1,2,3] # -- ca. 1000 songs <=> ca. 5h?
# BATCH = [4,6,7] # -- ca. 840 songs <=> ca. 4.5h?
# BATCH = [8,9,10] # -- ca. 950 songs <=> ca. 5h?

TARGET_DIR = f"{BACKUP_LOCATION_PATH}backup-{datetime.datetime.now().date()}-batch{'all' if 0 in BATCH else reduce(lambda a,b: a+f"{b}", BATCH, "")}/"
# TARGET_DIR = f"{BACKUP_LOCATION_PATH}unsorted/xyz/"
LOG_OUTPUT_PATH = f"{TARGET_DIR}log.txt"

AUDIO_QUALITY = "best" # must be either "best" or "mp3"

## functions & classes
def log(txt):
    with open(LOG_OUTPUT_PATH, "a") as f:
        print(txt, file=f)
    print(txt)

def create_dir(name):
    try:
        os.mkdir(name)
    except:
        log("creating playlist-directory failed")
        log("this error can't be handled")
        log("exiting...")
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
                        log("FATAL: Too many songs in the playlist")
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


## prepare initial directories
# ----------------------------

# -- check that BATCH is nonempty
if (len(BATCH) == 0):
    print("Fatal: Please set BATCH to an acceptable value!")
    sys.exit()

# -- clear playlists directory
shutil.rmtree(f"{SCRIPT_PATH}playlists")
os.mkdir(f"{SCRIPT_PATH}playlists")

# -- prepare target directory (log will be available after this)
try:
    os.mkdir(TARGET_DIR)
except:
    print(f"Error when creating directory '{TARGET_DIR}'.")
    response = input("Try to delete it? (y/n):")
    if (response == "y"):
        shutil.rmtree(TARGET_DIR)
        os.mkdir(TARGET_DIR)
        log("\nTarget directory overwritten.\n")
    else:
        print("exiting...")
        sys.exit()

# -- keep the time
time_start = datetime.datetime.now()


## extract song links
# -------------------

# -- Get yt music object
yt = YTMusic()

# -- keep track of failed songs
total_fails = 0
failed_songs = []

# -- batch logic
do_batch = True

# -- get links for all playlists
with open(f"{BACKUP_LOCATION_PATH}{LINKS_FILE_NAME}", "r") as links: # parse link file
    for l in links:

        # check for batch
        if (re.search("^### ", l)):
            if (re.search("^### Batch TEST", l)):
                do_batch = "TEST" in BATCH
            elif (re.search("^### Batch ", l)):
                batch_number = int((l.strip())[-1])
                do_batch = 0 in BATCH or batch_number in BATCH
            continue

        # maybe skip link
        if not do_batch:
            continue

        # extract playlist ids
        re_pl_id = re.search("(?<=list=).+(?= # )", l)
        if not re_pl_id:
            log("Something went wrong when reading the link! Skipping it...")
            continue
        pl_id = re_pl_id.group()
        fails = 0

        # parse tracks in playlist-response
        try:
            pl = yt.get_playlist(pl_id, limit=None)
            with open(f"{SCRIPT_PATH}playlists/{pl["title"]}.txt", "w") as f:
                for x in pl["tracks"]:
                    # extract video id
                    f.write(f"https://music.youtube.com/watch?v={x["videoId"]}\n") # sometimes, the id gets returned as null!
                    if x["videoId"] == None:
                        fails += 1
                        failed_songs.append({"pl_id": pl_id, "pl_name": pl["title"], "song_name": x["title"]})

                # inform about failures in this playlist
                log(f"Total of {fails} failures for playlist {pl["title"]}.")
                total_fails += fails

        # if this fails, it's probably because the playlist is not set to public or unlisted
        except:
            log(f"Something went wrong with playlist https://music.youtube.com/watch?list={pl_id}")

# -- log info about failed songs
try:
    log (f"\nExtraction finished with total number of {total_fails} failures...")
    for x in failed_songs:
        log(f"  - '{x["song_name"]}' from playlist '{x["pl_name"]}'  (https://music.youtube.com/watch?list={x["pl_id"]})")
    log("\nManual intervention may be required!")
except:
    log("\nCould not log relevant information...")

log("\n\nBeginning Downloads:\n")



## download the songs
# --------------------

# -- get playlist file-names
files = os.listdir(f"{SCRIPT_PATH}playlists/")
errors = []
skipped = []

# -- download songs for each playlist
for filename in files:
    # prepare playlist-specific vars
    pl_name = re.search(".+(?=.txt)", filename).group()
    create_dir(TARGET_DIR + pl_name)
    index = Idx()

    # iterate songs
    with open(f"{SCRIPT_PATH}playlists/{filename}", "r") as file:
        for song in file:

            log(f"Beginning download of next song...\n")
            retries = 0
            success = False

            while not success and retries <= 5:

                if retries != 0:
                    log("Retry download after 10 seconds...")
                    time.sleep(10)
                    log(f"Retrying now ({retries}/5):\n")

                # check if the link is busted
                if re.findall("(?<=v=)None", song):
                    # skip broken link but still increment index
                    log(f"Broken link with index {index.get()} was skipped!\n")
                    skipped.append(f"Song {index.get()} in playlist {pl_name}")
                    success = True
                else:
                    # get corresponding ytmusic object
                    # this command basically does the following:
                    # 1. download audio-only in the best available quality
                    # 2. convert download with ffmpeg to audio file with the best audio format and quality
                    
                    ytdlp_command = f'yt-dlp --js-runtimes "{JS_RUNTIME}" -f "ba" {"--embed-metadata " if EMBED_METADATA else ""}{"--embed-thumbnail " if EMBED_THUMBNAIL else ""}--extract-audio --audio-format {AUDIO_QUALITY} --audio-quality 0 -o "{TARGET_DIR}/{pl_name}/{index.get()} - %(title)s.%(ext)s" "{song}"'
                    output = ""
                    try:
                        result = subprocess.run(ytdlp_command, check=True, shell=True, capture_output=True)
                        output = result.stdout.decode("utf-8")
                        # log(output) --> i dont want to print everything
                        if ("ERROR" in output):
                            if (retries==5):
                                errors.append(f"Song from playlist '{pl_name}' with index {index} has failed!\nAdditional information: {output}")
                        else:
                            success = True
                            log(f"\nCompleted Download of song with index {index.get()}!")
                            log(f"Saved to file {re.search("(?<=\[ExtractAudio\] Destination: ).+\.(opus|mp3)", output).group()}")
                            log(f"Timestamp: {datetime.datetime.now()}")
                            log("------------------------------------------")
                            log(f"Number of current errors: {len(errors)}.")
                            log(f"Number of skipped songs so far: {len(skipped)}")
                    except Exception as e:
                        log("\nSOMETHING WENT WRONG WITH EXECUTING THE COMMAND!!!\n")
                        log(e)
                        log("\nOutput:")
                        log(output)
                        log("")
                        if (retries==5):
                            errors.append(f"Song from playlist '{pl_name}' with index {index.get()} has failed! Link: {song}")
                
                retries += 1

            log(f"Continuing with the next song in {SONG_DELAY} seconds...")
            time.sleep(SONG_DELAY)
            index.inc()

log("\n-------------------------------------------------------\n")
log(f"Process finished with a total of {len(errors)} errors.\n")
log("-------------------------------------------------------\n\n")

log("The following songs were skipped:")
for s in skipped:
    log(f" - {s}")

log("\n\nThe following errors were encountered:\n")
for error in errors:
    log(error)

log("\nFinished Backup successfully!")
log(f"Time passed: {datetime.datetime.now() - time_start}")
log("")
