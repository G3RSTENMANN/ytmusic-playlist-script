from ytmusicapi import YTMusic
import re, os, shutil

# -- clear playlists directory
shutil.rmtree("playlists")
os.mkdir("playlists")
# try:
#     os.rmdir("playlists")
# except:
#     print("removing directory failed")
# try:
#     os.mkdir("playlists")
# except:
#     print("creating directory failed")

# -- Get yt music object
yt = YTMusic()

# -- keep track of failed songs
total_fails = 0
failed_songs = []

# -- get links for all playlists
with open("/media/luca/media/music/ytmusic-backups/links.txt", "r") as links: # parse link file
    for l in links:
        # extract playlist ids
        re_pl_id = re.search("(?<=list=).+", l)
        pl_id = re_pl_id.group()
        fails = 0

        # parse tracks in playlist-response
        try:
            pl = yt.get_playlist(pl_id, limit=None)
            with open(f"playlists/{pl["title"]}.txt", "w") as f:
                for x in pl["tracks"]:
                    # extract video id
                    f.write(f"https://music.youtube.com/watch?v={x["videoId"]}\n") # sometimes, the id gets returned as null!
                    if x["videoId"] == None:
                        fails += 1
                        failed_songs.append({"pl_id": pl_id, "pl_name": pl["title"], "song_name": x["title"]})

                # inform about failures in this playlist
                print(f"Total of {fails} failures for playlist {pl["title"]}.")
                total_fails += fails

        # if this fails, it's probably because the playlist is not set to public or unlisted
        except:
            print(f"Something went wrong with playlist https://music.youtube.com/watch?list={pl_id}")

# -- print info about failed songs
try:
    print (f"\nExtraction finished with total number of {total_fails} failures...")
    for x in failed_songs:
        print(f"  - Song '{x["song_name"]}' from playlist '{x["pl_name"]}' (https://music.youtube.com/watch?list={x["pl_id"]})")
    print("\nManual intervention required!")
except:
    print("\nCould not print relevant information...")