# ----------------------------------------- #
# posUpdateLoop.pyw                         #
# Speed_Limit75                             #
#                                           #
# This file runs a loop to refresh data in  #
# the input folder every 5 seconds,         #
# regardless if it can connect to FSUIPC or #
# XPUIPC.                                   #
# ----------------------------------------- #

# Import libarys
import time
import threading
import track
import json
import web
import config
import os

# Set variables
stop = False
pirepID = ""

# Define functions
def read(x):
    file = open(str(os.getenv('APPDATA')) + '/xACARS/input/' + x + '.txt', "r")
    toreturn = file.read()
    print(file.read())
    file.close()
    print(toreturn)
    return toreturn

def loop():
    global pirepID
    while True:
        if config.useFSUIPC == True: track.beginTrack()
        try:
            if config.useFSUIPC == True: track.posUpdate()

            
            exportdata = {"lat": read('lat'),"lon": read('lon'),"heading": read('heading'),"altitude": read('altitude'),"vs": read('vs'),"gs": read('gs')}
            exportdata = {"positions": [exportdata]}

            exportdata = json.dumps(exportdata)
            
            web.post(config.website + '/api/pireps/' + pirepID + '/acars/position', exportdata)

            print(exportdata)
        except Exception as e:
            print(e)

        time.sleep(5)

        if stop == True:
            break

def startLoop(x):
    global thread
    global pirepID
    pirepID = x
    thread = threading.Thread(target=loop)
    thread.start()

def stopLoop():
    global thread
    global stop
    stop = True
    track.endTrack()