import json
import os

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

def writePrefsToFile(prefData,prefFile):
    #[object,command,value]

    #make folder
    folder = prefFile.rsplit('/',1)[0]
    if not os.path.exists(folder):
        os.makedirs(folder)

    prefDict = loadDictionary(prefFile)
    #update in dictionary
    for pref in prefData:
        prefDict[pref[0]] = [{pref[1]:pref[2]}]
    
    #write out to json file
    with open(prefFile, mode='w') as feedsjson:
        json.dump(prefDict, feedsjson, indent=4, sort_keys=True)

#writePrefsToFile([['object1','command','value1'],['object2','command','value2']]'C:/Users/Chris/Dropbox/Projects/Qt/localPrefs.json')

