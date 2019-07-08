cmds.select('shoulder_guideJoint_L',r=True)
cmds.select('elbow_guideJoint_L',add=True)
cmds.select('wrist_guideJoint_L',add=True)

#AUTO RIG NOODLE LIMB
#
#
import maya.cmds as cmds

def midpoint(p1,p2):
    #return midpoint 
    m1 = []
    m1.append((p1[0] + p2[0])/2)
    m1.append((p1[1] + p2[1])/2)
    m1.append((p1[2] + p2[2])/2)
    return m1
    
def createJoints(jointType,lockMidJoints):
    newJoints = []
    for i,j in enumerate(guideJoints):
        #get joint position
        jPos = cmds.xform(j,q=True,t=True,ws=True)
    
        if guideJoints[i-1] and i > 0:
            #create midpoint joint
            mjPos = midpoint(jPos,cmds.xform(guideJoints[i-1],q=True,t=True,ws=True))
            newJointName = guideJoints[i-1].replace('_guide','Mid_%s'%jointType)
            newJoint = cmds.joint(n=newJointName,p=[mjPos[0],mjPos[1],mjPos[2]])
            newJoints.append(newJoint)
            #lock mid joints
            if lockMidJoints == 1:
                 cmds.setAttr('%s.rx'%newJoint,lock=True)
                 cmds.setAttr('%s.ry'%newJoint,lock=True)
                 cmds.setAttr('%s.rz'%newJoint,lock=True)
        #create new joint
        newJointName = j.replace('guide',jointType)
        newJoint = cmds.joint(n=newJointName,p=[jPos[0],jPos[1],jPos[2]])
        newJoints.append(newJoint)
    return newJoints
    
def locatorChild(obj,hierarchy):
    #create locator
    newLocator = cmds.spaceLocator(n='%s_LOC'%obj)
    #position and parent locator to obj
    pPos = cmds.xform(obj,q=True,piv=True,ws=True)
    cmds.move(pPos[0],pPos[1],pPos[2],newLocator,ws=True)
    if hierarchy:
        cmds.parent(newLocator[0],obj)
    return newLocator[0]

def createPlusCtrl(pos):
    #make circle
    ctrl = cmds.circle(r=0.3,s=12,ut=0,d=1,ch=0,sw=360,tol=0.01)
    cmds.xform(ctrl,ro=[0,0,15],t=pos)
    #shape plus
    cvs = ['%s.cv[1]'%ctrl[0],'%s.cv[10]'%ctrl[0],'%s.cv[7]'%ctrl[0],'%s.cv[4]'%ctrl[0]]
    cmds.scale(0.361464,0.361464,0.361464,cvs,r=True,) 
    #freeze position
    cmds.makeIdentity(ctrl,apply=True,t=1,r=1,s=1)
    
    return ctrl

#list joints
guideJoints = cmds.ls(sl=True)

cmds.select(cl=True)
blendJoints = createJoints('blend',0)
cmds.select(cl=True)
fkJoints = createJoints('FK',1)
cmds.select(cl=True)
ikJoints = createJoints('IK',1)
cmds.select(cl=True)
bendJoints = createJoints('bend',0)

curvePoints = []
for i,j in enumerate(blendJoints):
    cmds.parentConstraint(fkJoints[i],ikJoints[i],j)
    jPos = cmds.xform(j,q=True,t=True,ws=True)
    curvePoints.append(tuple(jPos))

#create controller
ikjPos = cmds.xform(ikJoints[-1],q=True,t=True,ws=True)
newIKControl = cmds.circle(n='IK_CTRL_L',ch=0,r=0.3)
cmds.xform(newIKControl,t=ikjPos,ws=True)
cmds.makeIdentity(newIKControl,apply=True,t=1)
#create IK handle 
newIkHandle = cmds.ikHandle(sj=ikJoints[0],ee=ikJoints[-1])
cmds.parent(newIkHandle[0],newIKControl)


#create distance
startLoc = locatorChild(ikJoints[0],0)
endLoc = locatorChild(newIKControl[0],1)
distanceNode = cmds.shadingNode('distanceBetween',asUtility=True)
cmds.connectAttr('%s.worldPosition[0]'%startLoc,'%s.point1'%distanceNode)
cmds.connectAttr('%s.worldPosition[0]'%endLoc,'%s.point2'%distanceNode)
#math nodes
multNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.connectAttr('%s.distance'%distanceNode,'%s.input1X'%multNode)
cmds.setAttr('%s.operation'%multNode,2)
restDistance = 0
for i,j in enumerate(ikJoints):
    if i > 0:
        restDistance += cmds.getAttr('%s.translateX'%j)
cmds.setAttr('%s.input2X'%multNode,restDistance)

condishNode = cmds.shadingNode('condition',asUtility=True)
cmds.connectAttr('%s.distance'%distanceNode,'%s.firstTerm'%condishNode)
cmds.connectAttr('%s.input2X'%multNode,'%s.secondTerm'%condishNode)
cmds.setAttr('%s.operation'%condishNode,2)
cmds.connectAttr('%s.outputX'%multNode,'%s.colorIfTrueR'%condishNode)


#create curve
ikCurve = cmds.curve(d=3,p=curvePoints,n='ikSpline_curve')
#attach joints
ikSplineHandle = cmds.ikHandle(sj=bendJoints[0], ee=bendJoints[-1],c=ikCurve,sol='ikSplineSolver',ccv=False,pcv=False,n='ikSpline_handle')
splineMultNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.setAttr('%s.operation'%splineMultNode,2)
cmds.setAttr('%s.input2X'%splineMultNode,cmds.arclen(ikCurve))
curveInfoNode = cmds.arclen(ikCurve, ch=True)
cmds.connectAttr('%s.arcLength'%curveInfoNode,'%s.input1X'%splineMultNode)

for i,j in enumerate(bendJoints):
    if i < len(bendJoints)-1:
        cmds.connectAttr('%s.outputX'%splineMultNode,'%s.scaleX'%j)

#get curve cvs
curveCVs = cmds.ls('{0}.cv[:]'.format(ikCurve), fl=True)
#create clusters
for i,cv in enumerate(curveCVs):
    newCluster = cmds.cluster(cv)
    cPos = cmds.xform(newCluster[1],q=True,piv=True,ws=True)
    bendCtrl = cmds.circle(n='bend_CTRL_L',ch=0,r=0.3)
    cmds.xform(bendCtrl,ro=[0,-90,0])
    cmds.makeIdentity(apply=True,r=True)
    bendCtrlGrp = cmds.group(bendCtrl,n='bend_CTRL_GRP_L')
    cmds.xform(bendCtrlGrp,t=[cPos[0],cPos[1],cPos[2]],ws=True)
    cmds.makeIdentity(bendCtrlGrp,apply=True,t=1)
    cmds.parent(newCluster[1],'%s|%s'%(bendCtrlGrp,bendCtrl[0]))
    cmds.parentConstraint(blendJoints[i],bendCtrlGrp,mo=True)
    

for i,j in enumerate(ikJoints):
    if i < len(ikJoints)-1:
        cmds.connectAttr('%s.outColorR'%condishNode,'%s.scaleX'%j)

fkIkCtrl = createPlusCtrl([1,1,1])