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

sel = cmds.ls(sl=True)
tempDict = {}

sel = cmds.ls(sl=True)
tempDict = {}

for s in sel:
    nodeAtts = cmds.attributeInfo(s,all=True )
    nodeMulti = cmds.attributeInfo(s,m=True )
     
    nodeType = cmds.nodeType(s)
    attrDict = {s:{"attr":{},"nType":nodeType}}
    
    for a in nodeMulti:
        children = cmds.attributeQuery( a, node=s,listChildren=True)
        if children:
            print children
            value = cmds.getAttr('%s.%s'%(s,a),multiIndices=True)
            print value
            for i,v in enumerate(value):
                print cmds.getAttr('%s.%s[%s].position'%(s,a,i))
                print cmds.getAttr('%s.%s[%s].colorR'%(s,a,i))
                print cmds.getAttr('%s.%s[%s].colorG'%(s,a,i))
                print cmds.getAttr('%s.%s[%s].colorB'%(s,a,i))
    
    for a in nodeAtts:
        try:
            value = cmds.getAttr('%s.%s'%(s,a))
            defaultValue = cmds.attributeQuery( a, node=s,ld=True)
            if len(defaultValue) == 1:
                defaultValue = defaultValue[0]
            elif len(defaultValue) > 1:
                defaultValue = [tuple(defaultValue)]
                
            if value != defaultValue:
                attrDict[s]['attr'][a] = value
        except:
            pass
    tempDict.update(attrDict)

print tempDict


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
            cmds.setAttr('%s.%s'%(newShader,k),tempDict[key]['attr'][k])
        except:
            pass
	

