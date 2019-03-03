import maya.cmds as cmds
import maya.mel as mel
import os, sys

## Get filename
def GetFilename(short):
    filename = cmds.file( query=True, sceneName=True ,shortName=short)
    return filename

## Remove initals and version number
def simpleSplit(s, c, n):
    words = s.split(c)
    return c.join(words[:n])


## list other files in directory
def ListAllFiles():
    removeFilename = GetFilename(False).rsplit('/', 1)
    files = os.listdir(removeFilename[0])
    allinitialless = []
    for item in files:
        #check for initials
        end = item.split('_')[-1]
        if any(char.isdigit() for char in end):
            initialless = item.rsplit('.',1)[0]
        else:
            initialless = item.rsplit('_',1)[0]
        versionless = simpleSplit(initialless, '_', -1)
        allinitialless.append (initialless)
    return allinitialless

#################################
##  Increment Current version  ##
#################################

import re

## Get filename
def GetFilename(short):
    filename = cmds.file( query=True, sceneName=True ,shortName=short)
    return filename

## Remove initals
def RemoveInitials(s, c, n):
    words = s.split(c)
    name = c.join(words)
    #check if filename has initials
    if (words[-1].isalpha()):
        name = c.join(words[:n])
    return name
    
## Remove version
def RemoveVersion(s, c, n):
    words = s.split(c)
    name = c.join(words)
    version = words[-1].lower()
    #check if filename has version
    if ((version.replace("v", "")).isdigit()):
        name = c.join(words[:n])
    return name

## Returns the current version
def CurrentVersion(filename):
    version = '0'
    # check if version exists
    if any(char.isdigit() for char in filename):
        removeLetters = re.sub('[a-z]*\.?[a-zA-Z]', "", filename)
        while (removeLetters[-1] == '_'):
            removeLetters = removeLetters[:-1]
        
        splitNumbers = removeLetters.split('_')
        version = splitNumbers[-1]
    return version

## Increments the 'CurrentVersion' and returns the next version
def NextVersionAsString(filename):
    versionString = (CurrentVersion(filename))
    nextVersion = int(versionString)+1
    nextVersionString = str(nextVersion)
    
    while len(nextVersionString) < 3:
        nextVersionString = '0'+nextVersionString
    return nextVersionString

def CreateCandidate(filename):

    initialless = RemoveInitials(filename, '_', -1)
    versionless = RemoveVersion(initialless, '_', -1)
    candidate = (versionless+'_v'+NextVersionAsString(initialless))
    return candidate

def CompareCandidate(candidate,allFiles,folder,initials):
    nextCandidate = candidate
    success = False
    
    while success == False:
        foundMatch = False
        for f in allFiles:
            if nextCandidate == f:
                foundMatch = True
                nextCandidate = CreateCandidate(f)

        if foundMatch == False:
            success = True
            break
     
    if (success == True):
        
        intitialsExt = ''
        if len(initials) > 0:
            intitialsExt = '_'+initials
        
        fullNewName = (folder+'/'+nextCandidate+intitialsExt+'.mb')
        cmds.file(rename=fullNewName)
        cmds.file( save=True )

def IncrementCurrentFile(**keyword_parameters):
    fullFilename = GetFilename(False).rsplit('/', 1)
    folder =  fullFilename[0]
    filename = fullFilename[-1]
    removeExtention = RemoveInitials(filename, '.', -1)
    
    candidate = CreateCandidate(removeExtention)
    
    allFiles = ListAllFiles()
    
    initials = ''
    if ('initials' in keyword_parameters):
        initials=keyword_parameters['initials']
    
    CompareCandidate(candidate,allFiles,folder,initials)

#IncrementCurrentFile()







