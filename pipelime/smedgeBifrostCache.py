import os
import maya.cmds as cmds
import subprocess

def submitToSmedge(packetSize,priority,sim,foam,mesh):

    #Query values from UI

    submit = 'C:/Program Files/Smedge/Submit.exe'
    dir = submit.rsplit('/',1)[0]

    #set the working dir and PATH to the directory
    os.chdir(dir)
    os.putenv("PATH",dir)
    #now set submit to just the basename of the executable
    submit = submit.rsplit('/',1)[1]

    #get start and end frames from timeline
    startFrameFloat = cmds.playbackOptions(q=True,minTime=True)
    startFrame = str('{0:g}'.format(startFrameFloat))
    endFrameFloat = cmds.playbackOptions(q=True,maxTime=True)
    endFrame = str('{0:g}'.format(endFrameFloat))

    #set naming
    filename = cmds.file(q=True,sn=True)
    shortname = cmds.file(q=True,sn=True,shn=True)
    smedgeName = 'bifrost: %s'%shortname.split('.')[0]
    extra = ''
    jobID = ''

    #mesh cache
    cmds.setAttr('%s.liquidmeshCacheControl'%bifrostLiquidContainer,0)
    cmds.setAttr('%s.enableLiquidMeshCache'%bifrostLiquidContainer,0)
    cmds.setAttr('%s.liquidmeshCachePath'%bifrostLiquidContainer,'',type="string")
    cmds.setAttr('%s.liquidmeshCacheFileName'%bifrostLiquidContainer,'',type="string")

    #check what to do
    if sim == 1: 
        extra = '-UsageLimit 1 -DistributeMode \"Forward\"'
        #clear cache inputs
        if mesh == 1:
            #liquid cache
            cmds.setAttr('%s.enableLiquidCache'%bifrostLiquidContainer,0)
            cmds.setAttr('%s.liquidCacheControl'%bifrostLiquidContainer,0)
            cmds.setAttr('%s.liquidCachePath'%bifrostLiquidContainer,'',type="string")
            cmds.setAttr('%s.liquidCacheFileName'%bifrostLiquidContainer,'',type="string")
            #solid cache
            cmds.setAttr('%s.enableSolidCache'%bifrostLiquidContainer,0)
            cmds.setAttr('%s.solidCacheControl'%bifrostLiquidContainer,0)
            cmds.setAttr('%s.solidCachePath'%bifrostLiquidContainer,'',type="string")
            cmds.setAttr('%s.solidCacheFileName'%bifrostLiquidContainer,'',type="string")
        
        #set variables on bifrost nodes
        #turn mesh off
        #turn evaluate on
        #evaluation type to simulation
        #clear all cache variables

        #save file
        cmds.file(rename='%s.sim'%(filename.rsplit('.',1)[0]))
        cmds.file(save=True)
        #submit string
        cmd = '%s Script -Type \"Generic Script\" -Name \"%s - SIM\" -Priority %s %s -Pool \"Redshift\" -ErrorStarts \"Failed\" -Range \"%s-%s\" -PacketSize %s -Command \\\"C:\\Program Files\\Autodesk\\Maya2019\\bin\\mayabatch.exe\\\" \\\"%s.sim.mb\\\" \\\"-command\\\" \\\"MeshBifrost($(SubRange.Start),$(SubRange.End),%s,%s,%s)\\\"'%(submit,smedgeName,priority,extra,startFrame,endFrame,packetSize,filename.rsplit('.',1)[0],sim,foam,mesh)
        print cmd
        #do it
        jobID = subprocess.check_output(cmd,stdin=None,stderr=None,shell=False)
        print jobID.split(' ')[-1]
        
    if mesh == 1: 
        extra = '-WaitForJobID %s -WaitForWholeJob 0'%jobID.split(' ')[-1]
        if sim == 1:
            print 'wait for sim to finish'
            #extra = 'wait for sim to finish'
        cmds.file(rename='%s.mesh'%(filename.rsplit('.',1)[0]))
        cmds.file(save=True)
        #submit string
        cmd = '%s Script -Type \"Generic Script\" -Paused -Name \"%s - MESH\" -Priority %s %s -Pool \"Redshift\" -ErrorStarts \"Failed\" -Range \"%s-%s\" -PacketSize %s -Command \\\"C:\\Program Files\\Autodesk\\Maya2019\\bin\\mayabatch.exe\\\" \\\"%s.mesh.mb\\\" \\\"-command\\\" \\\"MeshBifrost($(SubRange.Start),$(SubRange.End),%s,%s,%s)\\\"'%(submit,smedgeName,priority,extra,startFrame,endFrame,packetSize,filename.rsplit('.',1)[0],sim,foam,mesh)
        print cmd
        #do it
        result = subprocess.check_output(cmd,stdin=None,stderr=None,shell=False)

    #set filename back      
    cmds.file(rename=filename) 
    cmds.file(save=True)

submitToSmedge(4,100,1,0,1)
