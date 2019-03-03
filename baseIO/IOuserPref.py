import os
import json

def UserPrefPath():
    userMayaPath = os.environ.get('MAYA_APP_DIR')
    userMayaPrefsPath = userMayaPath+'/prefs'  
    userMayaPrefsFile = userMayaPrefsPath+'/IOUserPrefs.json'
    return userMayaPrefsFile

def SaveUserSettings(item):
    global userInitals
    userInitals = item
    userMayaPath = os.environ.get('MAYA_APP_DIR')
    userMayaPrefsPath = userMayaPath+'/prefs'
    if not os.path.exists(userMayaPrefsPath):
        os.makedirs(userMayaPrefsPath)
    
    userMayaPrefsFile = userMayaPrefsPath+'/IOUserPrefs.json'
    
    jsonText = '{\n    \"user\": {\n        \"initals\": \"'+item+'\"\n    }\n}'
    
    text_file = open(userMayaPrefsFile, "w")
    text_file.write(jsonText)
    text_file.close()   

def LoadUserSettings(filename):
    initials = ''
    if(os.path.exists(filename)):
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
                inputString = (data["user"]["initals"])
                initials = inputString
        except:
            cmds.error('could not parse '+filename+' try deleting it')
    else:
        print 'no file'

    return initials
