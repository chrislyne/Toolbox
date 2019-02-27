import maya.cmds as cmds
import maya.mel as mel

def importAnimation():

    #check if plug is already loaded
    if not cmds.pluginInfo('AbcExport',query=True,loaded=True):
        try:
            #load abcExport plugin
            cmds.loadPlugin( 'AbcExport' )
        except: cmds.error('Could not load AbcExport plugin')

    myWorkspace = cmds.workspace( q=True, fullName=True )
    myAlembics = myWorkspace+'/cache/alembic'

    basicFilter = "*.abc"
    selectedABC = cmds.fileDialog2(fm=4,fileFilter=basicFilter, dir=myAlembics)

    #create top level group
    if cmds.objExists('|ANIM') == 0:
        newRootGroup = cmds.group(em=True,n='ANIM')

    existingObjs = cmds.ls(transforms=True)

    for abc in selectedABC:
        grpName = '%s_GRP'%abc.split('/')[-1].split('.')[0]
        print grpName
    
        newGroup = cmds.group(em=True,n=grpName)
        cmds.parent(newGroup,'|ANIM')
        command = "AbcImport -reparent \"|ANIM|"+newGroup+"\" -mode import \""+abc+"\""
        mel.eval(command)

    updatedObjs = cmds.ls(transforms=True)

    newObjs = [x for x in updatedObjs if x not in existingObjs]
    cmds.select(newObjs,r=True)

    #import materials
    lio.io_importMaterials.assignMaterials()

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
#importAnimation();