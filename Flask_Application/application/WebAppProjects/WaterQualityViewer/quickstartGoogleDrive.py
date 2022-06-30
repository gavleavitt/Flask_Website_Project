from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authorize Google Account with machine
# Call this function from remote connection to server to authorize my account

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)