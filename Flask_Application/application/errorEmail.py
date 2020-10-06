import smtplib, ssl, os, email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from application import logger

port = 465  # For SSL
# Get email settings from environmental variables
emailpassword = os.environ.get("EMAILPASS")
emailaddr = os.environ.get("EMAILADDR")
emailtoaddr = os.environ.get("EMAILTOADDR")

def senderroremail(script, exceptiontype, body):
    """
    Called from try/except blocks, sends an email over smtp with exception details. Sender and receiver details are
    pulled from environmental variables.
    Parameters
    ----------
    script: String. Name of function/script that threw the exception, manually inputted in the function call.
    exceptiontype: String. Type of exception thrown.
    body: String. Full traceback thrown by exception.

    Returns
    -------
    Print statement.
    """
    try:
        logger.debug("Trying to send error email")
        # Create a secure SSL context
        context = ssl.create_default_context()
        # create connection to gmail smtplib server
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            # login to server
            server.login(emailaddr, emailpassword)
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["from"] = emailaddr
            message["To"] = emailtoaddr
            message["Subject"] = f"The Python script {script} raised an {exceptiontype} exception"
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            # Send email
            server.sendmail(emailaddr, emailtoaddr, message.as_string())
            # print("Message has been sent!")
    except Exception as e:
        logger.debug("Failed to send error email")
        logger.error(e)
        # print("The following exception was thrown when trying to email error report")
        # print(e)