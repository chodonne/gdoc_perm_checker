#!/usr/bin/python

from __future__ import print_function
import httplib2
import os
import sys

from ConfigParser import SafeConfigParser

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from apiclient import errors

import pprint
# ...


#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = '~/.credentials/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def retrieve_permissions(service, file_id):
    """Retrieve a list of permissions.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve permissions for.
    Returns:
    List of permissions.
    """
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        return permissions.get('items', [])
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)
    return None

def retrieve_document_title(service, file_id):
    """Retrieve the title of the document.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve the title for.
    Returns:
    The title of the document
    """
    try:
        filemetadata = service.files().get(fileId=file_id).execute()
        return filemetadata['title']
    except errors.HttpError, error:
        print ('An error occured: %s' % error)
    return None

def retrieve_document_parents(service, file_id):
    # Call my parents! Call my parents! Call my parents! *stomp* *stomp* *stomp*
    """Retrieve the parents of the document.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve the parents for
    Returns:
    List of parents
    """
    try:
        filemetadata = service.files().get(fileId=file_id).execute()
        return filemetadata['parents']
    except errors.HttpError, error:
        print ('An error occured: %s' % error)
    return None

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """

    pp = pprint.PrettyPrinter(indent=4)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
	
    parser = SafeConfigParser()
    parser.read("DriveConfig.INI")

    # Get our list of file IDs to check, either form the config file or from the command line arguments.

    fileids = [];


    if (len(sys.argv) > 1):
        argumentlist = sys.argv[1:]
        for fileid in argumentlist:
            fileids.append(fileid)
        
    else:
        for section in parser.sections(): # Fix this later.
            for name,value in parser.items(section):
                if name == "url":
                    fileids.append(value)


    for fileid in fileids:
        title = retrieve_document_title(service, fileid);
        print("Document Title: " + title);
        perm_list = retrieve_permissions(service, fileid)
        parents = retrieve_document_parents(service, fileid)
        #print("Parents: " + str(parents))
        for entry in perm_list:
            if type(entry) is dict:
                print("  " + entry['role'] + ":  " + entry['emailAddress']);
	

if __name__ == '__main__':
    main()
