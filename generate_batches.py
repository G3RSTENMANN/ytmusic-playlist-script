from ytmusicapi import YTMusic
import re, time, os

## -- top-level paths & vars
BACKUP_LOCATION_PATH = "/media/luca/media/music/ytmusic-backups/"
LINKS_FILE_NAME = "full-list.txt"
OUTPUT_FILE_NAME = "links.txt"

OUTPUT_PATH = f"{BACKUP_LOCATION_PATH}{OUTPUT_FILE_NAME}"

def write(txt):
    with open(OUTPUT_PATH, "a") as f:
        print(txt, file=f)
    print(txt)

def write_buffer(buf):
    for x in buf:
        write(x)

## extract song links
# -------------------

# -- delete output file
try:
    os.remove(OUTPUT_PATH)
except:
    print("Warning: couldn't remove file!")
    time.sleep(5)

# -- Get yt music object
yt = YTMusic()

# -- keep track of the batches
pl_c = 0
batch_c = 2
song_c = 0
song_buffer = []
write("### Batch 1")
next_batch_is_test = False

# -- get links for all playlists
with open(f"{BACKUP_LOCATION_PATH}{LINKS_FILE_NAME}", "r") as links: # parse link file
    for l in links:
        # skip batches
        if (re.search("^### ", l)):
            if (re.search("^### Batch WIP", l)):
                break
            if (re.search("^### Batch TEST", l)):
                write(f"### ==> total of {song_c} songs")
                write_buffer(song_buffer)
                song_buffer = []
                write("### -")
                write(f"### Batch TEST")
                song_c = 0
            continue

        # extract playlist ids
        re_pl_id = re.search("(?<=list=).+(?= # )", l)
        if not re_pl_id:
            write("Something went wrong when reading the following link: " + l)
            continue
        pl_id = re_pl_id.group()
        pl_c += 1

        # parse tracks in playlist-response
        try:
            pl = yt.get_playlist(pl_id, limit=None)
            pl_title = pl["title"]
            track_count = pl["trackCount"]

            if song_c + track_count > 500:
                write(f"### ==> total of {song_c} songs")
                write_buffer(song_buffer)
                song_buffer = []
                write("### -")
                write(f"### Batch {batch_c}")
                song_c = track_count
                batch_c += 1
            else:
                song_c += track_count

            song_buffer.append(f"https://music.youtube.com/playlist?list={pl_id} # {pl_title}")

            if song_c > 350:
                write(f"### ==> total of {song_c} songs")
                write_buffer(song_buffer)
                song_buffer = []
                write("### -")
                write(f"### Batch {batch_c}")
                song_c = 0
                batch_c += 1

        # if this fails, it's probably because the playlist is not set to public or unlisted
        except Exception as e:
            print(f"Something went wrong with playlist https://music.youtube.com/watch?list={pl_id}")
            print(e)
            time.sleep(1)

write(f"### ==> total of {song_c} songs")
write_buffer(song_buffer)
write("### -")
write(f"### fini. {pl_c} playlists written.")