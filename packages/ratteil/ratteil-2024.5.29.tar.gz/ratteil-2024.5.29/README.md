 RatTeil 
=======

**RatTeil** is a python-ffmpeg app to stream the Holly Quran to a youtube channel.

More detailed docummentaion is in the "docs" dictinory

How to install on
-----------------

Android
-------

1. Install Termux app.
2. Run *pkg update -y*.
3. Then *pkg install python wget ffmpeg -y*.
4. Then *python -m pip install ratteil*.
5. Run *ratteil -h* to see availables options.

Linux, Debian, etc
-------------------

1. Run *apt-get update -y*
2. Then *apt-get install python wget ffmpeg -y*
3. Then *python -m pip install ratteil*
4. Run *ratteil -h* to see availables options.

Or 

1. clone ratteil repo change to ratteil folder.
2. Run *sh install.sh*.
3. Run *python __main__.py -h* to see options.

Or 

1. download ratteil package from github or py
2. install requirements *apt-get install python ffmpeg wget -y*.
3. Run *python -m pip install <ratteil_package_file_path>*

Quick start
------------

before running this command make sure you put your images/videos that will be used as stream background under.
> *~/RatTeil-resources/imgs/*

and your video introduction under 
> *~/RatTeil-resources/fixer/*

file name must be introduction.mp4 and conlusion.mp4

1. Run *python -m pip install ratteil*
2. Run *ratteil -t youtube*
3. copy authentication links 
4. Follow google authentication link
5. Enter the authentication code/token and verfiy your authority
6. Done; stream'll start in view moments
