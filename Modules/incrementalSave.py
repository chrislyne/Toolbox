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
        initialless = simpleSplit(item, '_', -1)
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
    #check if filename has version
    if ((words[-1].replace("v", "")).isdigit()):
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
    foundMatch = 0
    newName = candidate
    for i in allFiles:
        if candidate == i:
            foundMatch = 1
            j = CreateCandidate(i)
            CompareCandidate(j,allFiles,folder,initials)
            newName = j
    if (foundMatch == 0):
        
        intitialsExt = ''
        if len(initials) > 0:
            intitialsExt = '_'+initials
        
        fullNewName = (folder+'/'+newName+intitialsExt+'.mb')
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

#IncrementCurrentFile(initials='cl')







