import maya.cmds as cmds

def makeJoints():
	#list of joints to create
	baseJoints = [
		{"name":"face_joint_GRP","type":"group"},
		{"name":"headAnchor_joint","type":"joint","p":"face_joint_GRP","l":"headAnchor","colorIndex":7}
		] #manditory joints
	mouthJoints = [
		{"name":"mouth_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"jaw_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":2},
		{"name":"jawEnd_joint","type":"joint","p":"jaw_joint","colorIndex":2},
		{"name":"lipBottom_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":2},
		{"name":"lipTop_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":2},
		{"name":"lipTop_R_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":1},
		{"name":"lipBottom_R_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":1},
		{"name":"lipCorner_R_joint","type":"joint","p":"mouth_joint_GRP","colorIndex":1}
		] #mouth joints
	eyebrowJoints = [
		{"name":"eyebrow_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"eyebrowCenter_joint","type":"joint","p":"eyebrow_joint_GRP","colorIndex":2},
		{"name":"eyebrowInside_R_joint","type":"joint","p":"eyebrow_joint_GRP","colorIndex":1},
		{"name":"eyebrowMiddle_R_joint","type":"joint","p":"eyebrow_joint_GRP","colorIndex":1},
		{"name":"eyebrowOutside_R_joint","type":"joint","p":"eyebrow_joint_GRP","colorIndex":1}
		] #eyebrow joints
	eyelidJoints = [
		{"name":"eyelid_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"eyelidTop_R_joint","type":"joint","p":"eyelid_joint_GRP","colorIndex":1},
		{"name":"eyelidBottom_R_joint","type":"joint","p":"eyelid_joint_GRP","colorIndex":1}
		] #eyelid joints
	cheekJoints = [
		{"name":"cheek_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"cheek_R_joint","type":"joint","p":"cheek_joint_GRP","colorIndex":1}
		] #cheek joints
	cheekBoneJoints = [
		{"name":"cheekBone_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"cheekBoneInside_R_joint","type":"joint","p":"cheekBone_joint_GRP","colorIndex":1},
		{"name":"cheekBoneCenter_R_joint","type":"joint","p":"cheekBone_joint_GRP","colorIndex":1},
		{"name":"cheekBoneOutside_R_joint","type":"joint","p":"cheekBone_joint_GRP","colorIndex":1}
		] #cheekbone joints
	noseJoints = [
		{"name":"nose_joint_GRP","type":"group","p":"face_joint_GRP"},
		{"name":"nose_joint","type":"joint","p":"nose_joint_GRP","colorIndex":2},
		{"name":"noseTip_joint","type":"joint","p":"nose_joint_GRP","colorIndex":2},
		{"name":"nostral_R_joint","type":"joint","p":"nose_joint_GRP","colorIndex":1}
		] #nose joints

	jointDict = baseJoints + mouthJoints + eyebrowJoints + eyelidJoints + cheekJoints + cheekBoneJoints + noseJoints

	for j in jointDict: #loop through joint list
		if 'type' in j:
			if j['type'] == "joint":
				newObj = cmds.joint(n=j['name']) #create joint
				cmds.setAttr("%s.type"%newObj,18) #set joint type
				cmds.setAttr("%s.otherType"%newObj, j['name'].split('_')[0],type="string") #set "otherType" name
				if j['name'].split('_')[1] == 'R':
					cmds.setAttr("%s.side"%newObj,2) #set label side to 'Right'
				if 'colorIndex' in j:
					cmds.color(ud=j['colorIndex'])
			if j['type'] == "group":
				newObj = cmds.group(n=j['name'],em=True) #create group

		if 'p' in j: 
			cmds.parent(newObj,j["p"]) #parent object

		cmds.select(clear=True) #clear selection

def mirrorJoints():
	sel = cmds.ls(sl=True) #joint selection
	for j in sel: #loop through selected joints
	    mj = cmds.mirrorJoint(j,mirrorYZ=True, searchReplace=["_R","_L"]); #mirror the joint
	    mj = mj[0] #redefine result as string using the first object
	    ry = cmds.getAttr("%s.rotateY"%mj) #get rotate Y
	    rz = cmds.getAttr("%s.rotateZ"%mj) #get rotate Z
	    cmds.setAttr("%s.rotateY"%mj,ry*-1) #correct Y rotation
	    cmds.setAttr("%s.rotateZ"%mj,rz*-1) #correct Z rotation
	    cmds.setAttr("%s.side"%mj, 1) #set joint label side to "Left" 
	    cmds.color(mj,ud=6) #change joint colour
