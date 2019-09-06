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
import json
import web
import config
import os

# Set variables
stop = False
pirepID = ""
delay = 5

# Define functions
def getNewDelay(): # Updates the delay based on current data
    global delay
    ias = float(read("IAS"))
    vs = float(read("vs"))

    if ias <= 150:
        delay = 5
    elif ias > 150 and ias <= 200:
        delay = 7
    elif ias > 200 and ias <= 250:
        delay = 10
    else:
        if vs < 0:
            vs = vs - vs - vs

        if vs >= 400 and ias > 250:
            delay = 15
        elif vs < 400 and ias > 250:
            delay = 30
        else:
            delay = 5

def read(x): # Read data from the input folder
    file = open(str(os.getenv('APPDATA')) + '/xACARS/input/' + x + '.txt', "r")
    toreturn = file.read()
    print(file.read())
    file.close()
    print(toreturn)
    return toreturn

def loop(): # Check for updates in a loop
    global pirepID
    while True:
        try:
            exportdata = {"lat": read('lat'),"lon": read('lon'),"heading": read('heading'),"altitude": read('altitude'),"vs": read('vs'),"gs": read('gs')}
            exportdata = {"positions": [exportdata]}

            exportdata = json.dumps(exportdata)
            
            web.post(config.website + '/api/pireps/' + pirepID + '/acars/position', exportdata)

            print(exportdata)
        except Exception as e:
            print(e)

        time.sleep(delay)
        getNewDelay()

        if stop == True:
            break

def startLoop(x): # Starts the loop in a new thread
    global thread
    global pirepID
    pirepID = x
    thread = threading.Thread(target=loop)
    thread.start()

def stopLoop(): # Stops the loop in the 'new' thread
    global thread
    global stop
    stop = True