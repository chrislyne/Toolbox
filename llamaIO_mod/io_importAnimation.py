def io_importAnimation():

    #import dialog
    proc string SelectedABC()
    {
        string $basicFilter = "*.abc";
        string $result[] = `fileDialog2 -fm 1 -fileFilter $basicFilter -dialogStyle 2`;
        return $result[0];
    }
    
    #split path
    string $abcPath = SelectedABC();
    string $parts[];
    $numTokens = `tokenize $abcPath "/" $parts`;
    string $filename = $parts[(`size $parts`-1)];
    string $fileParts[];
    $numTokens2 = `tokenize $filename "." $fileParts`;
    string $filename2 = $fileParts[0];
    //create top level group
    select -cl;
    if (`objExists |GEO` == 0)
    {
        string $newRootGroup = `group -em -n "GEO"`;
    }
    //create file group
    string $newGroup = `group -em -n $filename2`;
    parent $newGroup |GEO;
    string $importFiles = `AbcImport -mode import -reparent $newGroup $abcPath`;
    
    #remove curves
    
    #remove empty groups
}

def importAnim(filename):
        command = "AbcImport -mode import \""+filename+"\""; 
        mel.eval(command)
        setupSceneFromCam()

def importAnimDialog():
    myWorkspace = cmds.workspace( q=True, fullName=True )
    myAlembics = myWorkspace+'/cache/alembic'
    filename = cmds.fileDialog2(fileMode=1, dir=myAlembics, caption="Import Camera")
    #import camera
    if (filename):
        importAnim(filename[0])

abc_importAnimation();