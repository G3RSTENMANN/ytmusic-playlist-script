from ytmusicapi import YTMusic
import json

yt = YTMusic()

# -- Test general response structure
# playlist = yt.get_playlist("https://music.youtube.com/playlist?list=PL6_Il-Q-by6Tbak8l74tgAJt7LmHuN1yw")
# playlist = yt.get_playlist("PL6_Il-Q-by6Tbak8l74tgAJt7LmHuN1yw")
# playlist = yt.get_playlist("PL6_Il-Q-by6T-XzcqzDBF9ZYSU7ZRBO-H")
# playlist = yt.get_playlist("PL6_Il-Q-by6SDA12lT8Kn92AKKJLo4z36")
playlist = yt.get_playlist("PL6_Il-Q-by6T40xyzU1SxWaftHaxZdaYb", limit=None)
with open("testing/output.txt", "w") as f:
    playlist_output = json.dumps(playlist, indent=4)
    f.write(playlist_output)

count = 0
for t in playlist["tracks"]:
    count += 1
print(f"{count} tracks counted")
