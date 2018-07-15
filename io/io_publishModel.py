import maya.cmds as cmds

#add attributes
def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')

#publish shaders
def exportShaders(publishName):
    
    #initalise variables 
    allGeo = ""
    allMaterials = []
    
    #select hierarchy
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True )
    allDecendingShapes = cmds.ls(allDecending,s=True,l=True)
    
    #loop though if they have materials
    for shape in allDecendingShapes:
        shadingGroups = cmds.listConnections(shape,type='shadingEngine')
        if shadingGroups:
            allGeo += '-root %s '%(shape)
            allMaterials += shadingGroups
            
            #add attributes to shape nodes
            addAttribute(shape,'alembicName',publishName)
            addAttribute(shape,'material',shadingGroups)
            ID = cmds.ls(shape,uuid=True)
            addAttribute(shape,'IOID',ID[0])

    #materials used in our hierachy    
    allMaterials = list(set(allMaterials))  
    
    #log
    shaderCount = 0
    
    #get workspace
    workspace = cmds.workspace(q=True,fullName=True)
    
    for material in allMaterials:
        #process namespaces
        materialFilename = material.replace(':', '_')
        #export material
        cmds.select(material,r=True,noExpand=True)  
        cmds.file('%s/renderData/alembicShaders/%s/%s_%s.mb'%(workspace,publishName,publishName,materialFilename),force=True,typ='mayaBinary',pr=True,es=True)
        
        #increment to log
        shaderCount += 1

    return shaderCount

"""
#update name and run
def PublishModelCheckText():
    #list objects
    sel = cmds.ls(sl=True)
    if len(sel) == 1:
        publishString = sel[0]
        #remove namespaces from scene 
        #removeSceneNamespaces <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        publishName = cmds.textField(nameText,q=True,text=True)
        tempSelect = cmds.ls(sl=True)
       
        #shaders
        exportShaders = cmds.checkBox(shadersCheck,q=True,v=True)
        exportAlembic = cmds.checkBox(alembicCheck,q=True,v=True)
        shadersEported[]
        alembicExported = 0
        
        if exportShaders == 1:
            #DisconnectShadingNetworks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #shadersExport[] = exportShaders(publishName)<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #shadersEported = shadersExport<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #Reconnect<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        #alembic
        alembicLog = ''
        if exportAlembic == 1:
            #alembicExport = makeAlembic(publishName, publishString)<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            alembicExported = 1
            alembicLog = ('\nAlembic             '+alembicExport)

        #binary
        cmds.select(r=True,tempSelect)
        #makeRefLog[] = makeRef(publishName, publishString)<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #log
        #writeLog(publishName,makeRefLog[0],makeRefLog[1],makeRefLog[2],shadersEported[0],alembicLog)<<<<<<<<<<
        
        #completeDialog(shadersEported[0], shadersEported[1],alembicExported)

    #display errors
    else if(len(sel) > 1):
        cmds.error('select only ONE object to publish')
    else:
        cmds.error('select an object to publish')
"""

###    LOG    ###
   
         
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
def setText():
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
    #set textField text
    cmds.textField('nameText',e=True,tx=publishName)


def IO_publishModel_window():
    #UI objects
    publishForm = cmds.formLayout()
    textLabel = cmds.text(label='Publish Name')
    nameText = cmds.textField('nameText',w=250)
    reloadButton = cmds.iconTextButton(style='iconOnly',image1='refresh.png',c='setText()')
    shadersCheck = cmds.checkBox(l='Export Shaders',v=1)
    alembicCheck = cmds.checkBox(l='Export Alembic',v=1)
    publishCheck = cmds.checkBox(l='Create REF',v=1)
    btn1 = cmds.button(l='Publish',h=50,c='PublishModelCheckText()')
    btn2 = cmds.button(l='Close',h=50,c='deleteUI shaderExportWindow')
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
    setText()

def IO_publishModel():
    workspaceName = 'Publish REF Window'
    if(cmds.workspaceControl(workspaceName, exists=True)):
        cmds.deleteUI(workspaceName)
    cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'IO_publishModel_window()')

IO_publishModel()