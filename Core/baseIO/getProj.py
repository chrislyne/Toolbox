import maya.cmds as cmds 

def getProject():
	proj = cmds.workspace( q=True, directory=True, rd=True)
	return proj

def filepath():
	filename = cmds.file( query=True, sceneName=True)
	return filename

def sceneFolder():
	folder = filepath().rsplit('/',1)[0]
	return folder

def sceneFile():
	file = filepath().rsplit('/',1)[-1]
	return file

def sceneName():
	name = sceneFile().split('.')[0]
	return name
	
