from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
# from settings import dbcon
from application.projects.water_quality.modelsWaterQual import beaches, waterQualityMD5, stateStandards, waterQuality
import pdfplumber
import unicodedata
from datetime import datetime
import hashlib
from urllib.parse import quote
from urllib.request import urlretrieve
from application import app, errorEmail, application
from application.projects.water_quality import GoogleDriveUploadWaterQuality
from application.projects.water_quality import DBQueriesWaterQuality
import os
from application import logger
from geojson import Point, Feature, FeatureCollection


# resampcol = ['Total Coliform Results (MPN*)', "Fecal Coliform Results (MPN*)", 'Enterococcus Results (MPN*)']

def handleBeaches():
    """
    Handles calling database water quality queries and function to generate geojson results.

    Returns
    -------
    geojson_res : geojson feature collection object
        Water quality test results as a geojson feature collection object. This contains geometry and properties
        of all queried records in a form that can be passed straight into Leaflet geojson.

    """
    # Call database query to get most recent test results
    beachResults = DBQueriesWaterQuality.getBeachWaterQual()
    # geojson_dump = dumps(waterQualGeoJSON(beach_results))
    mostRecent = recentRecord(beachResults)
    # Format results into geojson
    geojsonResult = getWaterQualGeoJSON(beachResults)
    return {"waterqual": geojsonResult, "recent": mostRecent}

def makeNull(beachDict):
    # for i in list(beachDict.keys()):
    #     for a in list(beachDict[i].keys()):
    #         if not beachDict[i][a]:
    #             beachDict[i][a] = None
    for i in list(beachDict.keys()):
        if not beachDict[i]["Total Coliform Results (MPN*)"]:
            beachDict.pop(i, None)

def recentRecord(records):
    maxRec = 0
    for i in records:
        recdate = datetime.strptime(str(i.waterQuality.hash_rel.insdate), "%Y-%m-%d").timestamp()
        if recdate > maxRec:
            maxRec = recdate
    return datetime.fromtimestamp(maxRec).strftime("%m-%d-%Y")


def getWaterQualGeoJSON(records):
    """
    Processes water quality query results into a geojson Feature Collection.

    Parameters
    ----------
    records : List
        Nested lists containing SQL Alchemy query results:
            3 query result objects:
                waterQuality, waterqualityMD5 beaches
            1 string:
                geometry type of associated beach
            2 floats:
                x and y coordinates of the associated beach

    Returns
    -------
    featCollect : Geojson feature collection object
        Most recent water quality results per beach, one result per beach, as a geojson.

    """
    resultDict = {}
    for i, item in enumerate(records):
        # print(i.waterQuality.id, i.waterQuality.FecColi, i.waterQuality.beach_rel.BeachName, i.waterQuality.beach_rel.geom)
        # print(i.waterQuality.id, i.waterQuality.FecColi, i.waterQuality.beach_rel.BeachName)
        # print(item.waterQuality.beach_rel.BeachName, item.waterQuality.FecColi, test[i][-1], test[i][-2])
        beachName = (item.waterQuality.beach_rel.BeachName)
        resultDict[beachName] = {}
        resultDict[beachName]['FecColi'] = item.waterQuality.FecColi
        resultDict[beachName]['TotColi'] = item.waterQuality.TotColi
        resultDict[beachName]['Entero'] = item.waterQuality.Entero
        resultDict[beachName]['ExceedsRatio'] = item.waterQuality.ExceedsRatio
        resultDict[beachName]['BeachStatus'] = item.waterQuality.BeachStatus.rstrip()
        resultDict[beachName]['resample'] = item.waterQuality.resample.rstrip()
        # resultDict[beachName]['insDate'] = item.waterQuality.hash_rel.insdate.strftime("%Y-%m-%d")
        # resultDict[beachName]['pdfDate'] = item.waterQuality.hash_rel.pdfdate.strftime("%Y-%m-%d")
        resultDict[beachName]['insDate'] = item.waterQuality.hash_rel.insdate.strftime("%m-%d-%Y")
        resultDict[beachName]['pdfDate'] = item.waterQuality.hash_rel.pdfdate.strftime("%m-%d-%Y")
        resultDict[beachName]['GeomType'] = (records[i][-3]).split("ST_")[1]
        resultDict[beachName]['Lon'] = round(records[i][-2], 5)
        resultDict[beachName]['Lat'] = round(records[i][-1], 5)
        resultDict[beachName]['Name'] = item.waterQuality.beach_rel.BeachName.rstrip()
    featList = []
    for key in resultDict.keys():
        # Point takes items as long, lat Point must have (())
        beachPoint = Point((resultDict[key]['Lon'], resultDict[key]['Lat']))
        feature = Feature(geometry=beachPoint, properties=resultDict[key])
        featList.append(feature)

    featCollect = FeatureCollection(featList)
    return featCollect


def downloadPDF(url, pdfDest):
    """
    Downloads the water quality PDF with a new name, using the current date, and places it in a destionation folder.
    The source URL and PDF name do not change, they are updates with new content.
    :param url:
    :param pdfDest:
    :return:
    """
    # url = quote(url)
    urlretrieve(url, pdfDest)


def md5hash(text):
    """
    Generates a md5 hash of the text of the PDF, the text first has to be encoded. This will be used to see if
    the text within a PDF has been changed since the last time it was checked.
    :param text:
    :return:
    """
    return hashlib.md5(text.encode()).hexdigest()


def deletePDFQuit(pdfLoc):
    """
    Deletes pdf and ends the script
    :param pdfLoc:
    :return:
    """
    os.remove(pdfLoc)
    quit()


def handlePDFStatus(pdfStatus, pdfLoc, hashedText, pdfDict, pdfName):
    """

    Parameters
    ----------
    pdfStatus
    pdfLoc
    hashedText
    pdfDict
    pdfName

    Returns
    -------

    """
    if pdfStatus == "Exists":
        # print("Already processed this pdf, removing local pdf and quitting!")
        application.logger.debug("Already processed PDF, removing local PDF")
        try:
            os.remove(pdfLoc)
        except:
            # print("Failed to delete file!")
            application.logger.debug("Failed to remove local PDF")
        quit()
    else:
        try:
            GoogleDriveUploadWaterQuality.addtoGDrive(pdfLoc, pdfName)
            application.logger.debug("PDF uploaded to Google Drive")
        except Exception as e:
            # print("Google Drive upload threw an error, emailing exception")
            application.logger.debug("Google drive upload failed, trying to send email report")
            application.logger.debug(e)
            errorEmail.sendErrorEmail(script="addtoGDrive", exceptiontype=e.__class__.__name__, body=e)
        # print("Finished with local PDF, removing it from system")
        os.remove(pdfLoc)
    if checkResamp(pdfDict['cleanedtext']) == True:
        # print("This PDF contains re-sampled results")
        application.logger.debug("PDF contains re-sampled results, generating resample dict")
        beachDict = genReSampleDict(pdfDict['cleanedtext'], hashedText, pdfDict['pdfDate'])
    else:
        # Generate beach dictionary
        beachDict = genDict(pdfDict['pdfDate'])
        # Populate beach dictionary with results
        beachDict = populateDict(pdfDict['cleanedtext'], beachDict, "No")
        # If the new PDF contains updates but not re-sample data
        if pdfStatus == "Update":
            # print("This is a PDF filling in missing water quality results, with no re-sampling")
            application.logger.debug("PDF is updating missing water quality results, with no re-sampling")
            # Get the beaches with null values that are being updated
            application.logger.debug(f"Update PDF, getting null beaches with the date {pdfDict['pdfDate']}")
            nullBeaches = DBQueriesWaterQuality.getNullBeaches(pdfDict['pdfDate'])
            # Check if the key, beachname, is in the null beach list, if not delete it from the beach results dict
            # Delete any keys with None records for water quality, even if they were already null, its possible
            # that a updated PDF will not fill in all beaches
            for beachKey in list(beachDict.keys()):
                if (beachKey not in nullBeaches) or (beachDict[beachKey]['Total Coliform Results (MPN*)'] is None):
                    # del nullbeaches[beachkey]
                    # print(f"Removing {beachDict[beachkey]} key from the beach dictionary")
                    del beachDict[beachKey]
    # return beachDict
    # Get the md5 hash for the new pdf
    application.logger.debug("Getting hash id")
    # Mutate beachDict to replace empty strings with None values
    makeNull(beachDict)
    hashid = DBQueriesWaterQuality.insmd5(hashedText, pdfDict['pdfDate'], pdfName)
    application.logger.debug(f"Hash id is {hashid}, inserting into postgres")
    # Insert records into postgres, using the beachDict
    application.logger.debug(f"Beach dict being inserted is: {beachDict}")
    DBQueriesWaterQuality.insertWaterQual(beachDict, hashid)
    application.logger.debug("New water record has been inserted into postgres!")
    return beachDict


def cleanText(textList):
    """
    Normalizes the unicode text within the provided list, this is needed since the PDF conversion to text leads to
    some unicode characters being a combination of two unicode points, where we want a single value for ease of use.
    Items that are None are also converted to "Null" since the conversion sets some values to None for some reason.
    :param textList:
    :return:
    """
    text = []
    for item in textList:
        # print(f"item value is {item}")
        # item = convertValue(item)
        if item == '':
            item = None
        elif item == "<10":
            item = "0"
        elif item is not None:
            item = (unicodedata.normalize("NFKD", item).replace("\n", "").replace("‐", "-").replace(",", ""))
            if item == 'Results not available':
                item = None
        # print(f"cleaned item is {item}")
        text.append(item)
    return text


def genDict(pdfDate):
    """
    Generate a nested dictionary with beach names as keys at the upper level, and columns as keys at the
    nested level, values are set to '', except for the pdf date, so they can be filled in later.

    :param pdfDate:
    :return:
    """
    beachList = ['Carpinteria State Beach', 'Summerland Beach', 'Hammond\'s', 'Butterfly Beach',
                 'East Beach @ Sycamore Creek',
                 'East Beach @ Mission Creek', 'Leadbetter Beach', 'Arroyo Burro Beach', 'Hope Ranch Beach',
                 'Goleta Beach',
                 'Sands @ Coal Oil Point', 'El Capitan State Beach', 'Refugio State Beach', 'Guadalupe Dunes',
                 'Jalama Beach',
                 'Gaviota State Beach']
    beachFK = {'Carpinteria State Beach': 1, 'Summerland Beach': 2, 'Hammond\'s': 3, 'Butterfly Beach': 4,
               'East Beach @ Sycamore Creek': 5, 'East Beach @ Mission Creek': 6, 'Leadbetter Beach': 7,
               'Arroyo Burro Beach': 8, 'Hope Ranch Beach': 9, 'Goleta Beach': 10,
               'Sands @ Coal Oil Point': 11, 'El Capitan State Beach': 12, 'Refugio State Beach': 13,
               'Guadalupe Dunes': 14,
               'Jalama Beach': 15,
               'Gaviota State Beach': 16}
    col = ['Total Coliform Results (MPN*)', 'Total Coliform State Health Standard (MPN*)',
           "Fecal Coliform Results (MPN*)", 'Fecal Coliform State Health Standard (MPN*)',
           'Enterococcus Results (MPN*)',
           'Enterococcus State Health Standard (MPN*)', 'Exceeds FC:TC ratio standard **', 'Beach Status', 'fk']

    beachDict = {}
    for i in beachList:
        beachDict[i] = {}
        for c in col:
            beachDict[i][c] = ''
        beachDict[i]['Date'] = pdfDate
        beachDict[i]['fk'] = beachFK[i]
        beachDict[i]['resample'] = ''
    return beachDict


def convertValue(record):
    """

    :param record:
    :return:
    """
    if record == "<10":
        return "0"
    else:
        return record


def genReSampleDict(tab, hashedtext, pdfDate):
    """

    :param tab:
    :param hashedtext:
    :param pdfDate:
    :return:
    """
    application.logger.debug("Generating beach dictionary with resampled and data fill-ins")
    resampBeaches = []
    combinedBeaches = []
    resampTab = [tab[0]]
    newRecTab = [tab[0]]
    # Get list of null beaches
    nullBeaches = DBQueriesWaterQuality.getNullBeaches(pdfDate)
    application.logger.debug(f"Null beaches are {nullBeaches}")
    # Iterate over all records in the table
    for row in range(1, len(tab)):
        # Check each beach name, index 0 in the nested list, to see if it contains "sample", meaning it was resampled
        if "sample" in tab[row][0]:
            # print(f"Testing {tab[row][0]}")
            resampRow = tab[row]
            resampRow[0] = resampRow[0].split(' Re')[0].rstrip(" ")
            # print(f"Adding {resamprow[0]} to resample beach list")
            # Add to resample beach list
            resampBeaches.append(resampRow[0])
            # Add to resample table
            for item in resampRow[1:]:
                if " " in item:
                    resampRow[resampRow.index(item)] = item.split(" ")[0]
            resampTab.append(resampRow)
        elif tab[row][0] in nullBeaches and tab[row][1] is not None:
            # print("This re-sample PDF is also filling in missing data")
            # Add beach name to the combined beaches list
            application.logger.debug(f"Adding the following beach to the combined beaches list {tab[row][0]}")
            # print(f"Records to be appended are {tab[row]}")
            combinedBeaches.append(tab[row][0])
            # Add table row to the new records list
            newRecTab.append(tab[row])
    # Combine the beach names
    combinedBeaches = resampBeaches + combinedBeaches
    # print(f"Combined beach names list is {combinedbeaches}")
    # Use the beach names to generate a template dictionary
    combinedDict = genDict(combinedBeaches)
    # print(f"Template re-sample dictionary is {combinedDict}")
    # print(f"Re-sample table is {resampTab}")
    # Populate the dictionary with the re-sample data
    combinedDict = populateDict(resampTab, combinedDict, "Yes")
    # Populate the dictionary with the new record data
    combinedDict = populateDict(newRecTab, combinedDict, "No")
    return combinedDict


def checkResamp(tab):
    for sub_list in tab:
        if "sample" in sub_list[0]:
            return True


def getPDFContents(pdfLoc):
    """

    :param pdfLoc:
    :return:
    """
    pdfDict = {}
    with pdfplumber.open(pdfLoc) as pdf:
        p1 = pdf.pages[0]
        pdfDict['text'] = p1.extract_text()
        raw_tab = p1.extract_tables()[0]
        pdfDict['tab'] = raw_tab
    # pdfDate = cleanText([pdfDict['text'].split("Sample Results for the Week of: ")[1].split(" \nOpen")[0]])[0]

    pdfTitleList = pdfDict['text'].split("Sample Results for the Week of: ")[1].split(" ")
    dirtyTitle = f"{pdfTitleList[0]} {pdfTitleList[1]} {pdfTitleList[2]}"
    pdfDate = cleanText([dirtyTitle])[0]

    pdfDict['pdfDate'] = datetime.strptime(pdfDate, '%B %d %Y')
    cleanedtext = []
    for beachdetails in raw_tab:
        cleanedtext.append(cleanText(beachdetails))
    pdfDict['cleanedtext'] = cleanedtext
    return pdfDict


def populateDict(tab, beachDict, resample):
    """

    Parameters
    ----------
    tab
    beachDict
    resample

    Returns
    -------

    """
    col = ['Total Coliform Results (MPN*)', 'Total Coliform State Health Standard (MPN*)',
           "Fecal Coliform Results (MPN*)", 'Fecal Coliform State Health Standard (MPN*)',
           'Enterococcus Results (MPN*)',
           'Enterococcus State Health Standard (MPN*)', 'Exceeds FC:TC ratio standard **', 'Beach Status', 'fk']

    # Iterate over table skipping row one, which is column names, and use the row index number
    # print("Inside pop dict func")
    for row in range(1, len(tab)):
        # print(f"Working on row {tab[row]}")
        # For every row in the table, iterate over the columns, ignoring the first column(beach name),
        # since this is the key value. Use the column index to call on the column names list, which acts as a lookup
        # for the dictionary key value (column name) to be added to the 2nd level dictionary
        for i in range(1, (len(tab[row]))):
            # print(f"Filling key {beachDict[tab[row][0]][col[i-1]]} with value {tab[row][i]}")
            # col[i-1] is needed since the loop is starting at index 1 to avoid iterating over the beach name in the
            # original list (table), this index is needed to grab the proper column name(key) starting at index 0,
            # so its decreased by 1 to maintain proper index location for filling in data
            # beachDict[tab[row][0]][col[i-1]] = tab[row][i]
            if tab[row][i] is not None:
                beachDict[tab[row][0]][col[i - 1]] = tab[row][i].rstrip(" ")
            else:
                beachDict[tab[row][0]][col[i - 1]] = None
            beachDict[tab[row][0]]['resample'] = resample
    return beachDict


def parsePDF():
    """
    Kicks off process to parse water quality PDF.
    Returns
    -------
    Print Statement
    """
    # set PDF name
    pdfName = f"Ocean_Water_Quality_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdfLoc = pdfDest = os.path.join(app.root_path, 'static', 'documents', 'Water_Qual_PDFs', pdfName)
    downloadURL = "http://countyofsb.org/uploadedFiles/phd/PROGRAMS/EHS/Ocean%20Water%20Weekly%20Results.pdf"
    # Kick off script by downloading PDF
    application.logger.debug("Starting to parse PDF")
    downloadPDF(downloadURL, pdfDest)
    application.logger.debug("Downloaded PDF!")
    # Get pdf details
    pdfDict = getPDFContents(pdfLoc)
    application.logger.debug("PDF contents have been extracted")
    # Hash text of pdf document
    hashedText = md5hash(pdfDict['text'])
    # Check if md5 hash is already in postgres
    application.logger.debug("Checking PDF MD5 hash value against Postgres")
    pdfstatus = DBQueriesWaterQuality.checkmd5(hashedText, pdfDict['pdfDate'])
    application.logger.debug(f"PDF md5 has been checked, PDF status is {pdfstatus}")
    # Handle the results of the md5 hash check and control generation of dictionaries and interactions with postgres
    handlePDFStatus(pdfstatus, pdfLoc, hashedText, pdfDict, pdfName)
    application.logger.debug("All done processing PDF!")
    return pdfName



def pdfjob():
    """
    Function called by APScheduler BackgroundScheduler to kick off PDF parsing script.
    Uses try/except block to call function. This is done because quit() is called within the script as flow control
    to end it early, if this exception is not caught then an exception is raised, while the script will continue to
    run on schedule, it will pollute logs with tracebacks.

    Returns
    -------
    Nothing
    """

    application.logger.debug("PDF job issued, downloading and parsing PDF")
    try:
        pdfName = parsePDF()
        errorEmail.sendSuccessEmail(script="parsePDF", body=f"The PDF: {pdfName} was successfully processed!")
        application.logger.debug("Successfully parsed a new PDF!")
    except SystemExit:
        logger.debug("Ended ParsePDF early since file has already been processed")
        application.logger.debug("Ended ParsePDF job early")
    except Exception as e:
        # print("Parse PDF threw an error, emailing exception")
        application.logger.error("Parse PDF threw an error")
        application.logger.error(e)
        try:
            errorEmail.sendErrorEmail(script="ParsePDF", exceptiontype=e.__class__.__name__, body=e)
        except Exception as f:
            application.logger.error("Failed to send error email")
            application.logger.error(e)
