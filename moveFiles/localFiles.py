from shutil import copyfile
import os
import json

def copyFiles(sourceFiles,destinationPath):

	finalDst = []
	#make folder
	if not os.path.exists(destinationPath):
		os.makedirs(destinationPath)
	#copy files
	for f in sourceFiles:
		dst = '%s/%s'%(destinationPath,f.split('/')[-1])
		copyfile(f, dst)
		finalDst.append(dst)
	return finalDst

#copyFiles(['C:/Users/Chris/Dropbox/Projects/Backpack/Sorted/Product/can01.abc'],'C:/Users/Chris/Dropbox/Projects/Backpack/Sorted/Product/new')

def loadJSON(f):
    with open(f) as data_file:    
        data = json.load(data_file)
    return data

def loadDictionary(f):
    try:
        #look for existing dictionary
        prefDict = loadJSON(f)
    except:
        #create new dictionary if it can't find one
        prefDict = {}
    return prefDict

def savePrefs(userDict,jsonFileName):
	#find path
	prefPath = jsonFileName.rsplit('/',1)[0]
	#make folder
	if not os.path.exists(prefPath):
			os.makedirs(prefPath)
	#write json to disk
	existingDict = loadDictionary(jsonFileName)
	#merge existing file with new dictionary data
	mergedDict = {k: dict(existingDict.get(k, {}), **userDict.get(k, {})) for k in existingDict.viewkeys() | userDict.viewkeys()}
	#write data to disk
	with open(jsonFileName, mode='w') as feedsjson:
		json.dump(mergedDict, feedsjson, indent=4, sort_keys=True)


