# ----------------------------------------- #
# listAirlines.pyw                          #
# Speed_Limit75                             #
#                                           #
# This file manages adding and deleting     #
# all virtual airlines the user logs into.  #
# ----------------------------------------- #

# Import libarys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config as configLib
import configparser

# Define functions
def terminateNewAirline(): ## Closes the new airline creation screen
    global name
    global url
    global apiKey
    global newAirWindow
    global username
    global List

    List = configLib.list
    name = name.get()
    url = url.get()
    apiKey = apiKey.get()
    username = username.get()
    
    a = 0
    for key in List:
        a = a + 1

    config = configparser.ConfigParser()

    if apiKey == "":
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'username': username}
    else:
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey, 'username': username}

    with open('airlines.ini', 'a') as configfile:
        configfile.write("\n\n")
        config.write(configfile)

    newAirWindow.quit()
    return

def terminateEditAirline(): ## Closes the edit airline screen
    global airline
    global name
    global url
    global apiKey
    global username
    global editAirWindow
    
    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames
    List = configLib.list

    name = name.get()
    url = url.get()
    apiKey = apiKey.get()
    username = username.get()
    airline = airline.get()

    a = List.index(airline)
    
    config = configparser.ConfigParser()

    if apiKey == "":
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'username': username}
    else:
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey, 'username': username}

    file = open('airlines.ini', 'r')
    data = file.read()
    file.close()

    data1 = data.split("[" + str(a+1) + "]")
    data2 = data1[1].split("[" + str(a+2) + "]")

    with open('airlines.ini', 'w') as configfile:
        configfile.write(data1[0])
        config.write(configfile)
        if not a+2 == len(List):
            configfile.write("[" + str(a+2) + "]")
            configfile.write(data2[1])
        configfile.close()

    editAirWindow.quit()
    return

def terminateDeleteAirline(): ## Closes the delete airline screen
    global airline
    global delAirWindow
    
    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames
    List = configLib.list

    airline = airline.get()

    a = List.index(airline)
    
    config = configparser.ConfigParser()

    no = """
    if apiKey == "":
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'username': username}
    else:
        if username == "":
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey}
        else:
            config[str(a+1)] = {'name': name, 'url': url, 'apikey': apiKey, 'username': username}
    """

    file = open('airlines.ini', 'r')
    data = file.read()
    file.close()

    print(str(a+1))
    data1 = data.split("[" + str(a) + "]")
    print(data1[0])
    try:
        data2 = data1[1].split("[" + str(a+1) + "]")
        print(data2[1])
    except Exception as e:
        print(e)
        data2 = ["", ""]

    with open('airlines.ini', 'w') as configfile:
        configfile.write(data1[0])
        #config.write(configfile)
        if not data2[1] == "":
            configfile.write("[" + str(a) + "]")
            configfile.write(data2[1])
        configfile.close()
        config.write(configfile)

    delAirWindow.quit()
    return

def new(): ## New airline screen
    global name
    global url
    global apiKey
    global newAirWindow
    global username

    newAirWindow = tk.Tk()
    newAirWindow.iconbitmap('Favicon.ico')
    name = tk.StringVar(newAirWindow)
    url = tk.StringVar(newAirWindow)
    apiKey = tk.StringVar(newAirWindow)
    username = tk.StringVar(newAirWindow)

    newAirWindow.title('xACARS ' + configLib.version)
    tk.Label(newAirWindow, text='Airline Name: ').grid(row=0, column=0)
    tk.Label(newAirWindow, text='Airline URL: ').grid(row=1, column=0)
    tk.Label(newAirWindow, text='Username: ').grid(row=2, column=0)
    tk.Label(newAirWindow, text='API Key (Only if you want use autofill): ').grid(row=3, column=0)
    ttk.Entry(newAirWindow, textvariable=name).grid(row=0, column=1)
    ttk.Entry(newAirWindow, textvariable=url).grid(row=1, column=1)
    ttk.Entry(newAirWindow, textvariable=username).grid(row=2, column=1)
    ttk.Entry(newAirWindow, show="*", textvariable=apiKey).grid(row=3, column=1)
    ttk.Button(newAirWindow, text='Create', command=terminateNewAirline).grid(row=4, columnspan=2, sticky='we')
    newAirWindow.mainloop()
    newAirWindow.destroy()

    configLib.reloadList()
    newAirWindow.quit()
    newAirWindow.destroy()
    reload()

def editAutofill(): ## Autofill for the edit airline screen
    global airline
    global name
    global url
    global apiKey
    global username

    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames
    List = configLib.list

    a = List.index(airline.get())
    name.set(List[a])
    url.set(websites[a])
    if not savedAPIKeys[a] == "None Saved":
        apiKey.set(savedAPIKeys[a])
    if not usernames[a] == "None Saved":
        username.set(usernames[a])

def delete(): ## Delete iarline screen
    global airline
    global name
    global url
    global apiKey
    global username
    global delAirWindow

    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames
    List = configLib.list

    delAirWindow = tk.Tk()
    delAirWindow.iconbitmap('Favicon.ico')
    airline = tk.StringVar(delAirWindow)

    delAirWindow.title('xACARS ' + configLib.version)
    tk.Label(delAirWindow, text='Airline to delete: ').grid(row=0, column=0)
    ttk.OptionMenu(delAirWindow, airline, *List).grid(row=0, column=1)
    ttk.Button(delAirWindow, text='Update', command=terminateDeleteAirline).grid(row=1, columnspan=2, sticky='we')
    delAirWindow.mainloop()
    delAirWindow.destroy()

    configLib.reloadList()
    delAirWindow.quit()
    delAirWindow.destroy()
    reload()

def edit(): ## Edit screen
    global airline
    global name
    global url
    global apiKey
    global username
    global editAirWindow

    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames
    List = configLib.list

    editAirWindow = tk.Tk()
    editAirWindow.iconbitmap('Favicon.ico')
    airline = tk.StringVar(editAirWindow)
    name = tk.StringVar(editAirWindow)
    url = tk.StringVar(editAirWindow)
    apiKey = tk.StringVar(editAirWindow)
    username = tk.StringVar(editAirWindow)

    editAirWindow.title('xACARS ' + configLib.version)
    tk.Label(editAirWindow, text='Airline to edit: ').grid(row=0, column=0)
    ttk.OptionMenu(editAirWindow, airline, *List).grid(row=0, column=1)
    tk.Label(editAirWindow, text='Airline Name: ').grid(row=1, column=0)
    tk.Label(editAirWindow, text='Airline URL: ').grid(row=2, column=0)
    tk.Label(editAirWindow, text='Username: ').grid(row=3, column=0)
    tk.Label(editAirWindow, text='API Key (Only if you want use autofill): ').grid(row=4, column=0)
    ttk.Entry(editAirWindow, textvariable=name, text=name).grid(row=1, column=1)
    ttk.Entry(editAirWindow, textvariable=url, text=url).grid(row=2, column=1)
    ttk.Entry(editAirWindow, textvariable=username, text=username).grid(row=3, column=1)
    ttk.Entry(editAirWindow, show="*", textvariable=apiKey, text=apiKey).grid(row=4, column=1)
    ttk.Button(editAirWindow, text='Update', command=terminateEditAirline).grid(row=5, column=0, sticky='we')
    ttk.Button(editAirWindow, text='Autofill', command=editAutofill).grid(row=5, column=1, sticky='we')
    editAirWindow.mainloop()
    editAirWindow.destroy()

    configLib.reloadList()
    editAirWindow.quit()
    editAirWindow.destroy()
    reload()

def quit(): ## Closes main menu
    global window
    window.quit()
    window.destroy()

def reload(): ## Draws main window
    global window
    window = tk.Tk()
    window.iconbitmap('Favicon.ico')

    configLib.reloadList()

    list = configLib.list
    websites = configLib.websites
    savedAPIKeys = configLib.savedAPIKeys
    usernames = configLib.usernames

    window.title('xACARS - Airlines')
    tk.Label(window, text='Airline Name').grid(row=0, column=0) 
    tk.Label(window, text='Airline URL').grid(row=0, column=1)
    tk.Label(window, text='Username').grid(row=0, column=2)
    tk.Label(window, text='APIKey (optional)').grid(row=0, column=3)
    ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=1, columnspan=4, sticky="we")

    a = 1
    for key in list:
        try:
            name = list[a]
            tk.Label(window, text=name).grid(row=a+3, column=0)
            tk.Label(window, text=websites[a]).grid(row=a+3, column=1)
            tk.Label(window, text=usernames[a]).grid(row=a+3, column=2)
            tk.Label(window, text=savedAPIKeys[a]).grid(row=a+3, column=3)
            a = a + 1
        except:
            pass

    ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=a+3, columnspan=4, sticky="we")
    ttk.Button(window, text='Finish', command=quit).grid(row=a+4, column=0, sticky="we")
    ttk.Button(window, text='Add Airline', command=new).grid(row=a+4, column=1, sticky="we")
    ttk.Button(window, text='Edit Airline', command=edit).grid(row=a+4, column=2, sticky="we")
    ttk.Button(window, text='Delete Airline', command=delete).grid(row=a+4, column=3, sticky="we")
    window.mainloop()