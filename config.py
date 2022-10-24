#!/usr/bin/env python

# import preprocessing
from pathlib import Path

# lets keep a log file
logfile = 'deepface4sw.log'

#############
# the directory to search for faces
###
# you can provide a full path
# images_dir = "/home/me/Pictures/2021/"
# or abstract from user's home directory
images_dir = Path.home().joinpath('Pictures', '2021')

###
# path to the shotwell database
###
shotwell_db = Path.home().joinpath('.local', 'share', 'shotwell', 'data', 'photo.db')

###
# a directory of "known faces" sorted by name
# each name needs at least one image.
# example:
# # #
# alice
#       - alice1.jpg
#       - alice2.jpg
# bob
#       - bob1.jpg
# charly
#       - charly1.jpg
###
known_faces = "Training/"

###
# if you want to, you can keep a directory of faces found
# so you can check for errors later and maybe retrain the model
enable_testing = True
testing_faces = "Testing/"

# a text file to keep track of images we have covered already
known_images = 'known_images.txt'

# set log level to either ERROR, WARNING, INFO, DEBUG
log_level = 'DEBUG'
