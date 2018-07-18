import maya.cmds as cmds
import os, sys, time

def sortFaceShadingGroups(shape,shadingGrp):
    print 'shape = %s\n'%(shape)
    #find transform
    transform = cmds.listRelatives(shape,p=True,type='transform')
    #list all objects in set
    allObjects = cmds.sets( shadingGrp, q=True )
    
    faces = []
    #search set for matching shapes 
    for obj in allObjects:
        splitObj = obj.split('.')
        if len(splitObj) > 1:
            if splitObj[0] == transform[0]:
                faces.append(splitObj[1])
    #return faces assign to material
    return faces

#write to shader database
def WriteToDB(filename,log,mode):
    scenePath = os.path.split(os.path.abspath(filename))
    folderPath = scenePath[0]+'/'
    fileName = scenePath[1].split('.')[0]
    logFileName = folderPath+fileName+'.json'
    text_file = open(logFileName, mode)
    text_file.write(log)
    text_file.close()


def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')

#publish shaders
def exportShaders(publishName,scenePath):

    #initalise variables 
    allGeo = ""
    allMaterials = []
    data = '{\n "shapes":['
    
    #select hierarchy
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True )
    allDecendingShapes = cmds.ls(allDecending,s=True,l=True)
    
    #loop though if they have materials
    for i,shape in enumerate(allDecendingShapes):
        shadingGroups = cmds.listConnections(shape,type='shadingEngine')
        if shadingGroups:
            allGeo += '-root %s '%(shape)
            allMaterials += shadingGroups
            #remove duplicates from list
            shadingGroups = list(set(shadingGroups))
            
            #add attributes to shape nodes
            addAttribute(shape,'alembicName',publishName)
            addAttribute(shape,'material',shadingGroups)
            ID = cmds.ls(shape,uuid=True)
            addAttribute(shape,'IOID',ID[0])
            
            shadingGrpsString = ''
            #garbagy json formattring
            for n,shadingGrp in enumerate(shadingGroups):
                faces = ''
                allFaces = sortFaceShadingGroups(shape,shadingGrp)
                for c,f in enumerate(allFaces):
                    if c > 0:
                        faces += '","'
                    faces += '.%s'%(f)
                if n > 0:
                    shadingGrpsString += ',\n               '
                shadingGrpsString +=  '{\n              "%s":["%s"]\n               }'%(shadingGrp,faces)
            if i > 0:
                data += ','
            data += '\n     {\n     "%s":\n         {\n         "material": [\n             %s\n            ]\n         }\n     }'%(ID[0],shadingGrpsString)
    data += '\n ]\n}'  
    #write connections out to text file    
    WriteToDB(scenePath,data,'w')
    #materials used in our hierachy    
    allMaterials = list(set(allMaterials))  
    
    #log
    shaderCount = 0
    
    #get workspace
    workspace = cmds.workspace(q=True,fullName=True)
    
    for material in allMaterials:
        #process namespaces
        materialFilename = material.replace(':', '_')
        #export material
        cmds.select(material,r=True,noExpand=True)  
        cmds.file('%s/renderData/alembicShaders/%s/%s_%s.mb'%(workspace,publishName,publishName,materialFilename),force=True,typ='mayaBinary',pr=True,es=True)
        
        #increment to log
        shaderCount += 1

    return shaderCount
    
exportShaders('dog','C:/Users/Chris/Documents/maya/projects/default/renderData/alembicShaders/dog/dog_v001_cl.mb')    