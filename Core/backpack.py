import maya.cmds as cmds
import maya.mel as mel
import os, sys, time
from stat import S_ISREG, ST_MTIME, ST_MODE
from pymel.all import *
import json

## global Variables ##
def globalVars():
    global ioWorkspace
    ioWorkspace = 'C:/Users/Chris/Dropbox/Projects/Backpack' 

def exportFile():
    #selected objects
    objects = cmds.ls(sl=True)
    #check objects are selected
    if len(objects)>0:

        #create new file
        class2 = cmds.textField( "modelClassInputText", q=True, text=True)
        name = cmds.textField( "modelNameInputText", q=True, text=True)
        newpath = ioWorkspace+'/'+class2
        #create folder
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        #do export
        exportCommand = 'AbcExport -j "-frameRange 1 1 -stripNamespaces -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa '
        for obj in objects:
            exportCommand += '-root '+obj+' '
        exportCommand += '-file '+newpath+'/'+name+'.abc"'
        mel.eval(exportCommand)
        #reset menu state
        cmds.optionMenu( "modelClass", edit=True, vis=True)
        cmds.textField("modelClassInputText", edit=True, vis=False)
    #handle errors
    else:
        cmds.error('You must select an object to export')

def ListFolders(path):
    if(os.path.isdir(path)):
        dirs = []
        files = os.listdir( path )
        
        for aFile in files:
            if(os.path.isdir(path+'/'+aFile)): 
                dirs.append(aFile)
        return dirs

def printNewMenuItem( item ):
    if(item == "Create New"):
        cmds.optionMenu( "modelClass", edit=True, vis=False)
        cmds.textField("modelClassInputText", edit=True, vis=True)
        cmds.textField("modelNameInputText", edit=True, vis=True)
    else:
        cmds.textField("modelClassInputText", edit=True, text=item)


def ReturnToOptionMenu(self,selfMenu, item):
    cmds.optionMenu( selfMenu, edit=True, vis=True)
    cmds.textField(self, edit=True, vis=False)
    cmds.menuItem(parent=selfMenu,label=item)
    cmds.optionMenu(selfMenu, edit=True, v=item)

def UpdateMenus():
    printNewMenuItem(cmds.optionMenu("modelClass",q=True,v=True ))

def BackpackWindow():
    globalVars()
    mainLayout = cmds.columnLayout(columnAttach=('both', 5), rowSpacing=10, adj=1)
    outForm = cmds.formLayout()
        
    cmds.setParent( '..' )

    form = cmds.formLayout()
    
    modelingForm = cmds.formLayout()
    
    modelBtn1 = cmds.button("modelBtn1",l='Pocket',h=50,w=200,c='exportFile()')
    
    typeText = cmds.text(label="Type")
    nameText = cmds.text(label="Name")

    #model class menu
    modelClass = cmds.optionMenu("modelClass", w=50,changeCommand='UpdateMenus()')
    cmds.menuItem(label="Create New")
    cmds.menuItem(divider=True)
    allFolders =  ListFolders(ioWorkspace+"/")
    if allFolders:
        for file in allFolders:
           cmds.menuItem(label=file)
    modelClassInputText = cmds.textField ("modelClassInputText", w=50, vis=False, cc='ReturnToOptionMenu("modelClassInputText","modelClass",cmds.textField("modelClassInputText",q=True,tx=True ))')
    if(cmds.optionMenu(modelClass, q=True, numberOfItems=True)>2):
        cmds.optionMenu(modelClass, edit=True, sl=3)
    
    #model name menu
    cmds.menuItem(label="Create New")
    cmds.menuItem(divider=True)
    modelNameInputText = cmds.textField ("modelNameInputText",w=50)

    
    cmds.formLayout( modelingForm, edit=True, 
                     attachForm=[
                     (modelBtn1, 'left', 50),
                     (modelBtn1, 'right', 10),
                     (typeText, 'left', 10),
                     (nameText, 'left', 10),
                     
                     (modelClass, 'left', 50),
                     (modelClassInputText, 'left', 50),
                     (modelNameInputText, 'left', 50),
                     (modelClass, 'right', 10),
                     (modelClassInputText, 'right', 10),
                     (modelNameInputText, 'right', 10),
                     (typeText, 'top', 42),
                     (modelClass, 'top', 40),
                     (modelClassInputText, 'top', 40),
                     (modelNameInputText, 'top', 70),
                     (nameText, 'top', 72),
                        ],
                     attachControl=[
                     (modelBtn1, 'top', 30, modelNameInputText)
                     ]
                     )
    cmds.setParent( '..' )
    
    UpdateMenus()

#import studiIO
#from studiIO import *
#StudioIOWindow()
def dockingBackpack():
    WorkspaceName = 'Backpack'
    if (cmds.workspaceControl('Backpack', exists=True)):
        cmds.deleteUI('Backpack')
    cmds.workspaceControl( WorkspaceName,initialHeight=500,initialWidth=320, uiScript = 'BackpackWindow()' )

dockingBackpack()