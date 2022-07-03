import os
import boto3
from botocore.exceptions import ClientError
import logging
from io import StringIO
import csv
import logging
# from flask_application import flask_application
# from flask_application.util.ErrorEmail import errorEmail
from ErrorEmail import errorEmail

def setupLogging():
    logging.basicConfig(filename="Boto3.log", level=logging.DEBUG)

def connectToS3():
    """
    Establish connection to AWS S3 using environmental variables.

    :return: S3 service client.
    """
    s3_client = boto3.client(service_name='s3',
                             aws_access_key_id=os.getenv("BOTO3_Flask_ID"),
                             aws_secret_access_key=os.getenv("BOTO3_Flask_KEY"))
    return s3_client

def create_presigned_url(fileID, expiration=300):
    """Generate a presigned URL to share an S3 object

    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    # print("Generating temp access URL")
    s3_client = connectToS3()
    setupLogging()
    try:
        if fileID == "activitiesTopoJSON":
            fileName = "topoJSONPublicActivities.json"
        else:
            fileName = f"stream_{fileID}.csv"
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.getenv("S3_TRIMMED_STREAM_BUCKET"),
                                                            'Key': fileName},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

def get_presigned_url(fileID, bucket, expiration=300):
    """Generate a presigned URL to share an S3 object

    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    # print("Generating temp access URL")
    s3_client = connectToS3()
    setupLogging()
    try:
        if fileID:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket,
                                                                'Key': fileID},
                                                        ExpiresIn=expiration)
        else:
            return None
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

def writeMemoryCSV(streamData):
    """
    Converts activity stream data dictionary to a In-memory text buffer, avoids needing to write a local file since data
    will be uploaded up to S3.

    :param streamData: Dict. Formatted Strava Stream Data with lat/longs removed
    :return: In-memory text buffer. Activity stream CSV
    """
    setupLogging()
    # Create in-memory text buffer
    memOutput = StringIO()
    dataDict = {}
    # stream types to include, latlngs in privacy zones will be removed
    csvTypes =  ['time', 'latlng', 'altitude', 'velocity_smooth', 'grade_smooth', "distance", "heartrate", "cadence", "temp"]
    # Extract data from stream dictionary
    for streamType in csvTypes:
        try:
            dataDict[streamType] = streamData[streamType].data
        except:
            logging.debug(f"The stream type {streamType} doesn't exist, skipping")
    # Iterate over latlngs, which is a list with lat lng, converting to string of lat,lng
    for c, i in enumerate(dataDict['latlng']):
        dataDict['latlng'][c] = ",".join(str(x) for x in i)
    # See: https://stackoverflow.com/questions/23613426/write-dictionary-of-lists-to-a-csv-file
    # open buffer and populate with csv data
    writer = csv.writer(memOutput)
    # Write column names
    writer.writerow(dataDict.keys())
    # Each key:value(list) in dictionary is a column, write into CSV
    # I have no idea how this works, see link above for description
    writer.writerows(zip(*dataDict.values()))
    return memOutput

def uploadToS3(file, actID=None):
    """
    Uploads file to S3 Bucket. This bucket is not public but all activities are accessible to the public through the API
    with pre-signed temporary URLs. If the Act ID is none then the input is the TopoJSON file.

    :param file: Buffer/memory file to be uploaded, either JSON or CSV.
    :param actID: Strava Activity ID, used to name uploaded file, if empty then TopoJSON is assumed, which has a static
    name
    :return:
    Nothing, file is uploaded
    """

    # Get bucket details from environmental variable
    bucket = os.getenv("S3_TRIMMED_STREAM_BUCKET")
    # Establish connection to S3 API
    conn = connectToS3()
    setupLogging()
    try:
        # conn.put_object(Body=memCSV.getvalue(), Bucket=bucket, Key=fileName, ContentType='flask_application/vnd.ms-excel')
        if actID:
            # Add in-memory buffer csv to bucket
            # I think using getvalue and put_object on StringIO solves an issue with the StringIO object not being
            # compatible with other boto3 object creation methods see:
            # https://stackoverflow.com/a/45700716
            # https://stackoverflow.com/a/60293770
            fileName = f"stream_{actID}.csv"
            conn.put_object(Body=file.getvalue(), Bucket=bucket, Key=fileName)
            logging.debug(f"CSV {fileName} has been added to S3 Bucket {bucket}")
        else:
            # Add in-memory buffer TopoJSON file to bucket, file name is static
            fileName = "topoJSONPublicActivities.json"
            conn.put_object(Body=file, Bucket=bucket, Key=fileName)
    except Exception as e:
        logging.error(f"Upload to S3 bucket failed in the error: {e}")
        errorEmail.sendErrorEmail(script="UploadToS3Bucket", exceptiontype=e.__class__.__name__, body=e)

    # finally:
    #     # Close in-memory buffer file, removing it from memory
    #     file.close()

def deleteFromS3(bucket, filetype, actID):
    """
    Deletes existing file from S3 Bucket.

    @param bucket: String. S3 Bucket name.
    @param fileName: String. Filename of bucket object
    @return: Nothing.
    """
    # Establish connection to S3 API
    conn = connectToS3()
    if filetype == "trimmedCSV":
        # Create file name from ID
        fileName = f"stream_{actID}.csv"
        # Issue command to delete object
        conn.delete_object(Bucket=bucket, Key=fileName)
    else:
        pass