#export animation

def publishFile(path):

    #get workspace
    workspace = cmds.workspace( q=True, directory=True, rd=True)

    #get filename
    filename = cmds.file(q=True,sn=True)

    #get relative path
    relativePath = ''
    for( $i=$workspaceSize; $i<(`size $buffer`-1); ++$i ):

        relativePath += ($buffer[$i]+"/");

    #published file name
    string $publishName = "alembicTestSphere";
    
    exportString = ''
    sel = cmds.ls(sl=True)
    for item in sel:
        exportString += ' -root %s'%(item)
    #get timeline
    startFrame = cmds.playbackOptions(q=True,minTime=True)
    endFrame = cmds.playbackOptions(q=True,maxTime=True)
    
    folderPath = '%s/cache/alembic/%s'%(workspace,relativePath)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    #check if plug is already loaded
    if not cmds.pluginInfo('AbcImport',query=True,loaded=True):
        try:
            #load abcExport plugin
            cmds.loadPlugin( 'AbcImport' )
        except: cmds.error('Could not load AbcImport plugin')

        #export .abc
        additionalAttr = ''
        #IO attributes
        additionalAttributes = ['alembicName','IOID']
        #redshift attributes
        additionalAttributes += ['rsObjectId','rsEnableSubdivision','rsMaxTessellationSubdivs','rsDoSmoothSubdivision','rsMinTessellationLength','rsOutOfFrustumTessellationFactor','rsEnableDisplacement','rsMaxDisplacement','rsDisplacementScale']
        for attr in additionalAttributes:
            additionalAttr += ' -attr %s'%(attr)
        command = '-verbose -j ("-frameRange "+$startFrame+" "+$endFrame+" -attr material -attr alembicName -attr rsEnableSubdivision -attr rsMaxTessellationSubdivs -attr rsEnableDisplacement -attr rsMaxDisplacement -attr rsDisplacementScale -attr rsObjectId -attr castsShadows -attr receiveShadows -attr holdOut -attr primaryVisibility -attr smoothShading -attr visibleInReflections -attr visibleInRefractions -attr doubleSided -attr opposite -attr HeadAccessories -attr characterCreation -attr HairColour -attr skinColour -attr shoes -attr pants -attr sleeves -attr HeadAccessories -attr PantsColour -attr SleaveColour -attr ShoeColour -attr hatColour -attr TieColour -attr shoeColour -attr hairColour -attr SkinColour -attr Hair -attr Tie -attr Pants -attr Shoes -attr attribute -attr plug -ro -uvWrite -writeVisibility -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa"+$exportString+" -file \""+$workspace+"/cache/alembic/"+$relativePath+"/"+$path+".abc\"")'
        cmds.AbcExport ( j=command )

//update name and run
global proc CheckText()
{
   $prefixString = `textField -q -text prefixText`;
   $nameString = `textField -q -text nameText`;
   $publishName = ($prefixString+"_"+$nameString);
   publishFile($publishName);
}

global proc io_exportAnimation()
{
    if (`window -exists abcAnimationExportWindow`) deleteUI abcAnimationExportWindow;
    window -w 300 -h 100 -title "abc Animation Export Window" abcAnimationExportWindow;
        formLayout dauzerForm;
             text -label "Prefix" prefixLabel;
             textField -w 250 prefixText;
             text -label "Publish Name" textLabel;
             textField -w 250 nameText;
             button -l "Publish" -h 50 -c ("CheckText()") dauzerButton1;
             button -l "Close" -h 50 -c ("deleteUI abcAnimationExportWindow") dauzerButton2 ;
        formLayout -edit
             -af prefixLabel top 15
             -af prefixLabel left 10 
             -af prefixText top 10
             -ac prefixText left 10 textLabel
             -af prefixText right 10 
             -af textLabel top 45
             -af textLabel left 10 
             -af nameText top 40
             -ac nameText left 10 textLabel
             -af nameText right 10 
             -af dauzerButton1 bottom 0
             -af dauzerButton1 left 0
             -ap dauzerButton1 right 0 50
             -af dauzerButton2 bottom 0
             -ac dauzerButton2 left 0 dauzerButton1
             -af dauzerButton2 right 0 

    dauzerForm;
    string $publishName = "";
    
    //get filename
    string $filename = `file -q -sn -shn`;
    string $buffer[];
    $numTokens = `tokenize $filename "." $buffer`;
    
    //set text
    string $sel[] = `ls -sl`;
    string $selectionString = "";
    for ($item in $sel)
    {
        string $fullNameSplit[];
        $numTokens = `tokenize $item ":" $fullNameSplit`;
        int $size = (`size $fullNameSplit`)-1;
        $selectionString += (($fullNameSplit[$size]));
    }
    textField -edit -tx ($buffer[0]) prefixText;
    textField -edit -tx ($selectionString) nameText;
    showWindow abcAnimationExportWindow;
}
io_exportAnimation();