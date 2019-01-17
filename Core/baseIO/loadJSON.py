import json

def loadJSON(f):
    with open(f) as data_file:    
        data = json.load(data_file)
    
    return data


