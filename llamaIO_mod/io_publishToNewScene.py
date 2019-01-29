import subprocess
import maya.cmds as cmds
import os
import io_publishAnimation
from io_publishAnimation import IO_publishAnim_window
import io_publishCamera
from io_publishCamera import io_exportCamera_window
from LlamaIO import containsDigits
from LlamaIO import addPadding
from LlamaIO import UserPrefs 


def runExportScripts():
    animPath = io_publishAnimation.IO_publishAnim(1)
    cameraPath = io_publishCamera.io_exportCamera(1)

    makeNewFile(animPath,cameraPath)

#make nice file name  
def niceFileName(filename,variant,initials):
    import re 
    #split filename into workable parts
    fParts = filename.split('_')    
    #retain prefix but make sure it's not 'shot'
    filePrefix = ''
    for parts in fParts:
        if containsDigits(parts):
            break
        if parts.lower() == 'shot':
            break
        if parts.lower() == 'sh':
            break
        filePrefix += '%s_'%parts
    #identify numbers
    numbers = re.sub("[a-zA-Z.]", "", filename)
    parts = numbers.split('_')    
    numbers = filter(None, numbers.split('_'))
    #identify version
    version = '_v001'
    if len(numbers) > 0:
        version = '_v%s'%addPadding(numbers[-1],3)
    #identify shot number
    shotName = ''
    if len(numbers) > 1:
        shotName = 'SH%s'%addPadding(numbers[0],4)
    #add variant
    if variant:
        variant = '_%s'%variant
    #add variant
    if initials:
        initials = '_%s'%initials
        
    renderFileName = '%s%s%s%s%s.mb'%(filePrefix,shotName,variant,version,initials)
    return renderFileName

def makeNewFile(animPath,cameraPath):
    filename = cmds.file(q=True,sn=True)
    currentFolder = filename.rsplit('/',1)[0]
    #replace current folder with 'RENDER'
    newFolder = currentFolder.replace('ANIM','RENDER')
    newFolder = newFolder.replace('TVC','RENDER')
    #make sure the folder exists
    if not os.path.exists(newFolder):
        os.makedirs(newFolder)
    #get final file name/path
    fileName = niceFileName(filename.rsplit('/',1)[1],'RENDER',UserPrefs.getUserPrefs())
    renderFilename = '%s/%s'%(newFolder,fileName)
    #execute
    command = r'C:/Progra~1/Autodesk/Maya2017/bin/mayabatch.exe -command "saveFile(""%s"",""%s"",""%s"")"'%(renderFilename,animPath,cameraPath)
    subprocess.Popen(command,shell=True)

#runExportScripts()