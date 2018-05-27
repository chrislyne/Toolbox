import maya.cmds as cmds
import maya.mel as mel
import os, sys, time
from stat import S_ISREG, ST_MTIME, ST_MODE
from pymel.all import *
import json

## global Variables ##
def globalVars():
    global ioWorkspace
    ioWorkspace = cmds.workspace( q=True, fullName=True )
    global userInitals
    userInitals = 'xx'
    
def incSave():
    import io_incrementalSave
    io_incrementalSave.IncrementCurrentFile(userInitals)

def ChangeProject(project):
    if project == 1:
        print 'Create New'
        mel.eval("projectWindow")
    if project == 2:
        print 'Add Existing'
        mel.eval("setProject \"\"")
    if project > 3:
        global recentProjects
        evalString = 'setProject "'+recentProjects[project-4]+'"'
        mel.eval(evalString)
        global ioWorkspace
        ioWorkspace = cmds.workspace( q=True, fullName=True )
        allFolders =  ListFolders(ioWorkspace+"/scenes/REF/")
        clearList("modelClass")
        cmds.menuItem(parent="modelClass",label="Create New")
        cmds.menuItem(parent="modelClass",divider=True)
        if allFolders:
            for file in allFolders:
               cmds.menuItem(parent="modelClass", label=file)
            cmds.optionMenu("modelClass", edit=True, sl=3)
            UpdateMenus()

## returns user pref path ##
def UserPrefPath():
    userMayaPath = mel.getenv("MAYA_APP_DIR")
    userMayaPrefsPath = userMayaPath+'/prefs'  
    userMayaPrefsFile = userMayaPrefsPath+'/IOUserPrefs.json'
    return userMayaPrefsFile

def LoadUserSettings(filename):
    if(os.path.exists(filename)):
        try:
            with open(filename) as data_file:
                data = json.load(data_file)

                inputString = (data["user"]["initals"])
                cmds.textField ("initailsInputText",e=True, text=inputString)
                global userInitals
                userInitals = inputString
                #cmds.tabLayout("tabs", edit=True, selectTab='settingsForm')
        except:
            cmds.error('could not parse '+filename+' try deleting it')
    else:
        print 'no file'
        cmds.tabLayout("tabs", edit=True, selectTab='settingsForm')

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

def OrderByModified(dirpath):

    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)
    
    # leave only regular files, insert creation date
    entries = ((stat[ST_MTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    
    recentFiles = []
    
    for cdate, path in sorted(entries):
        #print time.ctime(cdate), os.path.basename(path)
        recentFiles.append(os.path.basename(path))
    return recentFiles


def OpenModelFile():
    buttonState = cmds.button("modelBtn1", q=True, l=True)
    if(buttonState == "Open"):
        class2 = cmds.optionMenu( "modelClass", q=True, v=True)
        name = cmds.optionMenu( "modelName", q=True, v=True)
        fileName = cmds.textScrollList( "fileList", q=True, selectItem=True)
        if fileName:
            modelPath = ioWorkspace+'/scenes/REF/'+class2+'/'+name+'/'+fileName[0]
            if(os.path.isfile(modelPath)):
                cmds.file( new=True, force=True ) 
                cmds.file( modelPath, open=True )
                print "modelName"
            else:
                print (modelPath+' does not exist')
    else:
        #create new file
        class2 = cmds.textField( "modelClassInputText", q=True, text=True)
        name = cmds.textField( "modelNameInputText", q=True, text=True)
        newpath = ioWorkspace+'/scenes/REF/'+class2+'/'+name
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        cmds.file( rename=(newpath+'/'+name+'_v001_'+userInitals+'.mb') )
        cmds.file( force=True, type='mayaBinary', save=True )
    #reset menu state
    cmds.optionMenu( "modelClass", edit=True, vis=True)
    cmds.textField("modelClassInputText", edit=True, vis=False)
    cmds.optionMenu( "modelName", edit=True, vis=True)
    cmds.textField("modelNameInputText", edit=True, vis=False)
    cmds.button("modelBtn1", edit=True, l="Open")

def clearList(listName):
    menu = cmds.optionMenu(listName, q=True, itemListLong=True)
    if menu:
        for item in menu:
            cmds.deleteUI(item, menuItem=True)

def ListFolders(path):
    if(os.path.isdir(path)):
        dirs = []
        files = os.listdir( path )
        
        for aFile in files:
            if(os.path.isdir(path+'/'+aFile)): 
                dirs.append(aFile)
        return dirs

def printNewMenuItem( item ):
    #print item
    if(item == "Create New"):
        cmds.optionMenu( "modelClass", edit=True, vis=False)
        cmds.textField("modelClassInputText", edit=True, vis=True)
        cmds.optionMenu( "modelName", edit=True, vis=False)
        cmds.textField("modelNameInputText", edit=True, vis=True)
        cmds.button("modelBtn1", edit=True, l="New")
    else:
        cmds.textField("modelClassInputText", edit=True, text=item)

def PopulateNameMenu( item ):
    subFolders = ListFolders(ioWorkspace+"/scenes/REF/"+item)
    clearList("modelName")
    cmds.menuItem(parent="modelName",label="Create New")
    cmds.menuItem(parent="modelName",divider=True)
    if(subFolders):
        for file in subFolders:
            if (file[0] != '.') and (file != 'backup'):
                cmds.menuItem(parent="modelName",label=file)
        if(len(subFolders)>2):
            cmds.optionMenu("modelName", edit=True, sl=3)
            
    if(cmds.optionMenu("modelName", q=True, numberOfItems=True)>2):
        cmds.optionMenu("modelName", edit=True, sl=3)
        cmds.textField("modelNameInputText", edit=True, vis=False)
        cmds.optionMenu("modelName", edit=True, vis=True)
        cmds.button("modelBtn1", edit=True, l="Open")
    else:
        cmds.textField("modelNameInputText", edit=True, vis=True)
        cmds.optionMenu("modelName", edit=True, vis=False)
        cmds.button("modelBtn1", edit=True, l="New")
        
def changeModelName(item):
    if(item == "Create New"):
        cmds.optionMenu( "modelName", edit=True, vis=False)
        cmds.textField("modelNameInputText", edit=True, vis=True)
        cmds.button("modelBtn1", edit=True, l="New")
        cmds.textScrollList( "fileList", e=True, vis=False,)
    else:
        class2 = cmds.optionMenu( "modelClass", q=True, v=True)
        modelPath = ioWorkspace+'/scenes/REF/'+class2+'/'+item
        recentFiles = OrderByModified(modelPath)
        cmds.textScrollList( "fileList", e=True, vis=True,)
        if recentFiles:
            cmds.textScrollList( "fileList", e=True, removeAll=True, append=list(reversed(recentFiles)), selectIndexedItem=1)
        else: 
            cmds.textScrollList( "fileList", e=True, removeAll=True,)


def ReturnToOptionMenu(self,selfMenu, item):
    cmds.optionMenu( selfMenu, edit=True, vis=True)
    cmds.textField(self, edit=True, vis=False)
    cmds.menuItem(parent=selfMenu,label=item)
    cmds.optionMenu(selfMenu, edit=True, v=item)

def UpdateMenus():
    printNewMenuItem(cmds.optionMenu("modelClass",q=True,v=True ))
    PopulateNameMenu(cmds.optionMenu("modelClass",q=True,v=True ))
    changeModelName(cmds.optionMenu("modelName",q=True,v=True ))

def BackpackWindow():
    globalVars()
    mainLayout = cmds.columnLayout(columnAttach=('both', 5), rowSpacing=10, adj=1)
    outForm = cmds.formLayout()
    
    #project menu
    #projectText = cmds.text(label="Project")
    
    #global recentProjects
    #recentProjects = cmds.optionVar (q='RecentProjectsList')
    #recentProjects.reverse()
    #projectMenu = cmds.optionMenu("projectMenu", w=50, cc='ChangeProject(cmds.optionMenu("projectMenu", q=True, sl=True))')
    
    #recentProjects
    #cmds.menuItem(label="Create New")
    #cmds.menuItem(label="Add Existing")
    #cmds.menuItem(divider=True)
    #for project in recentProjects:
        #splitPath = project.split('/')
        #cmds.menuItem(label=splitPath[-2], ann=project)
    #cmds.optionMenu("projectMenu", edit=True, sl=4)
    #cmds.formLayout(outForm,  edit=True, 
                     #attachForm=[
                     #(projectText, 'left', 5),
                     #(projectText, 'top', 14),
                     #(projectMenu, 'top', 10),
                     #(projectMenu, 'right', 5)],
                     #attachControl=[
                     #(projectMenu, 'left', 10,projectText)
                     #]
                     #)
        
    cmds.setParent( '..' )
    
    #cmds.separator()
    form = cmds.formLayout()
    #tabs = cmds.tabLayout("tabs",innerMarginWidth=5, innerMarginHeight=5)
    #cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    modelingForm = cmds.formLayout()
    
    modelBtn1 = cmds.button("modelBtn1",l='Open',h=50,w=50,c='OpenModelFile()')
    
    typeText = cmds.text(label="Type")
    nameText = cmds.text(label="Name")
    
    #btn2 = cmds.button("btn2",l='Save',h=50,w=50,c='mel.eval("file -save;")')
    #btn3 = cmds.button("btn3",l='Increment',h=50,w=50,c='incSave()')
    #btn4 = cmds.button("btn4",l='Publish',h=50,w=50,c='mel.eval("source abc_publishModel;abc_publishModel;")')
    #cmds.formLayout(modelingForm,  edit=True, 
                     #attachForm=[
                     #(btn2, 'left', 10),
                     #(btn2, 'top', 10),
                     #(btn3, 'top', 10),
                     #(btn4, 'right', 10),
                     #(btn4, 'top', 10)],
                     #attachPosition=[
                     #(btn2, 'right',0,33),
                     #(btn3, 'left',0,33),
                     #(btn3, 'right',0,66),
                     #(btn4, 'left',0,66)
                     #],
                     #)
    

    #sep = cmds.separator(style='in')
    newHeading = cmds.text (label="Open / Create Asset", fn="boldLabelFont")
    #model class menu
    modelClass = cmds.optionMenu("modelClass", w=50,changeCommand='UpdateMenus()')
    cmds.menuItem(label="Create New")
    cmds.menuItem(divider=True)
    allFolders =  ListFolders(ioWorkspace+"/scenes/REF/")
    if allFolders:
        for file in allFolders:
           cmds.menuItem(label=file)
    modelClassInputText = cmds.textField ("modelClassInputText", w=50, vis=False, cc='ReturnToOptionMenu("modelClassInputText","modelClass",cmds.textField("modelClassInputText",q=True,tx=True ))')
    if(cmds.optionMenu(modelClass, q=True, numberOfItems=True)>2):
        cmds.optionMenu(modelClass, edit=True, sl=3)
    
    #model name menu
    modelName = cmds.optionMenu("modelName", w=50,changeCommand=changeModelName)
    cmds.menuItem(label="Create New")
    cmds.menuItem(divider=True)
    modelNameInputText = cmds.textField ("modelNameInputText",w=50, vis=False,cc='ReturnToOptionMenu("modelNameInputText","modelName",cmds.textField("modelNameInputText",q=True,tx=True ))')
    if(cmds.optionMenu(modelName, q=True, numberOfItems=True)>2):
        cmds.optionMenu(modelName, edit=True, sl=3)
    
    fileList = cmds.textScrollList("fileList", numberOfRows=1, allowMultiSelection=False,dcc='OpenModelFile()')
    
    
    
    
    cmds.formLayout( modelingForm, edit=True, 
                     attachForm=[
                     #(sep, 'top', 100),
                     #(sep, 'right', 10),
                     #(sep, 'left', 10),
                     (newHeading, 'left', 10),
                     (modelBtn1, 'left', 50),
                     (modelBtn1, 'right', 10),
                     (typeText, 'left', 10),
                     (nameText, 'left', 10),
                     
                     (modelClass, 'left', 50),
                     (modelClassInputText, 'left', 50),
                     (modelName, 'left', 50),
                     (modelNameInputText, 'left', 50),
                     (modelClass, 'right', 10),
                     (modelClassInputText, 'right', 10),
                     (modelName, 'right', 10),
                     (modelNameInputText, 'right', 10),
                     (fileList, 'right', 10),
                     (fileList, 'left', 50),
                     (newHeading, 'top', 10),
                     (typeText, 'top', 42),
                     (modelClass, 'top', 40),
                     (modelClassInputText, 'top', 40),
                     (modelName, 'top', 70),
                     (modelNameInputText, 'top', 70),
                        ],
                     attachControl=[
                     #(nameText, 'top', 15, typeText),
                     (fileList, 'top', 20, modelNameInputText),
                     (modelBtn1, 'top', 10, fileList)
                     ]
                     )
    cmds.setParent( '..' )
    
    
    #animationForm = cmds.rowColumnLayout(numberOfColumns=2)
    
    #cmds.setParent( '..' )
    
    #rendingForm = cmds.rowColumnLayout(numberOfColumns=2)
    
    #cmds.setParent( '..' )
    
    ## SETTINGS TAB ##
    #settingsForm = cmds.rowColumnLayout("settingsForm",numberOfColumns=2,columnSpacing=[(1,10),(2,10)],rowOffset=[(1,'top',20)])
    #initailsText = cmds.text(label="Initials")
    #initailsInputText = cmds.textField ("initailsInputText",w=126, cc=SaveUserSettings)
    
    #cmds.setParent( '..' )
    
    #cmds.tabLayout( tabs, edit=True, tabLabel=((modelingForm, 'Modeling'), (animationForm, 'Animation'), (rendingForm, 'Rendering'), (settingsForm, 'Settings')) )
    
    
    UpdateMenus()
    JSONPath = UserPrefPath()
    LoadUserSettings(JSONPath)

#import studiIO
#from studiIO import *
#StudioIOWindow()
def dockingIO():
    WorkspaceName = 'Backpack'
    if (cmds.workspaceControl('Backpack', exists=True)):
        cmds.deleteUI('Backpack')
    cmds.workspaceControl( WorkspaceName,initialHeight=500, uiScript = 'BackpackWindow()' )

dockingIO()