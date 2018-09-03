"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import argparse
from apiclient.http import MediaFileUpload
import time
import io
from apiclient.http import MediaIoBaseDownload
# Setup the Drive v3 API

service = None

def login():
    global service
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store,flags)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    

def upload(fileName,parentID):
    index = fileName.rindex("/")
    ts = time.gmtime()
    simpleFile = fileName[index+1:]
    try:
        cut = simpleFile.index(".py")
        simpleFile = simpleFile[:cut]
    except:
        pass
    simpleFile += "_"+time.strftime("%Y-%m-%d", ts) + ".py"
    file_metadata = {'name': simpleFile,"parents":[parentID]}
    media = MediaFileUpload(fileName,
                            mimetype='file/py')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ("File ID:" + file.get('id'))
    if(file.get('id')):
        return True
    return False
def downloadTo(file_id,fileName):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(fileName, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

def download(id):
    folderID="'"+id+"'"
    query = "parents in " +folderID
    results = service.files().list( q= query,
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        toReturn = {}
        for item in items:
            toReturn[item['name'].encode("utf-8")] = item['id'].encode("utf-8")
            print('{0} ({1})'.format(item['name'], item['id']))
        return toReturn


