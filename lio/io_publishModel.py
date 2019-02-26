import maya.cmds as cmds
import maya.mel as mel
import os, sys, time
from shutil import copyfile
import platform
from LlamaIO import addAttribute

###    UTILITIES    ###

#write to shader database
def WriteToDB(filename,log,mode):
    scenePath = os.path.split(os.path.abspath(filename))
    folderPath = scenePath[0]+'/'
    fileName = scenePath[1].split('.')[0]
    logFileName = folderPath+fileName+'.json'
    text_file = open(logFileName, mode)
    text_file.write(log)
    text_file.close()

#disconnects the rig from the shading network for a clean shader export
def disconnectRig():
    connections = []
    ctrlObjects = []
    additionalAttributes = []
    nodeTypes = ['file','place2dTexture','animCurveUU','expression','noise','projection','lambert']
    for nType in nodeTypes:
        nodes = cmds.ls(typ=nType)
        for node in nodes:
            
            #not sure what this is, maybe some kind of garbagy error check
            if(node != "<done>"):
                connectedNodes = cmds.listConnections(node,t='transform',plugs=True,c=True,d=False,s=True)
                if connectedNodes:                   
                    #disconnect the nodes
                    inputs = connectedNodes[0::2]
                    outputs = connectedNodes[1::2]
                    for i,item in enumerate(outputs):
                        outputLong = cmds.ls(outputs[i].split('.')[0],l=True)[0]
                        outputLong = '%s.%s'%(outputLong,outputs[i].split('.')[1])
                        c = [outputLong,inputs[i]]
                        cmds.disconnectAttr (c[0],c[1])
                        connections.append(c)
                        ctrlObjects.append(c[0].split('.')[0])
    
    #list connections and add them to controller              
    ctrlObjects = set(ctrlObjects) 
    for ctrlObj in ctrlObjects:
        objConnections = ''
        for connection in connections:
            if connection[0].split('.')[0] == ctrlObj:
                #ctrlObj = cmds.ls(ctrlObj,l=True)
                objConnections += ('%s,%s;'%(connection[0],connection[1]))
        #convert to long path 
        #ctrlObj = cmds.ls(ctrlObj,l=True)[0]
        print ctrlObj
        addAttribute(ctrlObj,'connections',objConnections)
    #return controllers that affect shading networks
    return(ctrlObjects)

#reconnect the rig to the shading network
def reconnectRig(controls):
    for c in controls:
        #read connections from controler
        connections = cmds.getAttr('%s.connections'%(c)).split(';')
        #make connections
        for connection in connections:
            try:
                cmds.connectAttr(connection.split(',')[0],connection.split(',')[1])
            except:
                pass

###     EXPORTS     ###

#export mb
def makeRef(refName,publishString):
    #define full file name
    refFileName  = refName+'.mb'
    #set outliner colour
    cmds.setAttr ('%s.useOutlinerColor'%(publishString),1)
    cmds.setAttr ('%s.outlinerColorR'%(publishString),0.25)
    cmds.setAttr ('%s.outlinerColorG'%(publishString),0.8)
    cmds.setAttr ('%s.outlinerColorB'%(publishString),0.25)
    #refresh outliner
    mel.eval("AEdagNodeCommonRefreshOutliners();")
    #add attribute to node for re-publishing
    addAttribute(publishString,'publishName',refName)
    
    #get parent folder
    scenePath = cmds.file(q=True,sn=True)
    parentFolder = scenePath.rsplit('/',2)[0]
    currentFolder = scenePath.rsplit('/',2)[1]
    
    #output name
    pathName = parentFolder+'/'+refFileName
    backupName = ""
    
    #if file exists, increment and back it up
    if os.path.isfile(pathName):
        #make backup folder
        backupFolder = '%s/%s/backup'%(parentFolder,currentFolder)
        if not os.path.exists(backupFolder):
            os.makedirs(backupFolder)
        count = 1
        backupExists = os.path.isfile('%s/%s%d'%(backupFolder,refFileName,count))
        while (backupExists == 1):
            count += 1
            backupExists = os.path.isfile('%s/%s%d'%(backupFolder,refFileName,count))
        backupName = '%s/%s%d'%(backupFolder,refFileName,count)
        copyfile(pathName, backupName)
    #export .mb REF
    cmds.file(pathName,force=True,type='mayaBinary',pr=True,es=True)
    #log
    logOutput = []
    logOutput.append(pathName)
    logOutput.append(scenePath)
    logOutput.append(backupName)
    
    return logOutput

#export alembic
def makeAlembic(refName, publishString):
    try: 
        #check if plug is already loaded
        if not cmds.pluginInfo('AbcExport',query=True,loaded=True):
            try:
                #load abcExport plugin
                cmds.loadPlugin( 'AbcExport' )
            except: cmds.error('Could not load AbcExport plugin')
        #make folder
        modelFolder = '%scache/alembic/models'%(cmds.workspace(q=True,rd=True))
        if not os.path.exists(modelFolder):
            os.makedirs(modelFolder)
        #export .abc
        additionalAttr = ''
        #IO attributes
        additionalAttributes = ['alembicName','IOID']
        #redshift attributes
        additionalAttributes += ['rsObjectId','rsEnableSubdivision','rsMaxTessellationSubdivs','rsDoSmoothSubdivision','rsMinTessellationLength','rsOutOfFrustumTessellationFactor','rsEnableDisplacement','rsMaxDisplacement','rsDisplacementScale']
        for attr in additionalAttributes:
            additionalAttr += ' -attr %s'%(attr)
        command = '-frameRange 1 1%s -stripNamespaces -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa -root %s -file models/%s.abc'%(additionalAttr,publishString,refName)
        cmds.AbcExport ( j=command )
        return '%s/%s.abc'%(modelFolder,refName)
    except:
        return 'unable to export .abc'

def sortFaceShadingGroups(shape,shadingGrp):
    #find transform
    transform = cmds.listRelatives(shape,p=True,type='transform')
    #list all objects in set
    allObjects = cmds.sets( shadingGrp, q=True )
    
    faces = []
    #search set for matching shapes 
    for obj in allObjects:
        splitObj = obj.split('.')
        if len(splitObj) > 1:
            if splitObj[0] == transform[0]:
                faces.append(splitObj[1])
    #return faces assign to material
    return faces


#publish shaders
def exportShaders(publishName,scenePath):
    
    #get workspace
    workspace = cmds.workspace(q=True,fullName=True)

    #initalise variables 
    allGeo = ""
    allMaterials = []
    data = '{\n    "shapes":['
    
    #select hierarchy
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True )
    allDecendingShapes = cmds.ls(allDecending,s=True,l=True)

    #make folder
    shaderFolder = '%s/renderData/alembicShaders/%s'%(workspace,publishName)
    if not os.path.exists(shaderFolder):
        os.makedirs(shaderFolder)

    
    #loop though if they have materials
    for i,shape in enumerate(allDecendingShapes):
        shadingGroups = cmds.listConnections(shape,type='shadingEngine')

        #change mesh preview to render time smooth
        try:
            renderTimeOn = cmds.getAttr('%s.rsEnableSubdivision'%shape)
            previewOn = cmds.getAttr('%s.displaySmoothMesh'%shape)
            #turn display smooth off 
            cmds.setAttr('%s.displaySmoothMesh'%shape,0)
            #add redshift smooth
            if previewOn != 0 and renderTimeOn == 0:
                cmds.setAttr('%s.rsEnableSubdivision'%shape,1)
                cmds.setAttr('%s.rsMaxTessellationSubdivs'%shape,2)
        except:
            pass

        if shadingGroups:
            allGeo += '-root %s '%(shape)
            allMaterials += shadingGroups
            #remove duplicates from list
            shadingGroups = list(set(shadingGroups))
            
            #add attributes to shape nodes
            addAttribute(shape,'alembicName',publishName)
            addAttribute(shape,'material',shadingGroups)
            ID = cmds.ls(shape,uuid=True)
            addAttribute(shape,'IOID',ID[0])
            
            shadingGrpsString = ''
            #garbagy json formattring
            for n,shadingGrp in enumerate(shadingGroups):
                faces = ''
                allFaces = sortFaceShadingGroups(shape,shadingGrp)
                for c,f in enumerate(allFaces):
                    if c > 0:
                        faces += '","'
                    faces += '.%s'%(f)
                if n > 0:
                    shadingGrpsString += ',\n               '
                shadingGrpsString +=  '\n            {"%s":["%s"]}'%(shadingGrp,faces)
            if i > 0:
                data += ','
            data += '\n        {\n        "IOID": "%s",\n        "materials": [%s\n        ]\n        }'%(ID[0],shadingGrpsString)
            #data += '\n     {\n     "%s":\n         {\n         "material": [\n             %s\n            ]\n         }\n     }'%(ID[0],shadingGrpsString)
    data += '\n ]\n}'  
    #write connections out to text file    
    WriteToDB('%s/renderData/alembicShaders/%s/%s/'%(workspace,publishName,publishName),data,'w')
    #materials used in our hierachy    
    allMaterials = list(set(allMaterials))  
    
    #log
    shaderCount = 0
    
    for material in allMaterials:
        #process namespaces
        materialFilename = material.replace(':', '_')
        #export material
        cmds.select(material,r=True,noExpand=True)  
        cmds.file('%s/renderData/alembicShaders/%s/%s_%s.mb'%(workspace,publishName,publishName,materialFilename),force=True,typ='mayaBinary',pr=True,es=True)
        
        #increment to log
        shaderCount += 1

    return shaderCount

#update name and run
def PublishModelCheckText():
    
    #init log variables
    numberOfFiles = 0
    numberOfMultiShaders = 0
    alembicExported = 0
    
    #list objects
    sel = cmds.ls(sl=True)
    if len(sel) == 1:
        #get publish name from textfield
        publishName = cmds.textField('nameText',q=True,text=True)
        #get current selection so that it can be re-selected at the end
        tempSelect = cmds.ls(sl=True)
       
        #check UI
        doShaders = cmds.checkBox('shadersCheck',q=True,v=True)
        doAlembic = cmds.checkBox('alembicCheck',q=True,v=True)
        doBinary = cmds.checkBox('publishCheck',q=True,v=True)
        
        #full path to scene
        scenePath = cmds.file(q=True,sn=True)
        
        #shaders
        if doShaders == 1:
            ctrlObjs = disconnectRig()
            numberOfFiles += exportShaders(publishName,scenePath)
            reconnectRig(ctrlObjs)
            
            for ctrl in ctrlObjs:
                print 'control objects = %s'%ctrl

        #alembic
        if doAlembic == 1:
            makeAlembic(publishName, sel[0])
            alembicExported = 1

        #binary
        makeRefLog = [0,0,0]
        if doBinary == 1:
            cmds.select(tempSelect,r=True)
            makeRefLog = makeRef(publishName, sel[0])
            
        #log
        writeLog(publishName, makeRefLog[0], makeRefLog[1], makeRefLog[2],alembicExported,numberOfFiles)
        
        #dialog
        CompleteDialog(numberOfFiles, numberOfMultiShaders, alembicExported)

    #display errors
    elif len(sel) > 1:
        cmds.error('select only ONE object to publish')
    else:
        cmds.error('select an object to publish')
    
def publishModel():
    
    #init log variables
    numberOfFiles = 0
    numberOfMultiShaders = 0
    alembicExported = 0
    
    #list objects
    sel = cmds.ls(sl=True)
    if len(sel) == 1:
        #get publish name from textfield
        publishName = assumedPublishName()
        #get current selection so that it can be re-selected at the end
        tempSelect = cmds.ls(sl=True)
        
        #full path to scene
        scenePath = cmds.file(q=True,sn=True)
        
        #shaders
        ctrlObjs = disconnectRig()
        numberOfFiles += exportShaders(publishName,scenePath)
        reconnectRig(ctrlObjs)

        #alembic
        makeAlembic(publishName, sel[0])
        alembicExported = 1

        #binary
        makeRefLog = [0,0,0]
        cmds.select(tempSelect,r=True)
        makeRefLog = makeRef(publishName, sel[0])
            
        #log
        writeLog(publishName, makeRefLog[0], makeRefLog[1], makeRefLog[2],alembicExported,numberOfFiles)
        
        #dialog
        CompleteDialog(numberOfFiles, numberOfMultiShaders, alembicExported)

    #display errors
    elif len(sel) > 1:
        cmds.error('select only ONE object to publish')
    else:
        cmds.error('select an object to publish')   


###    LOG    ###

def writeLog(refFileName, pathName, scenePath, backupName,alembicExported,shaderExport):

    #log
    #get parent folder
    scenePath = cmds.file(q=True,sn=True)
    currentFolder = scenePath.rsplit('/',1)[0]
    #machine name 
    computer = platform.node()
    #Create A String Array With Test Data
    filePath = '%s/log/%s.mb.log'%(currentFolder,refFileName)
    if not os.path.exists('%s/log'%(currentFolder)):
        os.makedirs('%s/log'%(currentFolder))
    text_file = open(filePath, 'a')
    #Print Array To File
    log = '%s\nPublished to        %s\nPublished from      %s\nBackup file         %s\nAlembic Exported    %s\nShaders Exported    %s\nMachine             %s\n\n'%(cmds.date(),pathName,scenePath,backupName,alembicExported,shaderExport,computer)
    text_file.write(log)
    #Close File
    text_file.close() 
         
###    UI    ###

#Complete Dialog
def CompleteDialog(numberOfFiles, numberOfMultiShaders, alembicExported):

    alembicMessage = ''
    if alembicExported == 1:
        alembicMessage = '\n\nAlembic Export successful'

    #nice display message
    message = 'Exported %d materials with %d warnings %s'%(numberOfFiles,numberOfMultiShaders,alembicMessage)
    if numberOfFiles == 1:
        message = 'Exported %d file'%(numberOfFiles)
    
    #create dialog
    response = cmds.confirmDialog(title='Completed!',
                          message=message,
                          button=['Okay','Close'],
                          defaultButton="Okay",
                          cancelButton="Close",
                          dismissString="Close")   
    if response == 'Close':

        cmds.deleteUI('Publish REF Window')


#set text field
def assumedPublishName():
    #check if publish name exists (object has been published before)
    sel = cmds.ls(sl=True)
    if sel and (cmds.attributeQuery('publishName', node=sel[0],exists=True)):
        publishName = cmds.getAttr(sel[0]+'.publishName')
    else:
        #guess publish name
        filename = cmds.file(q=True,sn=True,shn=True)
        splitName = filename.split('.')
        parts = splitName[0].split('_')
        publishName =  (parts[0] + "_REF")
    return publishName

def setTextField():
    publishName = assumedPublishName()
    cmds.textField('nameText',e=True,tx=publishName)

def IO_publishModel_window():
    #UI objects
    publishForm = cmds.formLayout()
    textLabel = cmds.text(label='Publish Name')
    nameText = cmds.textField('nameText',w=250)
    reloadButton = cmds.iconTextButton(style='iconOnly',image1='refresh.png',c='setText()')
    shadersCheck = cmds.checkBox('shadersCheck',l='Export Shaders',v=1)
    alembicCheck = cmds.checkBox('alembicCheck',l='Export Alembic',v=1)
    publishCheck = cmds.checkBox('publishCheck',l='Create REF',v=1)
    btn1 = cmds.button(l='Publish',h=50,c='PublishModelCheckText()')
    btn2 = cmds.button(l='Close',h=50,c='cmds.deleteUI(\'Publish REF Window\')')
    #UI layout
    cmds.formLayout(
        publishForm,
        edit=True,
        attachForm=[
        (textLabel,'top',15),
        (textLabel,'left',10),
        (reloadButton,'top',10),
        (reloadButton,'right',10),
        (nameText,'top',10),
        (shadersCheck,'left',90),
        (alembicCheck,'left',90),
        (publishCheck,'left',90),
        (btn1,'bottom',0),
        (btn1,'left',0),
        (btn2,'bottom',0),
        (btn2,'right',0)
        ],
        attachControl=[
        (nameText,'left',10,textLabel),
        (nameText,'right',10,reloadButton),
        (shadersCheck,'top',15,textLabel),
        (alembicCheck,'top',15,shadersCheck),
        (publishCheck,'top',15,alembicCheck),
        (btn2,'left',0,btn1)
        ],
        attachPosition=[
        (btn1,'right',0,50)
        ])
    setTextField()

def IO_publishModel(silent):
    if silent == 1:
        print 'silent mode'
        publishModel()
    else:
        workspaceName = 'Publish REF Window'
        if(cmds.workspaceControl(workspaceName, exists=True)):
            cmds.deleteUI(workspaceName)
        cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'IO_publishModel_window()')

        

#IO_publishModel(0) 