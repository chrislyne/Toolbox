import maya.cmds as cmds

def makeBlendshapes():
	sel = cmds.ls(sl=True) #select head geo
	baseBlend = cmds.duplicate(sel[0],n="head_base_blend") #duplicate out head for blend base
	channels = ["translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ"] #list of locked channels
	for c in channels: #loop through locked channels
	    cmds.setAttr("%s.%s"%(baseBlend[0],c),l=False) #unlock all channels
	bsGrp = cmds.group(em=True,n="blendShapes") #make blandshape group
	cmds.parent(baseBlend[0],bsGrp) #parent blendShape base to group
	shapes = ["mouth","eyebrow","eyeLid","cheek","cheekbone","nose","lipCurl"] #list of blendshapes
	for i,s in enumerate(shapes): #loop through blendshape list
	    newShape = cmds.duplicate(baseBlend[0],n="head_%s_blend"%s)[0] #make blendshape targets
	    if i==0: #first loop
	        blendShape = cmds.blendShape(newShape,baseBlend[0])[0] #make blendshape node and connect first target
	    else: #remaining loop
	        cmds.blendShape( blendShape, edit=True, t=(baseBlend[0], i, newShape, 1.0) ) #connect remaining blendshapes

makeBlendshapes()