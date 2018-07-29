import os
import time
import maya.mel as mel
import maya.cmds as cmds
from pymel.all import *
import json


#load user settings from disk
def LoadUserSettings(filename,property):
    initials = ''
    if(os.path.exists(filename)):
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
                inputString = (data[property[0]][property[1]])
                initials = inputString
        except:
            cmds.error('could not parse '+filename+' try deleting it')
    else:
        print 'no file'

    return initials
    
#save user settings
def SaveUserSettings(item):
    global userInitals
    userInitals = item
    userMayaPath = mel.getenv("MAYA_APP_DIR")
    userMayaPrefsPath = userMayaPath+'/prefs'
    if not os.path.exists(userMayaPrefsPath):
        os.makedirs(userMayaPrefsPath)
    
    userMayaPrefsFile = userMayaPrefsPath+'/IOUserPrefs.json'
    
    jsonText = '{\n    \"user\": {\n        \"initals\": \"'+item+'\"\n    }\n}'
    
    text_file = open(userMayaPrefsFile, "w")
    text_file.write(jsonText)
    text_file.close()   

#define where the pref file is
def UserPrefPath():
    userMayaPath = mel.getenv("MAYA_APP_DIR")
    userMayaPrefsPath = userMayaPath+'/prefs'  
    userMayaPrefsFile = userMayaPrefsPath+'/IOUserPrefs.json'
    return userMayaPrefsFile

def updateUserPrefs(initials):
    userConfigFile = UserPrefPath()
    
    fileExists = os.path.isfile(userConfigFile)
    if fileExists:
        #file m time
        f1 = os.path.getmtime(userConfigFile)
        #current time
        t = time.time()
        #get difference
        timePassed = t - f1
        timePassedHours = timePassed / 3600
        #update file if too old
        if timePassedHours > 0.1:
            SaveUserSettings(initials)
    else:
        print 'it is not there'
        #create file
        SaveUserSettings(initials)


def getUserPrefs():
    prefFile = UserPrefPath()
    initials = LoadUserSettings(prefFile,['user','initals'])
    if not initials:
        while True:
            initials = userInput()
            if initials:
                updateUserPrefs(initials)
                break
    return initials

###        UI        ###

def userInput():
    result = cmds.promptDialog(
                    title='User Prefs Input',
                    message='Enter Initials:',
                    button=['Update', 'Cancel'],
                    defaultButton='Update',
                    cancelButton='Cancel',
                    dismissString='Cancel')
    
    if result == 'Update':
        text = cmds.promptDialog(query=True, text=True)
        return text
       
#from LlamaIO import UserPrefs 
#from LlamaIO.UserPrefs import *       
#print getUserPrefs()    