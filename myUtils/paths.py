import os
import platform

def userPrefsPath():

	if platform.system() == "Windows":
		prefPath = os.path.expanduser('~/maya/prefs')
	else:
		prefPath = os.path.expanduser('~/Library/Preferences/Autodesk/Maya/prefs')
	return prefPath


	