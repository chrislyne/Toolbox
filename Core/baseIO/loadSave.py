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
    #prefData = [object,key,value],[object,key,value]

    #make folder
    folder = prefFile.rsplit('/',1)[0]
    if not os.path.exists(folder):
        os.makedirs(folder)

    prefDict = loadDictionary(prefFile)
    #update in dictionary
    for pref in prefData:
        if pref[0] in prefDict:
            d = prefDict[pref[0]]
            if pref[1] in d:
                prefDict[pref[0]][pref[1]] = pref[2]
            else: 
                d.update({pref[1]:pref[2]})
        else:  
            prefDict[pref[0]] = {pref[1]:pref[2]}
    
    #write out to json file
    with open(prefFile, mode='w') as feedsjson:
        json.dump(prefDict, feedsjson, indent=4, sort_keys=True)

#writePrefsToFile([['object1','c4','value7'],['object1','test','value5'],['object2','c4','value6']],'C:/Users/Chris/Dropbox/Projects/test.json')

