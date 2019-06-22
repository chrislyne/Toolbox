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
    extentionType = ''
    extra = ''
    jobID = ''

    #check what to do
    if sim == 1: 
        extra = '-UsageLimit 1 -DistributeMode \"Forward\"'
        #set variables on bifrost nodes
        #turn mesh off
        #turn evaluate on
        #evaluation type to simulation
        #clear all cache variables

        #save file
        cmds.file(rename='%s%s'%(filename.rsplit('.',1)[0],extentionType))
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
        cmds.file(rename='%s%s'%(filename.rsplit('.',1)[0],extentionType))
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



global proc SmedgeBifrostCache()
{
    if (`window -exists submitBifrostWindow`) deleteUI submitBifrostWindow;
    window -w 200 -h 200 -title "Bifrost Submit Window"  submitBifrostWindow;
        formLayout submitBifrostForm;
            text -label "Packets" -w 100 textLabel1;
            text -label "Priority" -w 100 textLabel2;
            intSliderGrp -field true -minValue 1 -maxValue 1000 -fieldMinValue 1 -value 4 -w 200 slider1;
            intSliderGrp -field true -minValue 0 -maxValue 100 -fieldMinValue 0 -fieldMaxValue 100 -value 100 -w 200 slider2;
            checkBox -label "Sim" -w 100 check3;
            checkBox -label "Mesh" -w 100 check1;
            checkBox -label "Foam" -w 100 check2;
            
            button -l "Submit" -h 50 -c ("SubmitToSmedge();deleteUI submitBifrostWindow")  Btn1;
            button -l "Close" -h 50 -c ("deleteUI submitBifrostWindow")  Btn2 ;
        formLayout  -edit
                    -af check1 top 20 
                    -af check1 left 70
                    -ac check2 top 10 check1
                    -af check2 left 70 
                    -ac check3 top 10 check2
                    -af check3 left 70 
                    -ac slider1 top 72 check3
                    -af slider1 left 70
                    -ac slider2 top 102 check3
                    -af slider2 left 70 
                    -af textLabel1 left -12 
                    -ac textLabel1 top -18 slider1
                    -af textLabel2 left -12 
                    -ac textLabel2 top -20 slider2
                    -af Btn1 bottom 0
                    -af Btn1 left 0
                    -ap Btn1 right 0 50
                    -af Btn2 bottom 0
                    -ac Btn2 left 0 Btn1
                    -af Btn2 right 0 

    submitBifrostForm;
    showWindow submitBifrostWindow;
}
//SmedgeBifrostCache();