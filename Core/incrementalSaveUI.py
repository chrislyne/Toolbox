import os
import time
import maya.mel as mel
import maya.cmds as cmds
from pymel.all import *

def importModules(fileName):
    import imp
    try:
        dirname = os.path.dirname(__file__)
        #parentDir = dirname
    except:
        print 'running in test environment'
        dirname = 'C:/Users/Chris/Dropbox/Projects/Toolbox'
        #parentDir = os.path.abspath(os.path.join(dirname, os.pardir))
    
    fileName = imp.load_source(fileName, (dirname+'/Modules/'+fileName+'.py'))
    #IOuserPref = imp.load_source('IOuserPref', (dirname+'/Modules/IOuserPref.py'))
    return fileName

def updateUserPrefs(initials):
    IOuserPref = importModules('IOuserPref')
    userConfigFile = IOuserPref.UserPrefPath()
    
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
            IOuserPref.SaveUserSettings(initials)
    else:
        print 'it is not there'
        #create file
        IOuserPref.SaveUserSettings(initials)

def inputText():
    initals = cmds.textField('nameText',q=True,text=True)
    return initals

def userIDWindow(initials):
    installForm = cmds.formLayout()
    textMessage = cmds.text(label='Hey, it\'s been over a week are these still your initials?')
    textLabel = cmds.text(label='Initials')
    nameText = cmds.textField('nameText',width=250,tx='Custom')
    
     
    btn1 = cmds.button(height=50,label='Update',c='updateUserPrefs(inputText());incrementalSaveUI();cmds.deleteUI(\'User ID\')')
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
    cmds.textField(nameText,edit=True,tx=initials)

def user_install(initials):
    workspaceName = 'User ID'
    if(cmds.workspaceControl('User ID', exists=True)):
        cmds.deleteUI('User ID')
    cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'userIDWindow(\''+initials+'\')')
#user_install()

def incrementalSaveUI():
    IOuserPref = importModules('IOuserPref')
    incrementalSave = importModules('incrementalSave')
    userConfigFile = IOuserPref.UserPrefPath()
    initials = ''
    fileExists = os.path.isfile(userConfigFile)
    if fileExists:
        initials = IOuserPref.LoadUserSettings(userConfigFile)
        #file m time
        f1 = os.path.getmtime(userConfigFile)
        #current time
        t = time.time()
        #get difference
        timePassed = t - f1
        timePassedHours = timePassed / 3600
        #update file if too old
        if timePassedHours > 168:
            user_install(initials)
        else:
            incrementalSave.IncrementCurrentFile(initials=initials)
    else:
        print 'it is not there'
        #create file
        user_install(initials)
        
#incrementalSaveUI()    