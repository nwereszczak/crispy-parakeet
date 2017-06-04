# TODO

## Note: Looks like sickrage can rename and move the tv shows into plex.  Kind of disapointing since it does some of this.

## What will it do?

### Watch a signal directory that will contain movies and tv shows.
* Use inotify for python (linux only) 

### When a new item appears it will be renamed  
* Will end up using 'filebot' for now.  Using subproccess to call it from command line since it is programmed in java :(. 
* Maybe I will look at it and recode it in python at some point to use as a lib.
* Since it's guess work isnt the best I will keep a db of the movies/tvshows I have so far.  Might be able to just link it with sickrage or steal its db file.
* Find them in the database since plex does that.  Just need a clean rename.

### Once the file's new name is found then it is time to covert it.
* Use ffmpeg and ffmprobe
* Maybe create my own little API lib for ffmpeg to convert to h254 and acc/ac3 audio.
* Also add option to burn in subtitles using a given srt file or the file already embedded
* Add an option to embed a subtitle

### Once the file has been converted send it to the correct spot in plex (use my own mini text file db to see if it is in the tv shows list or movies list and go from there.
