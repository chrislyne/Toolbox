import maya.cmds as cmds

#list of joints to create
baseJoints = [
	{"name":"face_joint_GRP","type":"group"},
	{"name":"headAnchor_joint","type":"joint"}
	] #manditory joints
mouthJoints = [
	{"name":"mouth_joint_GRP","type":"group"},
	{"name":"lipBottom_joint","type":"joint"},
	{"name":"lipTop_joint","type":"joint"},
	{"name":"lipTop_R_joint","type":"joint"},
	{"name":"lipBottom_R_joint","type":"joint"},
	{"name":"lipCorner_R_joint","type":"joint"}
	] #mouth joints
eyebrowJoints = [
	{"name":"eyebrow_joint_GRP","type":"group"},
	{"name":"eyebrowCenter_joint","type":"joint"},
	{"name":"eyebrowInside_R_joint","type":"joint"},
	{"name":"eyebrowMiddle_R_joint","type":"joint"},
	{"name":"eyebrowOutside_R_joint","type":"joint"}
	] #eyebrow joints
eyelidJoints = [
	{"name":"eyelid_joint_GRP","type":"group"},
	{"name":"eyelidTop_R_joint","type":"joint"},
	{"name":"eyelidBottom_R_joint","type":"joint"}
	] #eyelid joints
cheekJoints = [
	{"name":"cheek_joint_GRP","type":"group"},
	{"name":"cheek_R_joint","type":"joint"}
	] #cheek joints
cheekBoneJoints = [
	{"name":"cheekBone_joint_GRP","type":"group"},
	{"name":"cheekBone_inside_R_joint"},
	{"name":"cheekBone_center_R_joint"},
	{"name":"cheekBone_outside_R_joint"}
	] #cheekbone joints
noseJoints = [
	{"name":"nose_joint_GRP","type":"group"},
	{"name":"nose_joint","type":"joint","p":"nose_joint_GRP"},
	{"name":"noseTip_joint","type":"joint","p":"nose_joint_GRP"},
	{"name":"nostral_R_joint","type":"joint","p":"nose_joint_GRP"}
	] #nose joints

jointDict = baseJoints + mouthJoints + eyebrowJoints + eyelidJoints + cheekJoints + cheekBoneJoints + noseJoints

for j in jointDict: #loop through joint list
	if 'type' in j:
		if j['type'] == "joint":
			newJoint = cmds.joint(n=j['name']) #create joint
		if j['type'] == "group":
			cmds.group(n=j['name'],em=True) #create group
	if 'p' in j: 
		cmds.parent(newJoint,j["p"]) #parent object

	cmds.select(clear=True) #clear selection
