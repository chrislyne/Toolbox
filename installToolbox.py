import maya.cmds as cmds
import sys
from pymel.all import *
import json
import os
import urllib

def AddIcons(shelfName):
    
    iconsMenu = cmds.optionMenu('iconsMenu', query=True,v=True) 
    
    #read json
    try:
        dirname = os.path.dirname(__file__)
    except:
        print 'running in test environment'
        dirname = 'C:/Users/Chris/Dropbox/Projects/Toolbox'

    JSONPath = dirname+'/toolboxShelf.json'
    with open(JSONPath) as data_file:    
        data = json.load(data_file)
        
    buttons = (data['icons'])
    for i, btn in enumerate(buttons):
        shelfElements = buttons[i]
        shelfString = 'cmds.shelfButton(rpt=True'
        #download icons from github
        try:
            icon = buttons[i]['icon']
            testfile = urllib.URLopener()
            testfile.retrieve(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/icons/'+icon), (iconsMenu+'/'+icon))
            shelfString += ',i1=\''+icon+'\''
            
        except:
            print ('file '+icon+' not available')
        try:
            label = buttons[i]['label']
            shelfString += ',l=\''+label+'\''
        except:
            label = ''
        try:
            com = buttons[i]['command']
            shelfString += ',c=\''+com+'\''
        except:
            com = ''
        try:
            stp = buttons[i]['stp']
            shelfString += ',stp=\''+stp+'\''
        except:
            shelfString += ',stp=\'mel\''
        
        shelfString += ',w=32,h=32,p=\''+shelfName+'\')'
        
        #add icons to shelf
        currentButton = eval (shelfString)
        
        try:
            mi = buttons[i]['menuItem']
            for i,l in enumerate(mi):
                cmds.shelfButton(currentButton,edit=True,mi=(mi[i]['label'],mi[i]['command']))
        except:
            print 'no menu item'
            

    
def CheckText():

   shelfName = cmds.textField('nameText',q=True,text=True)
   AddIcons(shelfName)

def FilterOutSystemPaths(path):
    systemPath  = 0
    allparts = path.split('/')
    for part in allparts:
        if part == 'ProgramData' or  part == 'Program Files':
            systemPath = 1
    
    return systemPath


def installToolboxWindow():
    installForm = cmds.formLayout()
    textLabel = cmds.text(label='Shelf')
    nameText = cmds.textField('nameText',width=250,tx='Custom')
    scriptsMenu = cmds.optionMenu('scriptsMenu')
    separator = ';'
    scriptsPaths = mel.getenv('MAYA_SCRIPT_PATH')
    allparts = scriptsPaths.split(separator)
    for i, part in enumerate(allparts):
        if (i==0):
            cmds.menuItem( label='Manually install scripts' )
        if (i<7):
            isSystemPath = FilterOutSystemPaths(part)
            if (isSystemPath == 0):
                cmds.menuItem( label=part )
            
    iconsMenu = cmds.optionMenu('iconsMenu')  
    iconsPaths = mel.getenv('XBMLANGPATH')
    iconsParts = iconsPaths.split(separator)
    
    for i, part in enumerate(iconsParts):
        if (i<6):
            isSystemPath = FilterOutSystemPaths(part)
            if (isSystemPath == 0):
                cmds.menuItem( label=part )
     
    btn1 = cmds.button(height=50,label='Install',c='CheckText()')
    btn2 = cmds.button(height=50,label='Close',c='cmds.deleteUI(\'Install Toolbox\')')
    
    cmds.formLayout(installForm,  edit=True, 
                     attachForm=[
                     (textLabel, 'top', 15),
                     (textLabel, 'left', 10),
                     (nameText, 'top', 10),
                     (nameText, 'right', 10),
                     (scriptsMenu, 'right', 10),
                     (iconsMenu, 'right', 10),
                     (btn1, 'bottom', 0),
                     (btn1, 'left', 0),
                     (btn2, 'bottom', 0),
                     (btn2, 'right', 0)
                     ],
                     attachControl=[
                     (nameText, 'left', 10,textLabel),
                     (scriptsMenu, 'top', 10,textLabel),
                     (scriptsMenu, 'left', 10,textLabel),
                     (iconsMenu, 'top', 10,scriptsMenu),
                     (iconsMenu, 'left', 10,textLabel),
                     (btn2, 'left', 0,btn1)
                     ],
                     attachPosition=[
                     (btn1, 'right', 0, 50)
                     ]
                     )
                     
    shelfName = ''
    #get current tab
    names = cmds.layout('ShelfLayout',q=True,ca=True)
    shelfIndex = cmds.shelfTabLayout('ShelfLayout', query=True, selectTabIndex=True)
    
    #set text
    selectionString = (names[shelfIndex-1])
    cmds.textField(nameText,edit=True,tx=selectionString)


def toolbox_install():
    workspaceName = 'Install Toolbox'
    if(cmds.workspaceControl('Install Toolbox', exists=True)):
        cmds.deleteUI('Install Toolbox')
    cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'installToolboxWindow()')


#toolbox_install()

#import installToolbox
#installToolbox.toolbox_install()