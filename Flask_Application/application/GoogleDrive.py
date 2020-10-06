from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from application import app, errorEmail
from application import logger

def addtoGDrive(pdfloc, pdfname):
    """

    Uploads water quality PDF file to Google drive account under My Drive\Projects\Water_Quality\pdf location,
    id:1GRunRWB7SKmH3I0wWbtyJ_UOCDiHGAxO

    Parameters
    ----------
    pdfloc: String. Location of PDF to uploaded with filename
    pdfname: String. Filename of PDF to upload, uploaded this with name.

    Returns
    -------
    Print statement
    """
    try:
        # Change location for client_secrets.json, application.py sits one level above this file and the file isnt
        # called properly when this function is called, but the file needs to stay in that location such that
        # quickstart.py can be called directly in the server's terminal
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(app.root_path, 'client_secrets.json')
        # Authenticate with OAuth, , must visit URL and input value.
        gauth = GoogleAuth(settings_file=os.path.join(app.root_path, 'settings.yaml'))
        # Use command line to auth, must connect to host, visit URL, login/auth with Google, then paste provided text into
        # terminal
        # gauth.CommandLineAuth()
        # Establish connection with Google Drive API
        drive = GoogleDrive(gauth)
        newfile = drive.CreateFile({"title": pdfname,
                                    'mimeType': 'application/pdf',
                                    'parents': [{'id': "1GRunRWB7SKmH3I0wWbtyJ_UOCDiHGAxO"}]})
        newfile.SetContentFile(pdfloc)
        newfile.Upload()
        print("File uploaded to Google Drive!")
        logger.debug(f"File {pdfname} uploaded to Google Drive!")
    except Exception as e:
        print("GoogleDrive upload threw an error, emailing exception")
        logger.error("Failed to upload to Google Drive account")
        logger.error(e)
        errorEmail.senderroremail(script="GoogleDrive", exceptiontype=e.__class__.__name__, body=e)


# testing
# pdfloc = r"G:\My Drive\Projects\test_documents\Ocean_Water_Quality_Report_testing_20201002.pdf"
# pdfname = r"Ocean_Water_Quality_Report_testing_20201002.pdf"
#
# addtoGDrive(pdfloc, pdfname)