# Setup
## Prerequisites

1. PYTHON - As this is a python tool, you need python, obviously :wink:. Version 3.x is needed. Ask your local search engine to aid you with installation...
2. SHOTWELL - Shotwell is a personal photo manager made for Linux. This program is adapted to Shotwells organization structure and database layout, 
but it should take little programming effort to port its ideas to other image managers.
3. COFFEE - a drink you should enjoy hot or frozen
4. TERMINAL - this is no GUI program, working at the command line should not fear you :nauseated_face:
5. IMPROVISATION - this document is based on my experience with Ubuntu Linux (20.04 right now), using other OSes will force you to 
adapt!

## Download
1. I will use /opt as a base directory, so `cd /opt`
2. download (https://github.com/medmen/deepface4shotwell/archive/refs/heads/master.zip)
3. unpack to /opt/deepface4shotwell `unzip master.zip`

## Create and start virtual env
CAUTION: you may need to call python using `python3` instead of `python` 

There is far more than one way to deal with virtual envs.  
I will address pythons built in venv and virtualenvwrapper, feel free to use whatever you like :-)  
You may name your virtual environment anything you like, i will use 'df4sw' 

### virtualenvwrapper

`mkvirtualenv df4sw`  
`workon df4sw`

### venv

`python -m venv df4sw`  
`source df4sw/bin/activate`

## Install Dependencies

`pip install -r requirements.txt` 

## Prepare known faces

within the `Training` folder  
add a folder for every person you want to identify  
within that folder add pictures of that person.  
Refer to the 
[readme_training.md](Training/readme_training.md)
 for details. 

## Point to your image directory

check or edit [config.py](config.py) to point the variable 'images_dir' to the directory 
containing your shotwell images or any subdirectory.   

## run (finally :wink: )

`python main.py` will trigger the process.  
Now its time to get some coffee..  
This will take a lot of time, expect about 20 seconds per image (!), maybe longer if images holding multiple faces need to be scanned.
