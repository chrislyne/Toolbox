#remove namespace
def removeSceneNamespaces():
    #set current namespace to root
    cmds.namespace(':',set=True)
    #list namespaces in scene
    allNamespaces = cmds.namespaceInfo(lon=True)
    while (len(allNamespaces) > 2):
        #list namespaces in scene again 
        allNamespaces = cmds.namespaceInfo(lon=True)
        for item in allNamespaces:
            namespaceName = ':' + item
            #make sure to avoid critical namespaces
            if namespaceName != ':UI' and namespaceName != ':shared':
                #empty and remove namespace
                cmds.namespace(f=True,mv=(namespaceName,':'))
                cmds.namespace(rm=namespaceName)