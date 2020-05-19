# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:19:43 2020

@author: Gavin Leavitt
"""

from __future__ import print_function
from googleapiclient import discovery
from apiclient.http import MediaIoBaseDownload
from httplib2 import Http
#Import just the error for exception handling!
from httplib2 import ServerNotFoundError
from oauth2client import file, client, tools
import time
import datetime
import io
import csv
import psycopg2
import zulu
import queryDB as queryDB
import script_config as config

####Active functions####

def connectPOSTGRESSQL():
    """
    
    Creates a database session by connecting to postgressql database using psycopg2.
    
    Consider setting variables and creating a external file to hold
    login information
    
    Parameters:
        None
    Returns:
        Connection instance
    """
    connection = psycopg2.connect(dbname=config.settings["dbname"], port=config.settings["port"], user=config.settings["user"],
                                  password=config.settings["password"], host=config.settings["host"])
    return connection

def setGoogleDriveScopes():
    """
    Set scope for script to connect to Google Drive resouces and return a connection to Google Drive API, currently allows readonly access to everything.
    
    This gives read only access to all files, still not clear on how to change scopes properly,
    I believe that the "storage.json" file has to be deleted and the script ran again to generate a new one
    see: https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#7
    
    Parameters:
        None
    Returns:
        Google Drive API Connection: Connection to Google Drive API with read-only access.
    
    """
    SCOPES = config.settings["scope"]
    #Windows:
    #store = file.Storage(r'B:\VMs\OSGeoLive_Shared\GoogleAPI\storage.json')
    #Ubuntu:
    store = file.Storage(config.settings["store"])
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(config.settings["flow"], SCOPES)
        creds = tools.run_flow(flow, store)
    #Builds the drive API connection so I can send requests
    drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return drive

def setInitialToken():
    """
    Gets the intitial state of the entire Google Drive account for change tracking.
    
    This value is compared against and gets changed in the changePolling function for further change tracking.
    
    Returns:
        Token: Initial state of Google Drive Account
    """
    startToken = drive.changes().getStartPageToken().execute()
    startTokenValue = startToken.get('startPageToken')
    return startTokenValue

def changePolling(pageToken,disconnect_timer,sleeptimer):
    """
    Polls Google Drive GPS folder for changes, if changes occur then downloads, processes, then inserts data into POSTGRES Database. 
    
    Google Drive account is polled every (sleeptimer) seconds for changes, once a change is detected the function determines if it was within the
    GPS folder, if so, a copy of the file is downloaded as a CSV then parsed. The GPS coordinates are extracted and parsed into SQL requests
    to the POSTGRES databse

    
    Parameters:
        pageToken: State of entire Google Drive account, initialized then updated by function.
        disconnect_timer(int): Retrys changePolling if a ServerNotFoundError is thrown when attempting to poll Google Drive API.
        sleeptimer(int): Wait time after polling to poll again.
    """
    while pageToken is not None:
        print("\nPolling Google API!")
        #Get the list of changes from the drive using the token as comparison
        try:
            response = drive.changes().list(pageToken=pageToken,spaces='drive').execute()
        except Exception as error:
            print (f"\nError:{error}\nFailed to interface with Google Drive API, internet may be down, waiting {disconnect_timer} seconds to try again!\n")
            time.sleep(disconnect_timer)
            continue
            
        #Iterate over list of changes getting values
        for change in response.get('changes'):
            #Get ID of changed file(s)
            changeFileId = change.get('fileId')
            #for some reason files are supposed to save as .csv but end up as google sheets with .csv on end,
            #need to strip .csv off filename
            changeFileName = change.get('file')['name'].strip('.csv')
            #Get parent folder of change file using its fileid (never changes even if filename does)
            parent = drive.files().get(fileId=changeFileId,fields = 'parents').execute()
            print (f'Change found for a file, file name is: {changeFileName} and its fileID is: {changeFileId}')         
            #Check to see if the parent is the GPS folder, is so do operations
            if fileid in parent['parents']:
                print("This is a change in a GPS file!")
                #Get file name of changed  for naming export
                changeFileName = change.get('file')['name']
                #Determine if a file was deleted, might use info later
                changeRemovedBol = change.get('removed')
                #Get file change time
                changeTime = change.get('time') 
                #Get file type
                changeFileType = change.get('file')['mimeType']
                #Exports Google sheet file
                csvLoc = export_file_local(changeFileId,changeFileName)
                #Pass csv location processing function
                csvDat = csvProcessing(csvLoc)
                print("All done downloading and reading CSV, passing to data processing!")
                #Take coordinates and append as a postgres POINT geometry type for SQL queries
                coordinate = "POINT({0} {1})".format(csvDat[2],csvDat[1])
                coordinate = [coordinate]             
                query_results = queryDB.queryDB(coordinate,conn,POI_Outdoors)
                insDat = dataAppend(csvDat,query_results,coordinate)
                print("Finished processing data and querying database, inserting data!")
                insertData(insDat)
                print("Data inserted in database!")
            else:
                print("\n Change elsehwere in Google Drive account, generating new page token! \n")
        if 'newStartPageToken' in response:
            # Last page, save this token for the next polling interval, becomes new token to compare against
            pageToken = response.get('newStartPageToken')
            print (f"New start token is: {pageToken}")
        #Determine if there is more data to get, if so a new token is generated
        #not sure if this will work as is to get the changes on the next loop
        if 'nextPageToken' in response:
            print("More info to be gathered!")
            pageToken = response.get('nextPageToken')
        print(f'End of polling interval and waiting for {sleeptimer} seconds! \n')
        time.sleep(sleeptimer)

def export_file_local(file_id,filename):
    """Downloads a google sheets file and saves as a local csv, if the file is large it will
    chunk out the download
    returns the saved file full location
    """
    mime = 'text/csv'
    request = drive.files().export_media(fileId=file_id,mimeType=mime)
    fileEXT = '.csv'
    #Windows:
    #fileSavePathway = r'B:\VMs\OSGeoLive_Shared\GoogleAPI\GPSSaveLocation'
    #Ubuntu:
    fileSavePathway = config.settings["fileSavePathway"]
    fullSave = fileSavePathway + '/' + filename + fileEXT
    fh = io.FileIO(fullSave, 'wb') 
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    print(f"File saved too: {fullSave}")
    return fullSave 

def csvProcessing(csvLoc):
    """ 
    Opens local csv and parses data, returning the last(most recent) row of data
    as a list.
    
    Parameters:
        csvloc
    Returns:
            
    """
    gpsDict = {}
    with open(csvLoc, 'r') as csvfile:
        csvReader = csv.reader(csvfile)
        counter = 0
        #Create dictonary of all values in CSV with the key autoincrementing
        for row in csvReader:
            #Header row
            if counter == 0:
                #headers = row[0:-1]
                counter += 1
                #print(headers)
            elif counter > 0:
                #print(row[0:-1])
                rowdata = row[0:-1]
                gpsDict[counter] = rowdata
                counter += 1
        #Most recent record        
        csvDatRecent = gpsDict[counter-1]
        return csvDatRecent

def dateTimeLocal(csvTime):
    """
    Converts from zulu time to local time. 
    
    Not sure if it handles PST vs PDT, will have to check.
    
    """
    dt = zulu.parse(csvTime)
    pacific = dt.astimezone(config.settings["timezone"])
    localTime = pacific.strftime('%Y-%m-%d %I:%M %p %Z')
    return localTime

def dataAppend(csvDat, query_results,coordinate):
    """
    Merges and parses csv data with database query results. 
        
    Parameters
    ----------
    csvDat : TYPE
        DESCRIPTION.
    query_results : TYPE
        DESCRIPTION.

    Returns
    -------
    List of data to be inserted into POSTGRES
    
    """
    #Append other data into list
    csvDat.append(phone)   
    #insert time
    csvDat.append(str(datetime.datetime.now()))
    #Convert to local time
    csvDat.append(dateTimeLocal(csvDat[0]))        
    values = []
    for i in query_results.keys():
        if i not in ["Road","Trail"]:
          values.append(query_results[i])
        else:
            values.append(query_results[i][0])
            values.append(query_results[i][1])
            
    csvDat.extend(values)
    csvDat.extend(coordinate)
    #Replace all '' with None to avoid data type errors, PostGres/psycopg2 don't like empty string inputs    
    csvDat = [None if i == '' else i for i in csvDat]   
    return csvDat

def fileinfo():
    pass    

def insertData(insDat):
    """ Inserts data into the gpsdata table in postgres """
       
    #New way, see: https://stackoverflow.com/questions/6117646/insert-into-and-string-concatenation-with-python
    #https://stackoverflow.com/questions/45624693/can-i-use-a-postgresql-postgis-function-in-a-insert-code-in-psycopg2-python
    #Using geomfromtext, see: https://postgis.net/docs/ST_GeomFromText.html
    #Make a cursor for inputting into table
    cur = conn.cursor()
    sql = '''
    INSERT INTO gpsdata (gpstime, lat, lon, elevation, accuracy, bearing, speed, satellites, provider, hdop, vdop, pdop, geoidheight, 
                         ageofdgpsdata, dgpsid, activity, battery, phone, inserttime, gpstimelocal, poi, city, county,
                          trail, dist_nearesttrail, road, dist_nearestroad, geom)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))'''

    print(insDat)
    print(len(insDat))
    #insDat = insDat[-2:]
    cur.execute(sql, insDat)
    #commit changes to DB
    conn.commit()
    print ("Data inserted and commited to Postgres database!")

def updateData():
    pass

def selectDat():
    """
    Selects youngest, most recent record, based on inserted time
    """
    recentSQL = ''' SELECT ID FROM gpsdata ORDER BY time desc LIMIT 1 '''
    cur_sel = conn.cursor()
    cur_sel.execute(recentSQL)
    records = cur_sel.fetchall()
    print(records)       

def movementStatus(csvDatRecent,csvDatPrev):
    """
    Use current and previous coordinates to determine current movement status
    returns a string of status: moving or stationary, and distance moved as int
    """
    #Check if there is > 1 records, if so calculate differences between records
    #TODO: Make a function to calculate information such as status
    pass
    # if len(gpsDict) > 1:
    #     csvDatPrev = gpsDict[counter-2]
    #     moveStatus = movementStatus(csvDatRecent,csvDatPrev)
    # else:
    #     pass

def locationStatus():
    """
    Use current location to query POSTGRESSQL.
    Returns current location and possible activity such as:
    home, at work, driving, on a walk/run, on a bike ride, resting on a bike ride, etc.         
    """
    pass
    
"""
TODO: Create function to read csv/dict and calculate data from previous to most recent record
"""    
        
####Active functions####  

#Connect to MTB postgres database on Ubuntu Server
conn = connectPOSTGRESSQL()


##Variables
#POIs
POI_Outdoors = config.settings["POI_Outdoors"]
#GPS folder fileid, all GPS files are uploaded to here
fileid = config.settings["fileid"]
#list query to get files in GPS folder
query = f"'{fileid}' in parents"
#phone submitting data
phone = config.settings["phone"]
#Process sleep timers for polling and exceptions
sleeptimer = 5
disconnect_timer = 60

###Kick off script####
while True:
    try:
        #Connect to API and set scopes
        drive = setGoogleDriveScopes()
        #Initial start token to compare against, retrieved on script opening 
        startTokenValue = setInitialToken()
        break
    except Exception as error:
        print (f"\nError:{error}\nFailed to interface with Google Drive API, internet may be down, waiting {disconnect_timer} seconds to try again!\n")
        time.sleep(disconnect_timer)
        continue

print (f"Start token is: {startTokenValue}")
#Poll change list to see if start token has changed, kicking off with initial token
#Keep start token seperate, might use this info later. 
pageToken = startTokenValue
changePolling(pageToken,disconnect_timer,sleeptimer)

  