import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
import baseIO.stringFormat as stringFormat
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
import os
import time
import Tools.screenshot as screenshot
from stat import S_ISREG, ST_MTIME, ST_MODE
import baseIO.incrementalSave as incSave
from lio.io_publishModel import IO_publishModel,IO_publishModel_window,PublishModelCheckText
import pipelime.resources.lm_resources
import json

def doubleClicked():
    print 'double clicked'
    assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setVisible(1)

def selectFolder():
    filename = QtWidgets.QFileDialog.getExistingDirectory()
    projectName = filename.split('/')[-2]
    projectPath = filename
    projectData = []
    projectData.append([projectName,'projectPath',projectPath])
    IO.writePrefsToFile(projectData,'%s/projects.json'%qtBase.local_path())
    assetManagerUIWindow.mainWidget.project_comboBox.addItems([projectName])
    assetManagerUIWindow.mainWidget.project_comboBox.setCurrentText(projectName)

#removes project from project combobox
def removeProject():
    #read curent project from dropdown menu
    currentProject = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    #load project dictionary
    projectDict = IO.loadDictionary('%s/projects.json'%qtBase.local_path())
    #remove current project from dictionary
    del projectDict[currentProject]
    #write out to json file
    with open('%s/projects.json'%qtBase.local_path(), mode='w') as feedsjson:
        json.dump(projectDict, feedsjson, indent=4, sort_keys=True)
    #remove text from dropdown menu
    assetManagerUIWindow.mainWidget.project_comboBox.removeItem(assetManagerUIWindow.mainWidget.project_comboBox.currentIndex())


def publishModel():
    IO_publishModel(0)
    metaData = []
    localPrefDict = IO.loadDictionary('%s/localPrefs.json'%qtBase.local_path())
    metaData.append(['user','value','%s'%localPrefDict["userName"]["value"].strip('\'')])
    metaData.append(['note','value','%s'%assetManagerUIWindow.mainWidget.textEdit_note.toPlainText()])
    folderName = getProj.sceneFolder().rsplit('/',1)[1]
    IO.writePrefsToFile(metaData,'%s/.data/%s_REF.json'%(getProj.sceneFolder(),folderName))

def incrementSceneFile():
    localPrefDict = IO.loadDictionary('%s/localPrefs.json'%qtBase.local_path())
    try:
        userInitials = localPrefDict["userInitials"]["value"].strip('\'')
    except:
        userInitials = ''
    incSave.IncrementCurrentFile(initials=userInitials)
    writeDataAfterSave()

def saveSceneFile():
    cmds.file(save=True)
    writeDataAfterSave()

def writeDataAfterSave():
    metaData = []
    localPrefDict = IO.loadDictionary('%s/localPrefs.json'%qtBase.local_path())
    metaData.append(['user','value','%s'%localPrefDict["userName"]["value"].strip('\'')])
    metaData.append(['note','value','%s'%assetManagerUIWindow.mainWidget.textEdit_note.toPlainText()])
    IO.writePrefsToFile(metaData,'%s/.data/%s.json'%(getProj.sceneFolder(),getProj.sceneName()))


def setProjectPth():
    projectsDict = IO.loadDictionary('%s/projects.json'%qtBase.local_path())
    key = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    cmds.workspace(projectsDict[key]['projectPath'], openWorkspace=True)

def takeScreenshot(assetName,projectsDict):
    global lch
    #assetName = assetManagerUIWindow.mainWidget.listWidget_assets.currentItem().text()
    assetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    assetPath = '%s/scenes/REF/%s/%s'%(projectsDict[project]["projectPath"],assetType,assetName)

    lch = screenshot.ScreenShot()
    imageFileName = '%s/.data/%s_thumb.jpg'%(assetPath,assetName)
    print imageFileName
    lch.launch(imageFileName)

    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.jpg"%(qtBase.self_path(), "tap"))
        window.mainWidget.pushButton_thumb.setIcon(buttonIcon)
        window.mainWidget.pushButton_thumb.setText("")
    except:
        pass

def orderByModified(dirpath):

    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)
    
    # leave only regular files, insert creation date
    entries = ((stat[ST_MTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    
    recentFiles = []
    
    for cdate, path in sorted(entries):
        #print time.ctime(cdate), os.path.basename(path)
        dateModified = time.strftime('%Y/%m/%d - %I:%M %p', time.localtime(os.path.getmtime(path)))
        
        fileDictPath = '%s/.data/%s.json'%(path.rsplit('\\',1)[0],path.split('\\')[-1].rsplit('.',1)[0])
        fileDict = IO.loadDictionary(fileDictPath)
        artistName = ''
        try:
            artistName = fileDict["user"]["value"]
        except:
            pass
        recentFiles.append([os.path.basename(path),artistName,dateModified])
    return recentFiles

def newAsset(projectsDict):

    setProjectPth()

    newAssetType = assetManagerUIWindow.mainWidget.lineEdit_newAssetType.text()
    newAssetName = assetManagerUIWindow.mainWidget.lineEdit_newAssetName.text()
    if newAssetName:
        if not newAssetType:
            newAssetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
        project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
        assetPath = '%s/scenes/REF/%s/%s'%(projectsDict[project]["projectPath"],newAssetType,newAssetName)

        itemsText = []
        items = []
        for index in xrange(assetManagerUIWindow.mainWidget.listWidget_assetType.count()):
            items.append(assetManagerUIWindow.mainWidget.listWidget_assetType.item(index))
            itemsText.append(assetManagerUIWindow.mainWidget.listWidget_assetType.item(index).text())

        if newAssetType not in itemsText:
            #add item to type list
            itm = QtWidgets.QListWidgetItem(newAssetType)
            assetManagerUIWindow.mainWidget.listWidget_assetType.addItem(itm)
            assetManagerUIWindow.mainWidget.listWidget_assets.clear()
            if not os.path.exists(assetPath):
                os.makedirs(assetPath)

        else:
            for i in items:
                if newAssetType == i.text():
                    itm = i
            setType(newAssetType,projectsDict)
        itm.setSelected(True)
        
        #add item to asset list
        itm = QtWidgets.QListWidgetItem(QtGui.QIcon('C:/Users/Admin/Documents/Toolbox/icons/lightRed.png'),newAssetName);
        assetManagerUIWindow.mainWidget.listWidget_assets.addItem(itm);
        itm.setSelected(True)
        #create folder and file
        if not os.path.exists(assetPath):
            os.makedirs(assetPath)
        #create new file
        cmds.file(newFile=True, force=True)
        cmds.file(rename='%s/%s_v001_cl.mb'%(assetPath,newAssetName))
        #set settings from project config file
        try:
            configFolder = '%s../.projectData'%getProj.getProject()
            projectsDict = IO.loadDictionary('%s/projectPrefs.json'%configFolder)
            cmds.setAttr("defaultResolution.width",int(projectsDict["resolutionW"]["value"]))
            cmds.setAttr("defaultResolution.height",int(projectsDict["resolutionH"]["value"]))
            fps = '%sfps'%(projectsDict["frameRate"]["value"])
            cmds.currentUnit(time=fps)
        except:
            pass


def editAsset(assetName,projectsDict):
    #set project
    setProjectPth()
    #read asset
    assetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    assetPath = '%s/scenes/REF/%s/%s'%(projectsDict[project]["projectPath"],assetType,assetName)
    #find latest version
    workingFiles = orderByModified(assetPath)
    if workingFiles:
        #open existing file
        latestFilePath = '%s/%s'%(assetPath,workingFiles[-1][0])
        cmds.file(latestFilePath, open=True, ignoreVersion=True, force=True)
    else:
        #create new file
        cmds.file(newFile=True, force=True)
        cmds.file(rename='%s/%s_v001_cl.mb'%(assetPath,assetName))

    #remove list selection
    items = []
    for index in xrange(assetManagerUIWindow.mainWidget.listWidget_assets.count()):
        assetManagerUIWindow.mainWidget.listWidget_assets.item(index).setSelected(False)
    #clear note
    assetManagerUIWindow.mainWidget.textEdit_note.setText('')


def referenceAsset(assetName,projectsDict,imp):
    #loop through selection
    for item in assetName:
        name = item.text()
        assetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
        project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
        assetPath = '%s/scenes/REF/%s/%s_REF.mb'%(projectsDict[project]["projectPath"],assetType,name)
        #try to load the asset file
        try:
            if imp != 1:
                cmds.file(assetPath, reference=True)
            else:
                cmds.file(assetPath, i=True)
        except:
            print 'unable to load reference %s'%assetPath

def setVersion(assetName,projectsDict):
    #read asset
    assetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    assetPath = '%s/scenes/REF/%s/%s'%(projectsDict[project]["projectPath"],assetType,assetName)
    #find latest version
    workingFiles = orderByModified(assetPath)
    assetManagerUIWindow.mainWidget.tableWidget_assetVersions.clearContents()
    assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setRowCount(0)
    for i,f in enumerate(workingFiles):
        assetManagerUIWindow.mainWidget.tableWidget_assetVersions.insertRow(i)
        assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setItem(i,0, QtWidgets.QTableWidgetItem(f[0]))

        nameItem = QtWidgets.QTableWidgetItem(f[1])
        assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setItem(i,1, nameItem)

        dateItem = QtWidgets.QTableWidgetItem(f[2])
        dateItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setItem(i,2, dateItem)
        

def setAsset(assetName,projectsDict):

    assetType = assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text()
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    thumbPath = '%s/scenes/REF/%s/%s/.data/%s_thumb.jpg'%(projectsDict[project]["projectPath"],assetType,assetName,assetName)
    #find and display date
    try:
        refPath = '%s/scenes/REF/%s/%s_REF.mb'%(projectsDict[project]["projectPath"],assetType,assetName)
        dateModified = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(refPath)))
        currentDate = time.strftime("%d/%m/%Y", time.localtime())
        if dateModified == currentDate:
            dateModified = 'Today'
        timeModified = time.strftime('%a %I:%M %p', time.localtime(os.path.getmtime(refPath)))
        assetManagerUIWindow.mainWidget.label_date.setText('%s - %s'%(dateModified,timeModified))
    except:
        assetManagerUIWindow.mainWidget.label_date.setText('')
    #find and display username
    try:
        namePath = '%s/scenes/REF/%s/%s/.data/%s_REF.json'%(projectsDict[project]["projectPath"],assetType,assetName,assetName)
        assetDict = IO.loadDictionary(namePath)
        assetManagerUIWindow.mainWidget.label_userName.setText(assetDict["user"]["value"])
    except:
        assetManagerUIWindow.mainWidget.label_userName.setText('')
    #find and display note
    try:
        namePath = '%s/scenes/REF/%s/%s/.data/%s_REF.json'%(projectsDict[project]["projectPath"],assetType,assetName,assetName)
        assetDict = IO.loadDictionary(namePath)
        assetManagerUIWindow.mainWidget.textEdit_note.setText(assetDict["note"]["value"])
    except:
        assetManagerUIWindow.mainWidget.textEdit_note.setText('')
    try:
        buttonIcon = QtGui.QIcon(thumbPath)
        assetManagerUIWindow.mainWidget.pushButton_thumb.setIcon(buttonIcon)
        assetManagerUIWindow.mainWidget.pushButton_thumb.setText("")
        
    except:
        pass
    assetManagerUIWindow.mainWidget.tableWidget_assetVersions.setVisible(0)
    setVersion(assetName,projectsDict)

def setType(key,projectsDict):
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    typePath = '%s/scenes/REF/%s'%(projectsDict[project]["projectPath"],key)

    assetFolders = []
    files = os.listdir(typePath)
    for name in files:
        if os.path.isdir(os.path.join(os.path.abspath(typePath), name)):
            #remove hidden folders
            if name[0] != '.':
                assetFolders.append(name)

    assetManagerUIWindow.mainWidget.listWidget_assets.clear()
    #assetManagerUIWindow.mainWidget.listWidget_assets.addItems(assetFolders)

    for assets in assetFolders:
        itm = QtWidgets.QListWidgetItem(QtGui.QIcon('C:/Users/Admin/Documents/Toolbox/icons/lightRed.png'),assets);
        if os.path.isfile('%s/%s_REF.mb'%(typePath,assets)):
            itm = QtWidgets.QListWidgetItem(QtGui.QIcon('C:/Users/Admin/Documents/Toolbox/icons/lightGreen.png'),assets);

        assetManagerUIWindow.mainWidget.listWidget_assets.addItem(itm);

    #select first item in list
    try:
        items = []
        for index in xrange(assetManagerUIWindow.mainWidget.listWidget_assets.count()):
            items.append(assetManagerUIWindow.mainWidget.listWidget_assets.item(index))

        items[0].setSelected(True)
        assetManagerUIWindow.mainWidget.listWidget_assets.setCurrentItem(items[0])
        setAsset(items[0].text(),projectsDict)
    except:
        pass


def setProject(key):
    projectsDict = IO.loadDictionary('%s/projects.json'%qtBase.local_path())
    print projectsDict
    projectPath = projectsDict[key]["projectPath"]

    assetTypeFolders = []
    path = '%s/scenes/REF/'%projectPath
    files = os.listdir(path)
    for name in files:
        if os.path.isdir(os.path.join(os.path.abspath(path), name)):
            #remove hidden folders
            if name[0] != '.':
                assetTypeFolders.append(name)
    #populate listWidget with folders
    assetManagerUIWindow.mainWidget.listWidget_assetType.clear()
    assetManagerUIWindow.mainWidget.listWidget_assetType.addItems(assetTypeFolders)

    #select first item in list
    try:
        items = []
        for index in xrange(assetManagerUIWindow.mainWidget.listWidget_assetType.count()):
            items.append(assetManagerUIWindow.mainWidget.listWidget_assetType.item(index))

        items[0].setSelected(True)
        assetManagerUIWindow.mainWidget.listWidget_assetType.setCurrentItem(items[0])
        setType(items[0].text(),projectsDict)
    except:
        pass


    #assetManagerUIWindow.mainWidget.listWidget_assetType.currentTextChanged.connect(lambda: setType(assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text(),path))


def assetManagerUI():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'lm_assetManager.ui')
    window._windowTitle = 'Asset Manager'
    window._windowName = 'assetManager'
    window.pathModify = 'pipelime/'
    window.BuildUI()
    window.show(dockable=True)

    projectsDict = IO.loadDictionary('%s/projects.json'%qtBase.local_path())

    projectLines = []
    for key in projectsDict:
        try:
            projectLines.append(key)
        except:
            pass

    window.mainWidget.project_comboBox.addItems(projectLines)
    window.mainWidget.project_comboBox.currentTextChanged.connect(lambda: setProject(window.mainWidget.project_comboBox.currentText()))

    window.mainWidget.listWidget_assetType.currentTextChanged.connect(lambda: setType(window.mainWidget.listWidget_assetType.currentItem().text(),projectsDict))

    #add project button
    window.mainWidget.pushButton_addProject.clicked.connect(selectFolder)
    #remove project button
    window.mainWidget.pushButton_removeProject.clicked.connect(removeProject)
    #change asset selection
    window.mainWidget.listWidget_assets.currentTextChanged.connect(lambda: setAsset(window.mainWidget.listWidget_assets.currentItem().text(),projectsDict))
    window.mainWidget.listWidget_assets.doubleClicked.connect(doubleClicked)
    #reference button
    window.mainWidget.pushButton_reference.clicked.connect(lambda: referenceAsset(window.mainWidget.listWidget_assets.selectedItems(),projectsDict,0))
    #import button
    window.mainWidget.pushButton_import.clicked.connect(lambda: referenceAsset(window.mainWidget.listWidget_assets.selectedItems(),projectsDict,1))
    #new button
    window.mainWidget.pushButton_new.clicked.connect(lambda: newAsset(projectsDict))
    #edit button
    window.mainWidget.pushButton_edit.clicked.connect(lambda: editAsset(window.mainWidget.listWidget_assets.currentItem().text(),projectsDict))
    #thumbnail button
    window.mainWidget.pushButton_thumb.clicked.connect(lambda: takeScreenshot(window.mainWidget.listWidget_assets.currentItem().text(),projectsDict))
    #save button
    window.mainWidget.pushButton_save.clicked.connect(saveSceneFile)
    #increment button
    window.mainWidget.pushButton_increment.clicked.connect(incrementSceneFile)
    #publish button
    window.mainWidget.pushButton_publish.clicked.connect(publishModel)

    #set project in menu
    
    return window

def openAssetManagertWindow():
    global assetManagerUIWindow
    assetManagerUIWindow = assetManagerUI()

    #set project dropdown to current project
    currentProject = cmds.workspace(fullName=True)
    projectsDict = IO.loadDictionary('%s/projects.json'%qtBase.local_path())
    for d in projectsDict:
        if currentProject == projectsDict[d]['projectPath']:
            print d
            assetManagerUIWindow.mainWidget.project_comboBox.setCurrentText(d)
            setProject(d)

openAssetManagertWindow() 
#prefWidget 
#get render layers from scene
