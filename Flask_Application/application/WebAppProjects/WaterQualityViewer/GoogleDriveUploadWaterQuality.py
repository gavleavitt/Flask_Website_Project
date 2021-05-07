from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from application import app, errorEmail, application

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
        application.logger.debug("Attempting to authenticate with Google Drive API through saved OAuth  credentials")
        # Change location for client_secrets.json, application.py sits one level above this file and the file isn't
        # called properly when this function is called, but the file needs to stay in that location such that
        # quickstart.py can be called directly if needed
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(app.root_path, 'WebAppProjects', 'WaterQualityViewer',
                                                                         'credentials.json')
        # Use command line to auth, must connect to host, visit URL, login/auth with Google, then paste provided text
        # into terminal
        # gauth.CommandLineAuth()

        # Create authenticated GoogleDrive instance using settings from the setting.yaml file to auto-authenticate with
        # saved credentials
        gauth = GoogleAuth(settings_file=os.path.join(app.root_path, 'WebAppProjects', 'WaterQualityViewer', 'settings.yaml'))

        # Establish connection with Google Drive API
        drive = GoogleDrive(gauth)
        application.logger.debug("Connected to Google Drive account")
        # Create a new GoogleDriveFile instance with a PDF mimetype in the water quality PDF folder using the parent folder's ID
        newfile = drive.CreateFile({"title": pdfname,
                                    'mimeType': 'application/pdf',
                                    'parents': [{'id': "1GRunRWB7SKmH3I0wWbtyJ_UOCDiHGAxO"}]})
        # Read file and set the content of the new file instance
        newfile.SetContentFile(pdfloc)
        # Upload the file to Google Drive
        newfile.Upload()
        # print("File uploaded to Google Drive!")
        application.logger.debug(f"File {pdfname} uploaded to Google Drive!")
    except Exception as e:
        print("GoogleDrive upload threw an error, emailing exception")
        application.logger.error("Failed to upload to Google Drive account")
        application.logger.error(e)
        errorEmail.sendErrorEmail(script="GoogleDrive", exceptiontype=e.__class__.__name__, body=e)


# testing
# pdfloc = r"G:\My Drive\Projects\test_documents\Ocean_Water_Quality_Report_testing_20201002.pdf"
# pdfname = r"Ocean_Water_Quality_Report_testing_20201002.pdf"
#
# addtoGDrive(pdfloc, pdfname)