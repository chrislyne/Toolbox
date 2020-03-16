import maya.cmds as cmds

def makeConnections(nodes_attr,ns):

    source = nodes_attr[0].split('.',1)
    dest = nodes_attr[1].split('.',1)
    if cmds.attributeQuery( source[1], node=source[0],exists=True) and cmds.attributeQuery( dest[1], node=dest[0],exists=True):
        cmds.connectAttr( '%s:%s'%(ns,nodes_attr[0]), '%s:%s'%(ns,nodes_attr[1]) )

def createNewNamespace(ns):
    #create a clean operating namespace
    
    #set to root namespace
    cmds.namespace( set=':' )
    #delete namespace if it already exists
    if cmds.namespace( exists=ns ):
        cmds.namespace( rm=ns,mnp=True )
    #make new namespace and set
    newNamespace = cmds.namespace( add=ns )
    cmds.namespace( set=':%s'%ns )
    
    return newNamespace

def removeNamespace(ns):
    cmds.namespace( set=':' )
    if cmds.namespace( exists=ns ):
        cmds.namespace( rm=ns,mnp=True )

def getNodeClassType(nodeType):
    #get type of node 
    #nodeType = cmds.nodeType(node)
    nodeClass = ''
    #list of shading nodes
    nodeClasses = ['utility','shader','texture']
    #find type of class
    for c in nodeClasses:
        if cmds.getClassification(nodeType,satisfies=c):
            nodeClass = c
    
    return nodeClass

def listShadingNodes(objects):
    #list ALL of the objects shape nodes
    allShapes = []
    for o in objects:
        shapes = cmds.listRelatives( o, allDescendents=True,type='shape')
        allShapes += shapes
    
    for shape in allShapes:
        #find connected shading networks
        con = cmds.listConnections( shape, scn=True, type='shadingEngine' )
        #remove duplicate materials  
        allMaterials = cmds.listConnections( shape, scn=True, type='shadingEngine' )
        allConnections = []
        allNodes = list(set(con))
        #add objects back into the list while it's being iterated 
        for m in allNodes:
            materials = cmds.listConnections( m, source=True,scn=True,destination=False,plugs=True)
            
            if materials:
                for matConnection in materials:
                    mat = matConnection.split('.')[0]
                    #add recursive shading nodes to the list
                    nodeType = cmds.nodeType(mat)
                    nodeClass = getNodeClassType(nodeType)
                    if any(nodeClass in s for s in ['utility','shader','texture',]) and nodeClass:
                        allNodes.append(mat)
                        destinations = cmds.connectionInfo(matConnection, destinationFromSource=True)
                        matching = [x for x in destinations if m in x]
                        for mDest in matching:
                            allConnections.append('%s,%s'%(matConnection,mDest))
                        allMaterials.append(mat)
        return (list(set(allMaterials)),list(set(allConnections)))

def shaderNetworkToDict(sel):

    tempDict = {}

    for s in sel:
        nodeAtts = cmds.attributeInfo(s,all=True )
        nodeMulti = cmds.attributeInfo(s,m=True )
        nodeType = cmds.nodeType(s)
        attrDict = {s:{"attr":{},"nType":nodeType}}
        if nodeMulti:
            for a in nodeMulti:
                children = cmds.attributeQuery( a, node=s,listChildren=True)
                if children:

                    value = cmds.getAttr('%s.%s'%(s,a),multiIndices=True)
                    if value:
                        for v in value:
                            for child in children:
                                childAttr = '%s[%s].%s'%(a,v,child)
                                childAttrValue = cmds.getAttr('%s.%s[%s].%s'%(s,a,v,child))
                                nodeAtts.append('%s[%s].%s'%(a,v,child))
        
        for a in nodeAtts:
            try:
                value = cmds.getAttr('%s.%s'%(s,a))
                if cmds.attributeQuery( a, node=s,ex=True):
                    defaultValue = cmds.attributeQuery( a, node=s,ld=True)

                    if defaultValue == None and isinstance(value, basestring):
                        pass
                    elif len(defaultValue) == 1:
                        defaultValue = defaultValue[0]
                    elif len(defaultValue) > 1:
                        defaultValue = [tuple(defaultValue)]

                else:
                    #force attributes without defaults to the dictionary 
                    defaultValue = ''

                if value != defaultValue:
                    #remove tuple from list
                    if isinstance(value, list):
                        value = tuple(value[0])
                    #add attr to attrDict
                    
                    attrDict[s]['attr'][a] = value
            except:
                pass
        tempDict.update(attrDict)

    return tempDict

def dictToShaderNetwork(tempDict):
    #build new shader
    for key in tempDict:
        nodeClass = getNodeClassType(tempDict[key]['nType'])
        if nodeClass == 'shader':
            newShader = cmds.shadingNode(tempDict[key]['nType'],asShader=True ,name=key)
        elif nodeClass == 'utility':
            newShader = cmds.shadingNode(tempDict[key]['nType'],asUtility=True ,name=key)
        elif nodeClass == 'texture':
            newShader = cmds.shadingNode(tempDict[key]['nType'],asTexture=True ,name=key)
        elif tempDict[key]['nType'] == 'shadingEngine':
            newShader = cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name=key)

        for k in tempDict[key]['attr']:
                try:
                #if not cmds.attributeQuery( k, node=s,hidden=True):
                   
                    tValue = tempDict[key]['attr'][k]
                    #check if value is a tuple
                    if isinstance(tValue, tuple):
                        #set value as tuple
                        cmds.setAttr('%s.%s'%(newShader,k),tValue[0],tValue[1],tValue[2])
                        
                    elif isinstance(tValue, basestring):
                        cmds.setAttr('%s.%s'%(newShader,k),tValue,type='string')
                        
                    else:
                        #set value as float
                        cmds.setAttr('%s.%s'%(newShader,k),tValue)

                except:
                    pass    
    
sel = cmds.ls(sl=True)
materials,connections = listShadingNodes(sel)
shaderNetwork = shaderNetworkToDict(materials)
for key in shaderNetwork:
    print key
tempNs = createNewNamespace('temp_shader_namespace')
dictToShaderNetwork(shaderNetwork)



for c in connections:
    makeConnections(c.split(','),tempNs)


removeNamespace(tempNs)

