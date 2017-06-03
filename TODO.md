# TODO

## What will it do?

### Watch a signal directory that will contain movies and tv shows.
* Use inotify for python (linux only) 

### When a new item appears it will first be found on either thetvdb.com or themoviedb.org 
* Both seems to have a free to use API with n account
* Then they will be used to find and rename the files
* Note: Might not have to find them in the database since plex does that.  Just need a clean rename.

### Once the file’s new name is found then it is time to covert it.
* Use ffmpeg and ffmprobe
* Maybe create my own little API lib for ffmpeg to convert to h254 and acc/ac3 audio.
* Also add option to burn in subtitles using a given srt file or the file already embedded
* Add an option to embed a subtitle

### Once the file has been converted send it to the correct spot in plex (use my own mini text file db to see if it is in the tv shows list or movies list and go from there.
