import maya.cmds as cmds
import os
def OpenRenderFolder(folderType):
    #path definitions
    workspace = cmds.workspace(q=True,fullName=True)
    imagePath = cmds.renderSettings(fin=True,fp=True)[0]
    tempImagePath = cmds.renderSettings(fin=True,fpt=True)[0]
    sourceimagesPath = '%s/sourceimages/'%(workspace)
    
    locations = [imagePath,tempImagePath,sourceimagesPath]
    
    folderPath = locations[folderType].rsplit('/',1)[0]
    ntfolderPath = folderPath.replace('/','\\')

    #make folder if it doesn't exist
    if not os.path.exists(ntfolderPath):
            os.makedirs(ntfolderPath)
    try:
        #open folder 
        os.startfile(ntfolderPath)
    except:
        cmds.error ('Folder does\'t exist and can not be created')
#OpenRenderFolder(0)
