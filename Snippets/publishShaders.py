import os, sys, time


#write to shader database
def WriteToDB(filename,log):
    filename = 'C:/Users/Chris/Documents/maya/projects/default/renderData/alembicShaders/dog/dog_v001_cl.mb'
    scenePath = os.path.split(os.path.abspath(filename))
    folderPath = scenePath[0]+'/'
    fileName = scenePath[1].split('.')[0]
    logFileName = folderPath+fileName+'.json'
    text_file = open(logFileName, 'a')
    text_file.write(log)
    text_file.close()


def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')

#publish shaders
def exportShaders(publishName):
    
    
    start = '{\n	"shapes":['
    WriteToDB('C:/Users/Chris/Documents/maya/projects/default/renderData/alembicShaders/dog/dog_v001_cl.mb',start)

    #initalise variables 
    allGeo = ""
    allMaterials = []
    
    #select hierarchy
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True )
    allDecendingShapes = cmds.ls(allDecending,s=True,l=True)
    
    #loop though if they have materials
    for shape in allDecendingShapes:
        shadingGroups = cmds.listConnections(shape,type='shadingEngine')
        if shadingGroups:
            allGeo += '-root %s '%(shape)
            allMaterials += shadingGroups
            
            #add attributes to shape nodes
            addAttribute(shape,'alembicName',publishName)
            addAttribute(shape,'material',shadingGroups)
            ID = cmds.ls(shape,uuid=True)
            addAttribute(shape,'IOID',ID[0])
            
            data = ',\n		{\n		"%s":\n			{\n			"material": [\n				"%s"\n			]\n			}\n		}'%(ID[0],shadingGroups[0])
            WriteToDB('C:/Users/Chris/Documents/maya/projects/default/renderData/alembicShaders/dog/dog_v001_cl.mb',data)

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
    
exportShaders('dog')    