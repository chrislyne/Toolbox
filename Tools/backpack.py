import maya.cmds as cmds
import maya.mel as mel
import os
import myUtils
reload(myUtils)
import moveFiles
reload(moveFiles)
import tempfile

import json

def getDbToken():
	#get token
	tPath = cmds.textField('tokenPathField',q=True,tx=True)
	if tPath:
		text_file = open(tPath, "r")
		lines = text_file.readlines()
		text_file.close()
		return lines[0]

def loadPrefs():
	prefPath = myUtils.paths.userPrefsPath()
	prefFile = '%s/toolboxPrefs.json'%(prefPath)
	try:
		with open(prefFile) as json_data:
			data = json.load(json_data)
			json_data.close()
		return data
	except:
		pass

def browseToFolder():
	folder = cmds.fileDialog2(fileMode=3, dialogStyle=1)
	if folder:
		cmds.textField('localFolderPath',e=True,tx=folder[0])
		userDict = {"backpack": {"localPath":  folder[0]}}
		prefPath = myUtils.paths.userPrefsPath()
		jsonFileName  = '%s/toolboxPrefs.json'%prefPath
		moveFiles.localFiles.savePrefs(userDict,jsonFileName)
		allFolders =  ListFolders('%s/'%folder[0])
		populateOptionMenu(allFolders)

def browseToToken():
	file = cmds.fileDialog2(fileMode=1, dialogStyle=1)
	if file:
		cmds.textField('tokenPathField',e=True,tx=file[0])
		userDict = {"backpack": {"tokenPath":  file[0]}}
		prefPath = myUtils.paths.userPrefsPath()
		jsonFileName  = '%s/toolboxPrefs.json'%prefPath
		moveFiles.localFiles.savePrefs(userDict,jsonFileName)
		token = getDbToken()
		if token:
			allFolders =  moveFiles.httpDropbox.listFiles('/Projects/Backpack/Sorted',token)
			populateOptionMenu(allFolders)

def toggleVis():
	if cmds.columnLayout('settingsMenu',vis=True,q=True):
		cmds.columnLayout('settingsMenu',vis=False,e=True)
	else:
		cmds.columnLayout('settingsMenu',vis=True,e=True)

def setText(textBox):
	sel = cmds.ls(sl=True) 
	if sel:
		cmds.textField (textBox,edit=True,tx=sel[0])

def exportAbc(objects,newpath,name):
	#create folder
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	#do export
	exportCommand = 'AbcExport -j "-frameRange 1 1 -stripNamespaces -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa '
	for obj in objects:
		exportCommand += '-root '+obj+' '
	exportCommand += '-file '+newpath+'/'+name+'.abc"'
	mel.eval(exportCommand)

def exportFile():
	#selected objects
	objects = cmds.ls(sl=True)
	#check objects are selected

	if len(objects)>0:
		#create new file
		class2 = cmds.textField( "modelClassInputText", q=True, text=True)
		name = cmds.textField( "modelNameInputText", q=True, text=True)
		#find textures
		fileNodes = myUtils.shadingNetwork.listShadingNodes(objects,'file')
		if fileNodes:
			filePaths = myUtils.shadingNetwork.listFilePaths(fileNodes)
		#export to local folder
		if cmds.optionMenu("storageType",q=True,v=True) == 'Local Folder':
			newpath = '%s/%s'%(cmds.textField('localFolderPath',q=True,tx=True),class2)
			#export alembic
			exportAbc(objects,newpath,name)
			#copy textures
			moveFiles.localFiles.copyFiles(filePaths,'%s/%s'%(newpath,name))

		elif cmds.optionMenu("storageType",q=True,v=True) == 'Dropbox App':
			#get token
			token = getDbToken()
			if token:
				newpath = tempfile.gettempdir().replace('\\','/')
				#export alembic
				exportAbc(objects,newpath,name)

				moveFiles.httpDropbox.uploadFileToDB('%s/%s.abc'%(newpath,name),'/Projects/Backpack/Sorted/%s/%s.abc'%(class2,name),token)
				#copy textures
				tempLocations = moveFiles.localFiles.copyFiles(filePaths,'%s'%(newpath))
				for t in tempLocations:
					fileName = t.split('/')[-1]
					moveFiles.httpDropbox.uploadFileToDB(t,'/Projects/Backpack/Sorted/%s/%s/%s'%(class2,name,fileName),token)
			else:
				cmds.warning('no token file set')
		#reset menu state
		cmds.optionMenu( "modelClass", edit=True, vis=True)
		cmds.textField("modelClassInputText", edit=True, vis=False)

	#handle errors
	else:
		cmds.error('You must select an object to export')

def ListFolders(path):
	if(os.path.isdir(path)):
		dirs = []
		files = os.listdir( path )
		
		for aFile in files:
			if(os.path.isdir(path+'/'+aFile)): 
				dirs.append(aFile)
		return dirs


## UI FUUNCTIONS ##

def toggleStorageType():
	storageType = cmds.optionMenu("storageType", v=True,q=True)
	print storageType
	if storageType == 'Dropbox App':
		cmds.rowLayout('dbPathGrp',e=True,vis=True) 
		cmds.rowLayout('localPathGrp',e=True,vis=False) 
		token = getDbToken()
		allFolders =  moveFiles.httpDropbox.listFiles('/Projects/Backpack/Sorted',token)
		populateOptionMenu(allFolders)
	else:
		cmds.rowLayout('dbPathGrp',e=True,vis=False) 
		cmds.rowLayout('localPathGrp',e=True,vis=True) 
		folder = cmds.textField('localFolderPath',q=True,tx=True)
		if folder:
			allFolders =  ListFolders('%s/'%folder)
			populateOptionMenu(allFolders)

	#save prefs to disk
	userDict = {"backpack": {"storageType":  storageType}}
	prefPath = myUtils.paths.userPrefsPath()
	jsonFileName  = '%s/toolboxPrefs.json'%prefPath
	moveFiles.localFiles.savePrefs(userDict,jsonFileName)

def printNewMenuItem( item ):
	if(item == "Create New"):
		cmds.optionMenu( "modelClass", edit=True, vis=False)
		cmds.textField("modelClassInputText", edit=True, vis=True)
		cmds.textField("modelNameInputText", edit=True, vis=True)
	else:
		cmds.textField("modelClassInputText", edit=True, text=item)

def populateOptionMenu(allFolders):
	#clear items from optionMenu
	menuItems = cmds.optionMenu('modelClass', q=True, itemListLong=True)
	if menuItems:
		cmds.deleteUI(menuItems)
	cmds.menuItem(label="Create New")
	cmds.menuItem(divider=True)
	print allFolders
	if allFolders:
		for file in allFolders:
			cmds.menuItem(label=file)

	cmds.optionMenu( 'modelClass', edit=True, vis=True)
	cmds.textField('modelClassInputText', edit=True, vis=False)

	if(cmds.optionMenu('modelClass', q=True, numberOfItems=True)>2):
		cmds.optionMenu('modelClass', edit=True, sl=3)

def ReturnToOptionMenu(self,selfMenu, item):
	cmds.optionMenu( selfMenu, edit=True, vis=True)
	cmds.textField(self, edit=True, vis=False)
	cmds.menuItem(parent=selfMenu,label=item)
	cmds.optionMenu(selfMenu, edit=True, v=item)

def UpdateMenus():
	printNewMenuItem(cmds.optionMenu("modelClass",q=True,v=True ))

def BackpackWindow():
	
	data = loadPrefs()
	localPath = ''
	storageType = 'Local Folder'
	tokenPath = ''
	try:
		localPath = data['backpack']['localPath']
	except:
		pass
	try:
		tokenPath = data['backpack']['tokenPath']
	except:
		pass
	try:
		storageType = data['backpack']['storageType']
	except:
		pass
	localVis = 0
	dropboxVis = 1
	if storageType == 'Local Folder':
		localVis = 1
		dropboxVis = 0
	
	modelingForm = cmds.formLayout('modelingForm')
	
	#setting menu
	settingsButton = cmds.iconTextButton(style='iconOnly',image1='gear.png',c='toggleVis()')
	settingsMenu = cmds.columnLayout('settingsMenu',vis=False,adj=True) 
	cmds.optionMenu("storageType", w=50,changeCommand='toggleStorageType()')
	cmds.menuItem(label="Local Folder")
	cmds.menuItem(label="Dropbox App")
	cmds.optionMenu("storageType", e=True,v=storageType)
	cmds.rowLayout('localPathGrp',numberOfColumns=2,adj=1,vis=localVis) 
	
	localFolderPath = cmds.textField('localFolderPath',ed=False,tx=localPath)
	browseBtn =  cmds.button(l='...',c='browseToFolder()',w=30)
	cmds.setParent(settingsMenu)
	cmds.rowLayout('dbPathGrp',numberOfColumns=2,adj=1,vis=dropboxVis) 
	tokenPathField = cmds.textField('tokenPathField',ed=False,tx=tokenPath)
	cmds.button(l='...',w=30,c='browseToToken()')
	cmds.setParent(settingsMenu)
	
	cmds.setParent(modelingForm)
	
	typeText = cmds.text(label="Type")
	nameText = cmds.text(label="Name")
	reloadButton = cmds.iconTextButton(style='iconOnly',image1='refresh.png',c='setText(\'modelNameInputText\')')

	modelBtn1 = cmds.button("modelBtn1",l='Pocket',h=50,w=200,c='exportFile()')

	#model class menu
	modelClass = cmds.optionMenu("modelClass", w=50,changeCommand='UpdateMenus()')
	cmds.menuItem(label="Create New")
	cmds.menuItem(divider=True)

	modelClassInputText = cmds.textField ("modelClassInputText", w=50, vis=False, cc='ReturnToOptionMenu("modelClassInputText","modelClass",cmds.textField("modelClassInputText",q=True,tx=True ))')
	if(cmds.optionMenu(modelClass, q=True, numberOfItems=True)>2):
		cmds.optionMenu(modelClass, edit=True, sl=3)
	
	#model name menu
	modelNameInputText = cmds.textField ("modelNameInputText")

	
	cmds.formLayout( modelingForm, edit=True, 
					attachForm=[
					 (settingsMenu,'left',10),
					 (settingsMenu,'right',40),
					 (settingsButton, 'right', 0),
					 (modelBtn1, 'left', 0),
					 (modelBtn1, 'right', 0),
					 (typeText, 'left', 10),
					 (nameText, 'left', 10),
					 (reloadButton,'right',10),
					 (modelBtn1,'bottom',0),
					 (modelClass, 'left', 50),
					 (modelClassInputText, 'left', 50),
					 (modelNameInputText, 'left', 50),
					 (modelClass, 'right', 10),
					 (modelClassInputText, 'right', 10),
					 (modelNameInputText, 'right', 10)
					],
					attachControl=[
					 (modelClass,'right',10,reloadButton),
        			 (modelClassInputText,'right',10,reloadButton),
        			 (modelNameInputText,'right',10,reloadButton),
					 (reloadButton,'top',72,settingsMenu),
					 (typeText, 'top', 42,settingsMenu),
					 (modelClass, 'top', 40,settingsMenu),
					 (modelClassInputText, 'top', 40,settingsMenu),
					 (modelNameInputText, 'top', 70,settingsMenu),
					 (nameText, 'top', 72,settingsMenu)
        			]
					 )
	cmds.setParent( '..' )

	setText('modelNameInputText')
	
	toggleStorageType()
	UpdateMenus()

#import studiIO
#from studiIO import *
#StudioIOWindow()
def dockingBackpack():
	WorkspaceName = 'Backpack'
	if (cmds.workspaceControl('Backpack', exists=True)):
		cmds.deleteUI('Backpack')
	cmds.workspaceControl( WorkspaceName,initialHeight=500,initialWidth=320, uiScript = 'BackpackWindow()' )

#dockingBackpack()