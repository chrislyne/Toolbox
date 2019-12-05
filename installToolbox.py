import maya.cmds as cmds
import sys
#from pymel.all import *
import maya.mel as mel
import json
import os
import urllib2
from collections import OrderedDict

def createShelf(shelfName):
	
	shelfExists = 0
	names = cmds.layout('ShelfLayout',q=True,ca=True)
	for name in names:
		if name == shelfName:
			shelfExists = 1
	
	if shelfExists == 1:
		print 'Shelf {} Exists'.format(shelfName)
	else:
		print 'Shelf {} does not exist'.format(shelfName)
		mel.eval("addNewShelfTab(\"%s\");"%shelfName)

def RemoveSeparator(shelfName,iconName):
	createShelf(shelfName)
	shelfButtons = cmds.shelfLayout(shelfName,q=True,childArray=True)

	if shelfButtons:
		for btn in shelfButtons:
			label = ''

			#Assert that this is a shelfButton
			if cmds.objectTypeUI(btn,isType='separator'):
				cmds.deleteUI(btn)

def RemoveButton(shelfName,iconName):
	shelfButtons = cmds.shelfLayout(shelfName,q=True,childArray=True)

	if shelfButtons:
		for btn in shelfButtons:
			label = ''

			#Assert that this is a shelfButton
			if cmds.objectTypeUI(btn,isType='shelfButton'):

				label = cmds.shelfButton(btn,q=True,label=True)

				#If this button has the label we're looking for,
				#delete the button.
				if iconName == label:
					cmds.deleteUI(btn)

def downloadFile(remote, local):

	
	u = urllib2.urlopen(remote)
	h = u.info()
	totalSize = int(h["Content-Length"])

	filePath = local.rsplit('/',1)

	#make folder
	if len(filePath) > 1:
		if not os.path.exists('%s'%(filePath[0])):
			os.makedirs('%s'%(filePath[0]))
	
	print "Downloading %s bytes..." % totalSize,
	fp = open(local, 'wb')
	
	blockSize = 8192 #100000 # urllib.urlretrieve uses 8192
	count = 0
	while True:
		chunk = u.read(blockSize)
		if not chunk: break
		fp.write(chunk)
		count += 1
		if totalSize > 0:
			percent = int(count * blockSize * 100 / totalSize)
			if percent > 100: percent = 100
			print "%2d%%" % percent,
			if percent < 100:
				print "\b\b\b\b\b",  # Erase "NN% "
			else:
				print "Done."
	
	fp.flush()
	fp.close()
	if not totalSize:
		print

def checkGroups(shelfName):
	#check that shelf exists
	createShelf(shelfName)
	
	#read json
	try:
		JSONPath = cmds.textField('jsonPathText',q=True, text=True)
		with open(JSONPath) as data_file:	
			data = json.load(data_file)

		children = cmds.columnLayout('listLayout',q=True,ca=True)
		allButtons = []
		for c in children:

			if cmds.checkBox(c,q=True,v=True):
				cName = cmds.checkBox(c,q=True,l=True)
				buttons = (data[cName]['buttons'])
				allButtons += buttons

			cmds.deleteUI(c)

		#remove separators
		RemoveSeparator(shelfName,'separator')

		AddIcons(shelfName,allButtons)
		cmds.deleteUI('Install Toolbox')
	except:
		pass


def AddIcons(shelfName,buttons):

	localScriptsPath = cmds.optionMenu('scriptsMenu', query=True,v=True) 
	localIconsPath = cmds.optionMenu('iconsMenu', query=True,v=True) 
	scriptsMenuI = cmds.optionMenu('scriptsMenu', query=True,sl=True)
	
	#resize progress bar
	cmds.progressBar('progressControl', edit=True,vis=True, maxValue=len(buttons)-1)

	#loop through dictionary
	for i, btn in enumerate(buttons):
		shelfElements = buttons[i]
		shelfString = 'cmds.shelfButton(rpt=True'
		#download icons from github
		try:
			icon = buttons[i]['icon']
			if isinstance(icon,basestring):
				icon = [icon]
			for ii,ico in enumerate(icon):
				if ico == 'separator':
					print 'seperator'
					shelfString = 'cmds.separator(style=\'shelf\',horizontal=0'
				else:
					#try to download file
					downloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/icons/'+ico), (localIconsPath+'/'+ico))
					if ii == 0:
						shelfString += ',i1=\''+ico+'\''  
		except:
			print ('file not available')
			#set icon to default button because image can not be downloaded
			shelfString += ',i1=\'commandButton.png\''
		#update progress
		cmds.progressBar('progressControl', edit=True, step=1)
		#download script from github
		if scriptsMenuI > 1:
			try:
				script = buttons[i]['script']

				downloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/'+script),(localScriptsPath+'/'+script))
				#DownloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/'+script),(localScriptsPath+'/'+fileName[-1]))
			except:
				print ('file not available')
		#download modules from github
		if scriptsMenuI > 1:
			try:
				modules = buttons[i]['modules']
				for mod in modules:

					downloadFile(('https://raw.githubusercontent.com/chrislyne/Toolbox/master/'+mod),'%s/%s'%(localScriptsPath,mod))
			except:
				print ('file not available')
		try:
			label = buttons[i]['label']
			shelfString += ',l=\''+label+'\''
		except:
			label = ''
		try:
			com = buttons[i]['command']
			shelfString += ',c=\''+com+'\''
		except:
			com = ''
		try:
			stp = buttons[i]['stp']
			shelfString += ',stp=\''+stp+'\''
		except:
			#shelfString += ',stp=\'mel\''
			print 'using mel'
		
		shelfString += ',w=32,h=32,p=\''+shelfName+'\')'
		
		#remove old button
		if label:
			RemoveButton(shelfName,label)

		#add icons to shelf
		currentButton = eval (shelfString)
		
		try:
			mi = buttons[i]['menuItem']
			for i,l in enumerate(mi):
				cmds.shelfButton(currentButton,edit=True,mi=(mi[i]['label'],mi[i]['command']))
		except:
			pass
	
def CheckText():

	shelfName = cmds.textField('nameText',q=True,text=True)

	checkGroups(shelfName)

def FilterOutSystemPaths(path):
	systemPath  = 0
	if path[0] == '/':
		systemPath = 1
	allparts = path.split('/')
	for part in allparts:
		if part == 'ProgramData' or  part == 'Program Files':
			systemPath = 1
	
	return systemPath

def browseForFile():
	filename = cmds.fileDialog2(fileMode=1, caption="Import Image")
	print filename
	cmds.textField('jsonPathText',e=True,tx=filename[0])
	updateGrpCheckboxes()
	#return filename

def updateGrpCheckboxes():
	try:
		children = cmds.columnLayout('listLayout',q=True,ca=True)
		for c in children:
			cmds.deleteUI(c)
	except:
		pass

	JSONPath = cmds.textField('jsonPathText',q=True,tx=True)

	try:
		data = json.load(open(JSONPath), object_pairs_hook=OrderedDict)
		cmds.textField('jsonPathText',e=True, text=JSONPath)
		cmds.setParent('listLayout')
		for k in data:
			cb = cmds.checkBox(h=20, label=k,v=1)
			try:
				if data[k]["checkStatus"] == 0:
					cmds.checkBox(cb, e=True,v=0)
				if data[k]["checkStatus"] == 2:
					cmds.checkBox(cb, e=True,v=1,ed=0)
			except:
				pass
	except:
		pass



def installToolboxWindow():
	installForm = cmds.formLayout()
	textLabel = cmds.text(label='Shelf')
	nameText = cmds.textField('nameText',width=250,tx='Custom')
	scriptsMenu = cmds.optionMenu('scriptsMenu')
	jsonPathText = cmds.textField('jsonPathText',width=250,ed=False,pht='path to json')
	jsonPathBtn = cmds.button('jsonPathBtn',width=50,label='...',c='browseForFile()')
	separator = ';' if cmds.about(nt=True) else ':'
	scriptsPaths = os.getenv('MAYA_SCRIPT_PATH')
	allparts = scriptsPaths.split(separator)
	for i, part in enumerate(allparts):
		if (i==0):
			cmds.menuItem( label='Manually install scripts' )
		if (i<7):
			isSystemPath = FilterOutSystemPaths(part)
			if (isSystemPath == 0):
				cmds.menuItem( label=part )
			
	iconsMenu = cmds.optionMenu('iconsMenu')  
	iconsPaths = os.getenv('XBMLANGPATH')
	iconsParts = iconsPaths.split(separator)
	
	for i, part in enumerate(iconsParts):
		if (i<6):
			isSystemPath = FilterOutSystemPaths(part)
			if (isSystemPath == 0):
				cmds.menuItem( label=part )

	progressControl = cmds.progressBar('progressControl',maxValue=10, vis=False, width=250)
	 
	btn1 = cmds.button(height=50,label='Install',c='CheckText()')
	btn2 = cmds.button(height=50,label='Close',c='cmds.deleteUI(\'Install Toolbox\')')

	listLayout = cmds.columnLayout('listLayout',adjustableColumn=True )

	try:
		dirname = os.path.dirname(__file__)
	except:
		print 'running in test environment'
		dirname = 'C:/Users/Admin/Documents/Toolbox'

	JSONPath = dirname+'/toolboxShelf.json'

	try:
		data = json.load(open(JSONPath), object_pairs_hook=OrderedDict)
		cmds.textField('jsonPathText',e=True, text=JSONPath)
		for k in data:
			cb = cmds.checkBox(h=20, label=k,v=1)
			try:
				if data[k]["checkStatus"] == 0:
					cmds.checkBox(cb, e=True,v=0)
				if data[k]["checkStatus"] == 2:
					cmds.checkBox(cb, e=True,v=1,ed=0)
			except:
				pass
	except:
		pass

	
	cmds.formLayout(installForm,  edit=True, 
					 attachForm=[
					 (textLabel, 'top', 15),
					 (textLabel, 'left', 10),
					 (nameText, 'top', 10),
					 (nameText, 'right', 10),
					 (scriptsMenu, 'right', 10),
					 (iconsMenu, 'right', 10),
					 (jsonPathBtn, 'right', 10),
					 (progressControl, 'left', 10),
					 (progressControl, 'right', 10),
					 (btn1, 'bottom', 0),
					 (btn1, 'left', 0),
					 (btn2, 'bottom', 0),
					 (btn2, 'right', 0)
					 ],
					 attachControl=[
					 (nameText, 'left', 10,textLabel),
					 (scriptsMenu, 'top', 10,textLabel),
					 (scriptsMenu, 'left', 10,textLabel),
					 (iconsMenu, 'top', 10,scriptsMenu),
					 (iconsMenu, 'left', 10,textLabel),
					 (jsonPathText, 'top', 10,iconsMenu),
					 (jsonPathBtn, 'top', 10,iconsMenu),
					 (jsonPathText, 'left', 10,textLabel),
					 (jsonPathText, 'right', 10,jsonPathBtn),
					 (progressControl, 'top', 20,jsonPathText),
					 (progressControl, 'left', 10,textLabel),
					 (listLayout, 'top', 20,jsonPathText),
					 (listLayout, 'left', 10,textLabel),
					 (btn2, 'left', 0,btn1)
					 ],
					 attachPosition=[
					 (btn1, 'right', 0, 50)
					 ]
					 )
					 
	shelfName = ''
	#get current tab
	names = cmds.layout('ShelfLayout',q=True,ca=True)
	shelfIndex = cmds.shelfTabLayout('ShelfLayout', query=True, selectTabIndex=True)
	
	#set text
	selectionString = (names[shelfIndex-1])
	cmds.textField(nameText,edit=True,tx=selectionString)


def toolbox_install():
	workspaceName = 'Install Toolbox'
	if(cmds.workspaceControl('Install Toolbox', exists=True)):
		cmds.deleteUI('Install Toolbox')
	cmds.workspaceControl(workspaceName,initialHeight=250,initialWidth=300,uiScript = 'installToolboxWindow()')


#toolbox_install()

#import installToolbox
#installToolbox.toolbox_install()