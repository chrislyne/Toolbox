import maya.cmds as cmds

def getRenderLayers():
	#returns render layers and their states
	renderlayers = cmds.ls(type="renderLayer")
	'''
	filter out extra legacy and default render layers
	'''
	layerData = []
	for layer in renderlayers:

		if ':defaultRenderLayer' in layer:
			print 'skipping %s'%layer
		elif '_defaultRenderLayer' in layer:
			print 'skipping %s'%layer
		else:
		    renderable = cmds.getAttr('%s.renderable'%layer)
		    layerData.append([layer,renderable])

	return layerData

def getStartFrame():
	startFrame = cmds.playbackOptions(q=True,min=True )
	startFrameStr = str('{0:g}'.format(startFrame))
	return str(startFrameStr)

def getEndFrame():
	endFrame = cmds.playbackOptions(q=True,max=True )
	endFrameStr = str('{0:g}'.format(endFrame))
	return str(endFrameStr)