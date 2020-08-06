import maya.cmds as cmds

#list of joints to create
baseJoints = [
	{"name":"face_joint_GRP","type":"group"},
	{"name":"headAnchor_joint","type":"joint","p":"face_joint_GRP","l":"headAnchor"}
	] #manditory joints
mouthJoints = [
	{"name":"mouth_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"jaw_joint","type":"joint","p":"mouth_joint_GRP"},
	{"name":"jawEnd_joint","type":"joint","p":"jaw_joint"},
	{"name":"lipBottom_joint","type":"joint","p":"mouth_joint_GRP"},
	{"name":"lipTop_joint","type":"joint","p":"mouth_joint_GRP"},
	{"name":"lipTop_R_joint","type":"joint","p":"mouth_joint_GRP"},
	{"name":"lipBottom_R_joint","type":"joint","p":"mouth_joint_GRP"},
	{"name":"lipCorner_R_joint","type":"joint","p":"mouth_joint_GRP"}
	] #mouth joints
eyebrowJoints = [
	{"name":"eyebrow_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"eyebrowCenter_joint","type":"joint","p":"eyebrow_joint_GRP"},
	{"name":"eyebrowInside_R_joint","type":"joint","p":"eyebrow_joint_GRP"},
	{"name":"eyebrowMiddle_R_joint","type":"joint","p":"eyebrow_joint_GRP"},
	{"name":"eyebrowOutside_R_joint","type":"joint","p":"eyebrow_joint_GRP"}
	] #eyebrow joints
eyelidJoints = [
	{"name":"eyelid_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"eyelidTop_R_joint","type":"joint","p":"eyelid_joint_GRP"},
	{"name":"eyelidBottom_R_joint","type":"joint","p":"eyelid_joint_GRP"}
	] #eyelid joints
cheekJoints = [
	{"name":"cheek_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"cheek_R_joint","type":"joint","p":"cheek_joint_GRP"}
	] #cheek joints
cheekBoneJoints = [
	{"name":"cheekBone_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"cheekBone_inside_R_joint","type":"joint","p":"cheekBone_joint_GRP"},
	{"name":"cheekBone_center_R_joint","type":"joint","p":"cheekBone_joint_GRP"},
	{"name":"cheekBone_outside_R_joint","type":"joint","p":"cheekBone_joint_GRP"}
	] #cheekbone joints
noseJoints = [
	{"name":"nose_joint_GRP","type":"group","p":"face_joint_GRP"},
	{"name":"nose_joint","type":"joint","p":"nose_joint_GRP"},
	{"name":"noseTip_joint","type":"joint","p":"nose_joint_GRP"},
	{"name":"nostral_R_joint","type":"joint","p":"nose_joint_GRP"}
	] #nose joints

jointDict = baseJoints + mouthJoints + eyebrowJoints + eyelidJoints + cheekJoints + cheekBoneJoints + noseJoints

for j in jointDict: #loop through joint list
	if 'type' in j:
		if j['type'] == "joint":
			newObj = cmds.joint(n=j['name']) #create joint
			#setAttr "headAnchor_joint.type" 18;
		if j['type'] == "group":
			newObj = cmds.group(n=j['name'],em=True) #create group
	if 'p' in j: 
		cmds.parent(newObj,j["p"]) #parent object

	cmds.select(clear=True) #clear selection
