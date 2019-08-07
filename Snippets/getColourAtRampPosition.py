import maya.cmds as cmds

def colourAtPoint(rampData,point):
    rampList = rampData.split(',')

    def channelGrad(channel,point):
        
        channelDict = {'R':0,'G':1,'B':2}
        channelInt = channelDict[channel]
        
        cmds.optionVar(stringValue=['tempRChannelOptVar', '%s,%s,1'%(rampList[channelInt],rampList[3])])
    
        positions = rampList[3::5]
        for i,c in enumerate(positions[1:]):
            cmds.optionVar(stringValueAppend=['tempRChannelOptVar', '%s,%s,1'%(rampList[channelInt::5][i+1],c)])
        
        tempGrad = cmds.gradientControlNoAttr(h=90,m=False)
        cmds.gradientControlNoAttr(tempGrad, e=True, optionVar='tempRChannelOptVar' )
        
        channelValue = cmds.gradientControlNoAttr(tempGrad, q=True, valueAtPoint=point )
        cmds.deleteUI(tempGrad, control=True )
        return channelValue
    
    R = channelGrad('R',point)
    G = channelGrad('G',point)
    B = channelGrad('B',point)
    
    return('(%s,%s,%s)'%(R,G,B))

rampData = '0,0,0,1,1,0.5,0,0,0,1,1,0,1,0.5,1'
print colourAtPoint(rampData,0.1)
