import json

def loadJSON(f):
    with open(f) as data_file:    
        data = json.load(data_file)    
    return data
    
globalData = loadJSON('C:/Users/Chris/Dropbox/Projects/Qt/globalPrefs.json')
print globalData
for o in globalData:
    print globalData[o]
    try:
        for v in globalData[o]:
            for i in v:
                pass
    except:
        pass

#update in dictionary
globalData['text1'] = [{u'setText': u'man'}]

#write out to json file
with open('C:/Users/Chris/Dropbox/Projects/Qt/localPrefs.json', mode='w') as feedsjson:
    json.dump(globalData, feedsjson)



