import maya.cmds as cmds
import maya.mel as mel

def importAnimation():

    myWorkspace = cmds.workspace( q=True, fullName=True )
    myAlembics = myWorkspace+'/cache/alembic'

    basicFilter = "*.abc"
    selectedABC = cmds.fileDialog2(fm=4,fileFilter=basicFilter, dir=myAlembics)

    #create top level group
    if cmds.objExists('|ANIM') == 0:
        newRootGroup = cmds.group(em=True,n='ANIM')
    
    for abc in selectedABC:
        grpName = abc.split('/')[-1].split('.')[0]
        print grpName
    
        newGroup = cmds.group(em=True,n=grpName)
        cmds.parent(newGroup,'|ANIM')
        command = "AbcImport -reparent \"|ANIM|"+newGroup+"\" -mode import \""+abc+"\""
        mel.eval(command)

    #remove curves
    
    #remove empty groups
    
'''
def importAnim(filename):
    command = "AbcImport -mode import \""+filename+"\""; 
    mel.eval(command)
    setupSceneFromCam()

def importAnimDialog():
    myWorkspace = cmds.workspace( q=True, fullName=True )
    myAlembics = myWorkspace+'/cache/alembic'
    filename = cmds.fileDialog2(fileMode=1, dir=myAlembics, caption="Import Camera")
    #import camera
    if (filename):
        importAnim(filename[0])
'''
#abc_importAnimation();