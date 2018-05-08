from pymel.core import *
for item in resourceManager(nameFilter='*'):
    try:
        #Make sure the folder exists before attempting.
        resourceManager(saveAs=(item, "C:/temp/icons/{0}".format(item)))    
    except:
        #For the cases in which some files do not work for windows, name formatting wise. I'm looking at you 'http:'!
        print item