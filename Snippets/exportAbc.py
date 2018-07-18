#export alembic
def makeAlembic(refName, publishString):
    try: 
        #check if plug is already loaded
        if not cmds.pluginInfo('AbcExport',query=True,loaded=True):
            try:
                #load abcExport plugin
                cmds.loadPlugin( 'AbcExport' )
            except: cmds.error('Could not load AbcExport plugin')
        #make folder
        modelFolder = '%scache/alembic/models'%(cmds.workspace(q=True,rd=True))
        if not os.path.exists(modelFolder):
            os.makedirs(modelFolder)
        #export .abc
        command = '-frameRange 1 1 -attr material -attr alembicName -stripNamespaces -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa -root %s -file models/%s.abc'%(publishString,refName)
        cmds.AbcExport ( j=command )
        return '%s/%s.abc'%(modelFolder,refName)
    except:
        return 'unable to export .abc'