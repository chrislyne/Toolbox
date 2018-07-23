import maya.cmds as cmds

def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')

#return connections from transforms to specific node types
def connectedNodes():
    connections = []
    ctrlObjects = []
    additionalAttributes = []
    nodeTypes = ['file','place2dTexture','animCurveUU','expression','noise']
    for nType in nodeTypes:
        nodes = cmds.ls(typ=nType)
        for node in nodes:
            
            #not sure what this is, maybe some kind of garbagy error check
            if(node != "<done>"):
                connectedNodes = cmds.listConnections(node,t='transform',plugs=True,c=True,d=False,s=True)
                if connectedNodes:  
                    #print connectedNodes                  
                    #disconnect the nodes
                    inputs = connectedNodes[0::2]
                    outputs = connectedNodes[1::2]
                    for i,item in enumerate(outputs):
                        c = [outputs[i],inputs[i]]
                        cmds.disconnectAttr (c[0],c[1])
                        connections.append(c)
                        ctrlObjects.append(c[0].split('.')[0])
                        

                #additional attributes to add to export
                #plug = connectedNodes[1].split('.')
                #additionalAttributes.append(plug[1]) 
                    
                #addAttribute(connectedNodes[1].split('.')[0],'connections',connections)  
    ctrlObjects = set(ctrlObjects) 
    for ctrlObj in ctrlObjects:
        addAttribute(ctrlObj,'connections','')
    print ctrlObjects 
    #print connections
    #return (connections)

connectedNodes()