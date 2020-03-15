import maya.cmds as cmds

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
            newShader = cmds.shadingNode(tempDict[key]['nType'],asShader=True )
        elif nodeClass == 'utility':
            newShader = cmds.shadingNode(tempDict[key]['nType'],asUtility=True )
        elif nodeClass == 'texture':
            newShader = cmds.shadingNode(tempDict[key]['nType'],asTexture=True )

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
shaderNetwork = shaderNetworkToDict(sel)
print shaderNetwork
dictToShaderNetwork(shaderNetwork)

