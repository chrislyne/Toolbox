#return connections from transforms to specific node types
def connectedNodes():
    connections = []
    additionalAttributes = []
    nodeTypes = ['file','place2dTexture','animCurveUU','expression']
    for nType in nodeTypes:
        nodes = cmds.ls(typ=nType)
        for node in nodes:
            #not sure what this is, maybe some kind of garbagy error check
            if(node != "<done>"):
                connectedNodes = cmds.listConnections(node,t='transform',plugs=True,c=True,d=False,s=True)
                if connectedNodes:
                    connections.append(connectedNodes)
                    #additional attributes to add to export
                    plug = connectedNodes[1].split('.')
                    additionalAttributes.append(plug[1])   

    return (connections,additionalAttributes)