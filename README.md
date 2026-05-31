> Disclaimer: This is a small script i wrote up fairly quickly myself. I can't promise that it will always run perfectly.

### Introduction
When I wanted to use yt-dlp with yt-music playlists I ran into the problem that some of the songs in my playlists were available on yt-music but not on regular YouTube. This resulted in yt-dlp just skipping these songs and this happened so frequently that it made the whole thing redundant.
I figured out that you can still access the "unavailable" songs on YouTube though, provided you have the video of said song. This is why I wrote this program to simplify the process.
I rely heavily on the project "ytmusicapi" and sometimes it still fails to fetch a video-ID for some songs. However, this number is staggeringly lower than what I got from regular yt-dlp.

To use this, all you need to do is:
- check off all the dependencies
- adjust the constants/paths in "yt\_music\_playlists.py" to your liking
- run the script "yt\_music\_playlists.py"

If you want to tweak the yt-dlp functionality you can edit the corresponding shell-command (currently in line 170) to your liking.

##### Dependencies:
- python 3.x
- ytmusicapi (install via pip)
- a working cli setup for yt-dlp (including ffmpeg and js-runtime)
