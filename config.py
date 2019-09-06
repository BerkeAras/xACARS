# ----------------------------------------- #
# config.py                                 #
# Speed_Limit75                             #
#                                           #
# This file read all ini files and sets the #
# variables to reflect their settings. It   #
# also make sure all .ini files that are    #
# needed exist, somthing that used to be    #
# handled by its own file.                  #
# ----------------------------------------- #

# Import required libarys.
import configparser
import os

# Make sure all .ini files exist
if os.path.exists('airlines.ini') == False:
    file = open("airlines.ini", 'w')
    file.write("[DEFAULT]\n")
    file.write("name=\n")
    file.write("url=\n")
    file.write("apikey=None Saved\n")
    file.close()

if os.path.exists('settings.ini') == False:
    file = open("settings.ini", 'w')
    file.write("[DEFAULT]\n")
    file.write("darkMode = False\n")
    file.write("checkForUpdatesOnStart = True\n")
    file.write("getPreReleaseVersions = False\n")
    file.write("loginMessageEnabled = True")
    file.close()

# Set static variables
version = "v1.0.0-alpha3"

# Pre-define Variables
airline = "None"
website = ""
APIKey = ""
list = []
websites = []
savedAPIKeys = []
usernames = []

# Change local variable
def changeVar(x, y):
    if x == "website":
        global website
        website = y
    elif x == "airline":
        global airline
        airline = y
    elif x == "APIKey":
        global APIKey
        y.replace(" ", "")
        y = y.strip()
        APIKey = y

# Reloads airlines.ini
def reloadList():
    global list
    global websites
    global savedAPIKeys
    global usernames
    list = []
    websites = []
    savedAPIKeys = []
    config = configparser.ConfigParser()
    config.read("airlines.ini")
    configSections = config.sections()
    try:
        list.append(config["1"]['name'])
        websites.append(config["1"]['URL'])
        savedAPIKeys.append(config["1"]['apikey'])
        usernames.append(config["1"]['username'])
        for key in configSections:
            list.append(config[key]['name'])
            websites.append(config[key]['URL'])
            savedAPIKeys.append(config[key]['apikey'])
            usernames.append(config[key]['username'])
    except Exception as e:
        print(e)
    
# Converts a string to a boolean.
def stringToBool(x):
    if x == "true":
        return True
    elif x == "True":
        return True
    elif x == "false":
        return False
    elif x == "False":
        return False
    else:
        raise TypeError("Expected True, true, False, or false: not " + x)

# Load airline list
reloadList() 

# Read settings
config = configparser.ConfigParser() 
config.read("settings.ini")
darkMode = config["DEFAULT"]["darkMode"]
checkUpdate = config["DEFAULT"]["checkForUpdatesOnStart"]
getPreRel = config["DEFAULT"]["getPreReleaseVersions"]
try:
    loginMessage = config["DEFAULT"]["loginMessageEnabled"]
    failed = False
except Exception:
    failed = True
    file = open('settings.ini', 'a')
    file.write("\nloginMessageEnabled = True")
    file.close()
    loginMessage = True

# Change the "True/False" variables to a boolean
darkMode = stringToBool(darkMode)
checkUpdate = stringToBool(checkUpdate)
getPreRel = stringToBool(getPreRel)
if failed == False:
    loginMessage = stringToBool(loginMessage)