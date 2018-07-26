import maya.cmds as cmds
import os
import io_publishAnimation
from io_publishAnimation import IO_publishAnim_window
import io_publishCamera
from io_publishCamera import io_exportCamera_window


def runExportScripts():
	animPath = io_publishAnimation.IO_publishAnim(1)
	cameraPath = io_publishCamera.io_exportCamera(1)

	makeNewFile(animPath,cameraPath)

def makeNewFile(animPath,cameraPath):

    filename = cmds.file(q=True,sn=True)
    currentFolder = filename.rsplit('/',1)[0]
    
    newFolder = currentFolder.replace('ANIM','RENDER')
    newFolder = newFolder.replace('TVC','RENDER')
    print newFolder
    if not os.path.exists(newFolder):
        os.makedirs(newFolder)
        
    renderFilename = '%s/foobar'%(newFolder)
    command = 'os.system(\'C:/Progra~1/Autodesk/Maya2017/bin/mayabatch.exe -command "saveFile(\"\"%s\"\",\"\"%s\"\",\"\"%s\"\")"\')'%(renderFilename,animPath,cameraPath)

    print command
    eval(command) 

#runExportScripts()