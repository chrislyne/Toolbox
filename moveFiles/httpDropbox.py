import httplib2
import urllib
import json

def uploadFileToDB(sourceFile,destinationFile,accessToken):
 
	http = httplib2.Http()
	payload=open(sourceFile,'r')
	 
	content = http.request('https://content.dropboxapi.com/2/files/upload', 
						   method="POST", 
						   headers={"Authorization": "Bearer %s"%accessToken, "Dropbox-API-Arg": "{\"path\": \"%s\",\"mode\": \"add\",\"autorename\": false,\"mute\": false,\"strict_conflict\": false}"%destinationFile,"Content-Type": "application/octet-stream"},
						   body=payload )[1]

#uploadFileToDB('C:/Users/Chris/Desktop/someFile.txt','/Homework/math/Matrices.txt','<access token>')


def listFiles(dbFolder,accessToken):
	http = httplib2.Http()
	payload="{\"path\": \"%s\",\"recursive\": false,\"include_media_info\": false,\"include_deleted\": false,\"include_has_explicit_shared_members\": false,\"include_mounted_folders\": true,\"include_non_downloadable_files\": false}"%dbFolder
 	#request db folder list
	content = http.request('https://api.dropboxapi.com/2/files/list_folder', 
					   method="POST", 
					   headers={"Authorization": "Bearer %s"%accessToken,"Content-Type": "application/json"},
					   body=payload )[1]

	#convert json data to dict
	folders = []
	contentDict = json.loads(content)
	for n in contentDict['entries']:
		folders.append(n['name'])

	return folders