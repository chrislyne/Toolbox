#creates .xgen files when they don't auto create
#
import maya.cmds as cmds
#list connections
xgnodes = cmds.ls(type='xgmPalette')
#create .xgen for each collection
for n in xgnodes:
	#get scene name
    filepath = cmds.file(q=True, sn=True)
    #name .xgen file
    xgenpath = "%s__%s.xgen"%(filepath.rsplit('.',1)[0],n)
    #write .xgen file
    xg.exportPalette(n.encode('utf8'),xgenpath.encode('utf8'))




