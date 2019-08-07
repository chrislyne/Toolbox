import maya.cmds as cmds
import maya.mel as mel

def setupSceneFromCam():
    #set attributes from camera
    perspCameras = cmds.listCameras( p=True )
    if(cmds.attributeQuery('frameRate', node=item, exists=True)):
        cameraframeRate = cmds.getAttr(item+'.frameRate')
        cmds.currentUnit(time=cameraframeRate)
    if(cmds.attributeQuery('width', node=item, exists=True)):
        cameraWidth = cmds.getAttr(item+'.width')
        cmds.setAttr( 'defaultResolution.width', cameraWidth )
    if(cmds.attributeQuery('height', node=item, exists=True)):
        cameraHeight = cmds.getAttr(item+'.height')
        cmds.setAttr( 'defaultResolution.height', cameraHeight )
    if(cmds.attributeQuery('startFrame', node=item, exists=True)):
        cameraStart = cmds.getAttr(item+'.startFrame')
        cmds.setAttr( 'defaultRenderGlobals.startFrame', cameraStart )
        cmds.playbackOptions(min=cameraStart,ast=cameraStart)
    if(cmds.attributeQuery('endFrame', node=item, exists=True)):
        cameraEnd = cmds.getAttr(item+'.endFrame')
        cmds.setAttr( 'defaultRenderGlobals.endFrame', cameraEnd )
        cmds.playbackOptions(max=cameraEnd,aet=cameraEnd)
            
def importCamera(filename):
    command = "AbcImport -mode import \""+filename+"\""; 
    mel.eval(command)
    setupSceneFromCam()

def importCameraDialog():
    myWorkspace = cmds.workspace( q=True, fullName=True )
    myAlembics = myWorkspace+'/cache/alembic'
    filename = cmds.fileDialog2(fileMode=1, dir=myAlembics, caption="Import Camera")
    #import camera
    if(filename):
        importCamera(filename[0])






