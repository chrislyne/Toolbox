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
        user_install()
    return initials

###        UI        ###

def inputText():
    initals = cmds.textField('nameText',q=True,text=True)
    return initals

def userIDWindow():
    installForm = cmds.formLayout()
    textMessage = cmds.text(label='Hey, it\'s been over a week are these still your initials?')
    textLabel = cmds.text(label='Initials')
    nameText = cmds.textField('nameText',width=250)
    
     
    btn1 = cmds.button(height=50,label='Update',c='updateUserPrefs(inputText());cmds.deleteUI(\'User ID\')')
    btn2 = cmds.button(height=50,label='Close',c='cmds.deleteUI(\'User ID\')')
    
    cmds.formLayout(installForm,  edit=True, 
                     attachForm=[
                     (textMessage, 'top', 15),
                     (textMessage, 'left', 10),
                     (textLabel, 'top', 45),
                     (textLabel, 'left', 10),
                     (nameText, 'top', 40),
                     (nameText, 'right', 10),
                     (btn1, 'bottom', 0),
                     (btn1, 'left', 0),
                     (btn2, 'bottom', 0),
                     (btn2, 'right', 0)
                     ],
                     attachControl=[
                     (nameText, 'left', 10,textLabel),
                     (btn2, 'left', 0,btn1)
                     ],
                     attachPosition=[
                     (btn1, 'right', 0, 50)
                     ]
                     )
    #set initals from user config                 
    #cmds.textField(nameText,edit=True,tx=initials)

def user_install():
    workspaceName = 'User ID'
    if(cmds.workspaceControl('User ID', exists=True)):
        cmds.deleteUI('User ID')
    cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'userIDWindow()')

        
        
#print getUserPrefs()    