#make reference .mb
import maya.cmds as cmds
from os import path
from shutil import copyfile

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
#mr = makeRef('kitty_REF','KBB_GEO_GRP')
#print mr