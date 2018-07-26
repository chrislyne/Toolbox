import maya.cmds as cmds
import os

###    UTILITIES    ###

#add attribue
def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')
    
###        EXPORTS        ###

#publish camera
def publishCamera(abcFilename,cameraName):
    #get workspace
    workspace = cmds.workspace( q=True, directory=True, rd=True)
    workspaceLen = len(workspace.split('/'))
    #get filename
    filename = cmds.file(q=True,sn=True)
    #get relative path (from scenes)
    relativePath = ''
    for dir in filename.split('/')[8:-1]:
        relativePath += '%s/'%(dir)
    
    #get scene settings
    startFrame = int(cmds.playbackOptions(q=True,minTime=True))
    endFrame = int(cmds.playbackOptions(q=True,maxTime=True))
    camWidth = cmds.getAttr('defaultResolution.width')
    camHeight = cmds.getAttr('defaultResolution.height')
    frameRate = cmds.currentUnit(q=True,time=True)
    
    #add settings to camera
    addAttribute(cameraName,'startFrame',startFrame)
    addAttribute(cameraName,'endFrame',endFrame)
    addAttribute(cameraName,'camWidth',camWidth)
    addAttribute(cameraName,'camHeight',camHeight)
    addAttribute(cameraName,'frameRate',frameRate)
    
    #published file name    
    exportString = ' -root %s'%(cameraName)
    
    folderPath = '%scache/alembic/%s'%(workspace,relativePath)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    
    #check if plugin is already loaded
    if not cmds.pluginInfo('AbcImport',query=True,loaded=True):
        try:
            #load abcExport plugin
            cmds.loadPlugin( 'AbcImport' )
        except: 
            cmds.error('Could not load AbcImport plugin')

    #export .abc
    additionalAttr = ''
    #IO attributes
    additionalAttributes = ['width','height','startFrame','endFrame','frameRate']
    for attr in additionalAttributes:
        additionalAttr += ' -attr %s'%(attr)
    command = '-frameRange %d %d%s -ro -stripNamespaces -worldSpace -dataFormat ogawa%s -file %scache/alembic/%s%s.abc'%(startFrame,endFrame,additionalAttr,exportString,workspace,relativePath,abcFilename)
    #write to disk
    cmds.AbcExport ( j=command )
    return '%scache/alembic/%s%s.abc'%(workspace,relativePath,abcFilename)

#rename camera 
def renameCamera(selectionCamera):
    #get range
    startFrame = int(cmds.playbackOptions(q=True,minTime=True))
    endFrame = int(cmds.playbackOptions(q=True,maxTime=True))

    #get filename
    filename = cmds.file(q=True,sn=True,shn=True)
    
    shotName = filename.split('_')[0]
    
    newName = cmds.rename(selectionCamera,'%s_s%s_e%s'%(shotName,startFrame,endFrame))
    return newName

#list cameras
def listAllCameras():
    listAllCameras = cmds.listCameras(p=True)
    #remove 'persp' camera
    if 'persp' in listAllCameras: listAllCameras.remove('persp')
    return listAllCameras

#create file name for export camera
def makeCameraName():
    filename = cmds.file(q=True,sn=True,shn=True).split('.')[0]
    camFileName = filename+'_CAMERA'
    return camFileName

#assume and run
def runSilent():
    publishName = makeCameraName()
    allCameras = listAllCameras()
    fileName = ''
    if allCameras:
        #make sure there is only one camera, else run UI
        if len(allCameras) > 1:
            io_exportCamera(0)        
        else:
            newCamName = renameCamera(allCameras[0])
            fileName = publishCamera(publishName,newCamName)
    else:
        cmds.error( 'no valid camera in scene')
    return fileName
   
#update name and run
def runWithUI():
    publishName = cmds.textField('nameText',q=True,text=True)
    selectionCamera = cmds.optionMenu('cameraSelection',q=True,v=True)
    #check if a camera is selected and run
    if selectionCamera != '':
        newCamName = renameCamera(selectionCamera)
        publishCamera(publishName,newCamName)
    else:
        cmds.error( 'no valid camera in scene')


###        UI        ###

def io_exportCamera_window():

    exportForm = cmds.formLayout()
    textLabel = cmds.text('textLabel',label='Publish Name')
    nameText = cmds.textField('nameText',w=250)
    cameraLabel = cmds.text('cameraLabel',label='Camera')
    
    allCameras = listAllCameras()
    cameraSelection = cmds.optionMenu('cameraSelection')
    for cam in allCameras:
        cmds.menuItem(l=cam)
    
    Button1 = cmds.button('Button1',l='Publish',h=50,c='runWithUI()')
    Button2 = cmds.button('Button2',l='Close',h=50,c='cmds.deleteUI(\'Publish Camera\')') 
             
    cmds.formLayout(
        exportForm,
        edit=True,
        attachForm=[
        (textLabel,'top',15),
        (textLabel,'left',10),
        (nameText,'top',10),
        (nameText,'right',10),
        (cameraLabel,'left',10),
        (cameraSelection,'right',10),
        (Button1,'bottom',0),
        (Button1,'left',0),
        (Button2,'bottom',0),
        (Button2,'right',0)
        ],
        attachControl=[
        (nameText,'left',10,textLabel),
        (cameraLabel,'top',20,textLabel),
        (cameraSelection,'top',20,textLabel),
        (cameraSelection,'left',40,cameraLabel),
        (Button2,'left',0,Button1)
        ],
        attachPosition=[
        (Button1,'right',0,50)
        ])

    exportForm
    
    #get filename
    filename = makeCameraName()
    cmds.textField('nameText',edit=True,tx=filename)

def io_exportCamera(silent):
    if silent == 1:
        return runSilent()
    else:
        workspaceName = 'Publish Camera'
        if(cmds.workspaceControl(workspaceName, exists=True)):
            cmds.deleteUI(workspaceName)
        cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'io_exportCamera_window()')

#print io_exportCamera(1) 