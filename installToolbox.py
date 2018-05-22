import maya.cmds as cmds
import sys
from pymel.all import *
import json
import os
import urllib2

def createShelf(shelfName):
    
    shelfExists = 0
    names = cmds.layout('ShelfLayout',q=True,ca=True)
    for name in names:
        if name == shelfName:
            shelfExists = 1
    
    if shelfExists == 1:
        print 'Shelf {} Exists'.format(shelfName)
    else:
        print 'Shelf {} does not exist'.format(shelfName)
        mel.addNewShelfTab(shelfName)

def RemoveButton(shelfName,iconName):
    shelfButtons = cmds.shelfLayout(shelfName,q=True,childArray=True)

    for btn in shelfButtons:
        label = ''

        #Assert that this is a shelfButton
        if cmds.objectTypeUI(btn,isType='shelfButton'):

            label = cmds.shelfButton(btn,q=True,image=True)

            #If this button has the label we're looking for,
            #delete the button.
            if iconName == label:
                cmds.deleteUI(btn)

def DownloadFile(remote, local):

    
    u = urllib2.urlopen(remote)
    h = u.info()
    totalSize = int(h["Content-Length"])
    
    print "Downloading %s bytes..." % totalSize,
    fp = open(local, 'wb')
    
    blockSize = 8192 #100000 # urllib.urlretrieve uses 8192
    count = 0
    while True:
        chunk = u.read(blockSize)
        if not chunk: break
        fp.write(chunk)
        count += 1
        if totalSize > 0:
            percent = int(count * blockSize * 100 / totalSize)
            if percent > 100: percent = 100
            print "%2d%%" % percent,
            if percent < 100:
                print "\b\b\b\b\b",  # Erase "NN% "
            else:
                print "Done."
    
    fp.flush()
    fp.close()
    if not totalSize:
        print

def AddIcons(shelfName):
    
    #check that shelf exists
    createShelf(shelfName)
    
    localScriptsPath = cmds.optionMenu('scriptsMenu', query=True,v=True) 
    localIconsPath = cmds.optionMenu('iconsMenu', query=True,v=True) 
    scriptsMenuI = cmds.optionMenu('scriptsMenu', query=True,sl=True)
    
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
            DownloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/icons/'+icon), (localIconsPath+'/'+icon))
            shelfString += ',i1=\''+icon+'\''
            
        except:
            print ('file not available')
        #download script from github
        if scriptsMenuI > 1:
            try:
                script = buttons[i]['script']
                fileName = script.split('/')
                DownloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/'+script),(localScriptsPath+'/'+fileName[-1]))
            except:
                print ('file not available')
        #download modules from github
        if scriptsMenuI > 1:
            try:
                modules = buttons[i]['modules']
                for mod in modules:
                    fileName = mod.split('/')
                    #make folder
                    if not os.path.exists(localScriptsPath+'/Modules'):
                        os.makedirs(localScriptsPath+'/Modules')
                    DownloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/'+mod),(localScriptsPath+'/Modules/'+fileName[-1]))
            except:
                print ('file not available')
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
        
        #remove old button
        RemoveButton(shelfName,icon)

        #add icons to shelf
        currentButton = eval (shelfString)
        
        try:
            mi = buttons[i]['menuItem']
            for i,l in enumerate(mi):
                cmds.shelfButton(currentButton,edit=True,mi=(mi[i]['label'],mi[i]['command']))
        except:
            print ''
    
    
    
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