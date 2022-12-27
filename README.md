# Christmas Tree Lights (CTL) 2.0
Flask app to control christmas tree lights using rpi

*spoiler alert: still might be buggy*

Inspired by https://www.instructables.com/Raspberry-Pi-Christmas-Tree-Light-Show/ (modified code in `playsongs.py`)

Also checkout this link https://drive.google.com/drive/folders/1Ku2mxV9_Gpv29n7ya_VAf92_tAC22TIS to make new sequences (some of the files are in this repo in case the drive folder would get deleted)

## Requirements
There are some particular libraries that you need to install (`pygame`, `werkzeug`, `mutagen`, `alsaaudio`).
I created a box with a TFT 1.8inch display, so for that additional libraries (`adafruit-rgb-display`, `digitalio`, `board`) are required too (I might create a version without the display)

## Running and customising the database
After installing all the libraries just `cd christmas_tree_lights2.0` and run `python3 application.py`. This will run it with pre-made database `chtrli.db`, which uses files from `songs_mp3`, `seq_txt` and `static/song_imgs` folders. Feel free to remove them, run `python3 create_database`. You should get a database with two users - **admin** (password is admin) and the same for **user**, one suggestion and empty song list.  
**There is not _yet_ good error handling for empty song list, so after adding one song the server may crash, just restart it and it should be fine after that.**

### To-be-aware-of features
- Volume cannot be controled by a user that is not signed in, also such users cannot like songs, or suggestions.
- Admin user can alter the playlist, remove suggestions and add/remove admin privileges.

## TODO
- playlist page doesn't automatically refresh the time line with current time when the song expands (it stays on the song on which it was most recently refreshed)
- the code in application.py needs a lot of improvements since I was a bit in a hurry to make it work before Christmas and didnt have time to do it properly (esp. `get_songs()` can be often used much more efficiently - sometimes is used only to determine one song or number of songs).
