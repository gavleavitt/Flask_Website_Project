# open_pdf = PyPDF3.PdfFileReader(pdf_loc, 'rb')
# p1 = open_pdf.getPage(0)
# p1_text = p1.extractText()
# import pandas as pd
import pdfplumber
import unicodedata
from datetime import datetime
import hashlib
from urllib.parse import quote
from urllib.request import urlretrieve
from application import app, errorEmail, GoogleDrive, application
from application import DB_Queries_PDF as DBQ_PDF
import os
from application import logger

beachList = ['Carpinteria State Beach', 'Summerland Beach', 'Hammond\'s', 'Butterfly Beach',
             'East Beach @ Sycamore Creek',
             'East Beach @ Mission Creek', 'Leadbetter Beach', 'Arroyo Burro Beach', 'Hope Ranch Beach', 'Goleta Beach',
             'Sands @ Coal Oil Point', 'El Capitan State Beach', 'Refugio State Beach', 'Guadalupe Dunes',
             'Jalama Beach',
             'Gaviota State Beach']
beachfk = {'Carpinteria State Beach': 1, 'Summerland Beach': 2, 'Hammond\'s': 3, 'Butterfly Beach': 4,
           'East Beach @ Sycamore Creek': 5, 'East Beach @ Mission Creek': 6, 'Leadbetter Beach': 7,
           'Arroyo Burro Beach': 8, 'Hope Ranch Beach': 9, 'Goleta Beach': 10,
           'Sands @ Coal Oil Point': 11, 'El Capitan State Beach': 12, 'Refugio State Beach': 13, 'Guadalupe Dunes': 14,
           'Jalama Beach': 15,
           'Gaviota State Beach': 16}
col = ['Total Coliform Results (MPN*)', 'Total Coliform State Health Standard (MPN*)',
       "Fecal Coliform Results (MPN*)", 'Fecal Coliform State Health Standard (MPN*)', 'Enterococcus Results (MPN*)',
       'Enterococcus State Health Standard (MPN*)', 'Exceeds FC:TC ratio standard **', 'Beach Status', 'fk']
resampcol = ['Total Coliform Results (MPN*)', "Fecal Coliform Results (MPN*)", 'Enterococcus Results (MPN*)']
resampdict = {}


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


def pdfUpdate():
    """

    :return:
    """
    pass


def handlePDFStatus(pdfstatus, pdfLoc, hashedtext, pdfDict, pdfName, currentTime, beachList):
    if pdfstatus == "Exists":
        print("Already processed this pdf, removing local pdf and quitting!")
        application.logger.debug("Already processed PDF, removing local PDF")
        try:
            os.remove(pdfLoc)
        except:
            print("Failed to delete file!")
            application.logger.debug("Failed to remove local PDF")
        quit()
    else:
        try:
            GoogleDrive.addtoGDrive(pdfLoc, pdfName)
        except Exception as e:
            print("Google Drive upload threw an error, emailing exception")
            application.logger.debug("Google drive upload failed, trying to send email report")
            application.logger.debug(e)
            errorEmail.senderroremail(script="addtoGDrive", exceptiontype=e.__class__.__name__, body=e)
        print("File uploaded to Google Drive, removing local PDF")
        os.remove(pdfLoc)
    if checkresamp(pdfDict['cleanedtext']) == True:
        print("This PDF contains re-sampled results")
        beachDict = genReSampleDict(pdfDict['cleanedtext'], hashedtext, pdfDict['pdfDate'])
    else:
        # Generate beach dictionary
        beachDict = genDict(beachList, pdfDict['pdfDate'])
        # Populate beach dictionary with results
        beachDict = populateDict(pdfDict['cleanedtext'], beachDict, "No")
        # If the new PDF contains updates but not re-sample data
        if pdfstatus == "Update":
            print("This is a PDF filling in missing water quality results, with no re-sampling")
            # Get the beaches with null values that are being updated
            nullbeaches = DBQ_PDF.getNullBeaches(pdfDict['pdfDate'])
            # Check if the key, beachname, is in the null beach list, if not delete it from the beach results dict
            # Delete any keys with None records for water quality, even if they were already null, its possible
            # that a updated PDF will not fill in all beaches
            for beachkey in list(beachDict.keys()):
                if (beachkey not in nullbeaches) or (beachDict[beachkey]['Total Coliform Results (MPN*)'] is None):
                    # del nullbeaches[beachkey]
                    # print(f"Removing {beachDict[beachkey]} key from the beach dictionary")
                    del beachDict[beachkey]
    # return beachDict
    # Get the md5 hash for the new pdf
    hashid = DBQ_PDF.insmd5(hashedtext, pdfDict['pdfDate'], pdfName, currentTime)
    # Insert records into postgres, using the beachDict
    DBQ_PDF.insertWaterQual(beachDict, hashid)
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


def genDict(beachList, pdfDate):
    """
    Generate a nested dictionary with beach names as keys at the upper level, and columns as keys at the
    nested level, values are set to '', except for the pdf date, so they can be filled in later.

    :param pdfDate:
    :return:
    """
    print(f"Generating dictionary using the beachList:{beachList}")
    beachDict = {}
    for i in beachList:
        beachDict[i] = {}
        for c in col:
            beachDict[i][c] = ''
        beachDict[i]['Date'] = pdfDate
        beachDict[i]['fk'] = beachfk[i]
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
    print("Generating beach dictionary with resampled and data fill-ins")
    resampbeaches = []
    combinedbeaches = []
    resampTab = [tab[0]]
    newRecTab = [tab[0]]
    # Get list of null beaches
    nullbeaches = DBQ_PDF.getNullBeaches(pdfDate)
    print(f"Null beaches are {nullbeaches}")
    # Iterate over all records in the table
    for row in range(1, len(tab)):
        # Check each beach name, index 0 in the nested list, to see if it contains "sample", meaning it was resampled
        if "sample" in tab[row][0]:
            # print(f"Testing {tab[row][0]}")
            resamprow = tab[row]
            resamprow[0] = resamprow[0].split(' Re')[0].rstrip(" ")
            # print(f"Adding {resamprow[0]} to resample beach list")
            # Add to resample beach list
            resampbeaches.append(resamprow[0])
            # Add to resample table
            for item in resamprow[1:]:
                if " " in item:
                    resamprow[resamprow.index(item)] = item.split(" ")[0]
            resampTab.append(resamprow)
        elif tab[row][0] in nullbeaches and tab[row][1] is not None:
            # print("This re-sample PDF is also filling in missing data")
            # Add beach name to the combined beaches list
            print(f"Adding the following beach to the combined beaches list {tab[row][0]} ")
            # print(f"Records to be appended are {tab[row]}")
            combinedbeaches.append(tab[row][0])
            # Add table row to the new records list
            newRecTab.append(tab[row])
    # Combine the beach names
    combinedbeaches = resampbeaches + combinedbeaches
    # print(f"Combined beach names list is {combinedbeaches}")
    # Use the beach names to generate a template dictionary
    combinedDict = genDict(combinedbeaches, pdfDate)
    # print(f"Template re-sample dictionary is {combinedDict}")
    # print(f"Re-sample table is {resampTab}")
    # Populate the dictionary with the re-sample data
    combinedDict = populateDict(resampTab, combinedDict, "Yes")
    # Populate the dictionary with the new record data
    combinedDict = populateDict(newRecTab, combinedDict, "No")

    return combinedDict


def checkresamp(tab):
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
    pdfDate = cleanText([pdfDict['text'].split("Sample Results for the Week of: ")[1].split(" \nOpen")[0]])[0]
    pdfDict['pdfDate'] = datetime.strptime(pdfDate, '%B %d %Y')
    cleanedtext = []
    for beachdetails in raw_tab:
        cleanedtext.append(cleanText(beachdetails))
    pdfDict['cleanedtext'] = cleanedtext
    return pdfDict


def populateDict(tab, beachDict, resample):
    """
    Table comes in as a list of lists.
    :param tab:
    :param pdfDate:
    :return:
    """
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
    Kicks off process to parse the water quality PDF.
    Returns
    -------
    Print Statement
    """
    # Kick off script by downloading PDF
    print("Starting to parse PDF")
    downloadPDF(downloadURL, pdfDest)
    # Get pdf details
    pdfDict = getPDFContents(pdfLoc)
    # Hash text of pdf document
    hashedtext = md5hash(pdfDict['text'])
    # Check if md5 hash is already in postgres
    pdfstatus = DBQ_PDF.checkmd5(hashedtext, pdfDict['pdfDate'])
    # Handle the results of the md5 hash check and control generation of dictionaries and interactions with postgres
    # handlePDFStatus(pdfstatus, pdfLoc, hashedtext, pdfDict, pdfName, currentTime, beachList)
    currentTime = datetime.now()
    handlePDFStatus(pdfstatus, pdfLoc, hashedtext, pdfDict, pdfName, currentTime, beachList)
    print("All done processing PDF!")

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
        parsePDF()
        logger.debug("Successfully parsed a new PDF!")
    except SystemExit:
        logger.debug("Ended ParsePDF early since file has already been processed")
        print("Ended ParsePDF job early")
    except Exception as e:
        print("Parse PDF threw an error, emailing exception")
        application.logger.error("Parse PDF threw an error")
        application.logger.error(e)
        errorEmail.senderroremail(script="ParsePDF", exceptiontype=e.__class__.__name__, body=e)





pdfName = f"Ocean_Water_Quality_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
#  pdfLoc = pdfDest = r"G:\My Drive\Projects\Water_Quality\pdf" + pdfName
pdfLoc = pdfDest = os.path.join(app.root_path, 'static', 'documents', 'Water_Qual_PDFs', pdfName)
downloadURL = "http://countyofsb.org/uploadedFiles/phd/PROGRAMS/EHS/Ocean%20Water%20Weekly%20Results.pdf"


# Testing variables
# pdfName = r"Ocean_Water_Quality_Report_20200814.pdf"
# pdfLoc = r"G:\My Drive\Projects\Water_Quality\pdf\\" + pdfName

# # Kick off script by downloading PDF
# downloadPDF(downloadURL, pdfDest)
# # Get pdf details
# pdfDict = getPDFContents(pdfLoc)
# # Hash text of pdf document
# hashedtext = md5hash(pdfDict['text'])
# # Check if md5 hash is already in postgres
# pdfstatus = DBQ_PDF.checkmd5(hashedtext, pdfDict['pdfDate'])
# # Handle the results of the md5 hash check and control generation of dictionaries and interactions with postgres
# #handlePDFStatus(pdfstatus, pdfLoc, hashedtext, pdfDict, pdfName, currentTime, beachList)
# handlePDF = handlePDFStatus(pdfstatus, pdfLoc, hashedtext, pdfDict, pdfName, currentTime, beachList)
# print("All done processing PDF!")
