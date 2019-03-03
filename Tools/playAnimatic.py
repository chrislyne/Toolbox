from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time

# path to the directory 
myWorkspace = cmds.workspace( q=True, fullName=True )
jobFolder = myWorkspace.rsplit('/',1)[0]
dirpath = '%s/output/animatic'%jobFolder

# get all entries in the directory w/ stats
entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))

os.startfile(sorted(entries)[-1][1])


