import maya.cmds as cmds
import re
import os

#export animation
def publishFile(abcFilename):
    #get workspace
    workspace = cmds.workspace( q=True, directory=True, rd=True)
    workspaceLen = len(workspace.split('/'))
    #get filename
    filename = cmds.file(q=True,sn=True)
    #get relative path (from scenes)
    relativePath = ''
    for dir in filename.split('/')[8:-1]:
        relativePath += '%s/'%(dir)

    #string of objects to export
    exportString = ''
    sel = cmds.ls(sl=True)
    for item in sel:
        exportString += ' -root %s'%(item)

    #get timeline
    startFrame = int(cmds.playbackOptions(q=True,minTime=True))
    endFrame = int(cmds.playbackOptions(q=True,maxTime=True))

    #set folder to export to  
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
    additionalAttributes = ['alembicName','IOID']
    #redshift attributes
    additionalAttributes += ['rsObjectId','rsEnableSubdivision','rsMaxTessellationSubdivs','rsDoSmoothSubdivision','rsMinTessellationLength','rsOutOfFrustumTessellationFactor','rsEnableDisplacement','rsMaxDisplacement','rsDisplacementScale']
    for attr in additionalAttributes:
        additionalAttr += ' -attr %s'%(attr)
    command = '-frameRange %d %d%s -ro -uvWrite -writeVisibility -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa%s -file %scache/alembic/%s%s.abc'%(startFrame,endFrame,additionalAttr,exportString,workspace,relativePath,abcFilename)
    #write to disk
    cmds.AbcExport ( j=command )
    return '%scache/alembic/%s%s.abc'%(workspace,relativePath,abcFilename)

def runSilent():
    #construct filename from user input
    names = createFilenames()
    publishName = names[0]+'_'+names[1]
    return publishFile(publishName)

#update name and run
def runWithUI():
    #construct filename from user input
    prefixString = cmds.textField('prefixText',q=True,text=True)
    nameString = cmds.textField('nameText',q=True,text=True)
    publishName = prefixString+'_'+nameString
    publishFile(publishName)

def createFilenames():
    #get filename
    filename = cmds.file(q=True,sn=True,shn=True).split('.')[0]
    #set text
    publishName = ''
    sel = cmds.ls(sl=True)
    selection = []
    #remove any unnecessary characters and namespaces
    for item in sel:
        selection.append(re.split(':|\|',item)[-1].replace('_', ''))
    selection = list(set(selection))
    for i,s in enumerate(selection):
        if i != 0:
            publishName += '_'
        publishName += s
    #shorten name if longer than 50 characters
    if len(publishName)>50:
        publishName = '%s_anim'%(selection[0])
    #lengthen name if none exists
    if len(publishName)== 0:
        publishName = 'anim'
    return [filename,publishName]

def anim_setText():
    #get filename
    names = createFilenames()
    cmds.textField('prefixText',e=True,tx=names[0])
    cmds.textField('nameText',e=True,tx=names[1])

def IO_publishAnim_window():
    #UI objects
    publishForm = cmds.formLayout()
    prefixLabel = cmds.text(label='Prefix')
    prefixText = cmds.textField('prefixText',w=250)
    textLabel = cmds.text(label='Publish Name')
    nameText = cmds.textField('nameText',w=250)
    reloadButton = cmds.iconTextButton(style='iconOnly',image1='refresh.png',c='anim_setText()')
    btn1 = cmds.button(l='Publish',h=50,c='runWithUI()')
    btn2 = cmds.button(l='Close',h=50,c='cmds.deleteUI(\'Publish Animation Window\')')
    #UI layout
    cmds.formLayout(
        publishForm,
        edit=True,
        attachForm=[
        (prefixLabel,'top',15),
        (prefixLabel,'left',10),
        (reloadButton,'right',10),
        (prefixText,'top',10),
        (textLabel,'left',10),
        (btn1,'bottom',0),
        (btn1,'left',0),
        (btn2,'bottom',0),
        (btn2,'right',0)
        ],
        attachControl=[
        (prefixText,'left',10,textLabel),
        (prefixText,'right',10,reloadButton),
        (textLabel,'top',10,prefixLabel),
        (nameText,'top',10,prefixLabel),
        (nameText,'left',10,textLabel),
        (nameText,'right',10,reloadButton),
        (reloadButton,'top',10,prefixLabel),
        (btn2,'left',0,btn1)
        ],
        attachPosition=[
        (btn1,'right',0,50)
        ])
    anim_setText()

def IO_publishAnim(silent):
    if silent == 1:
        print 'silent'
        return runSilent()
    else:
        workspaceName = 'Publish Animation Window'
        if(cmds.workspaceControl(workspaceName, exists=True)):
            cmds.deleteUI(workspaceName)
        cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'IO_publishAnim_window()')

#print IO_publishAnim(1)