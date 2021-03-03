import os
import boto3
from botocore.exceptions import ClientError
import logging
from io import StringIO
import csv
from application import application, errorEmail

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

    try:
        if fileID == "activitiesTopoJSON":
            fileName = "topoJSONPublicActivities.json"
        else:
            fileName = f"stream_{fileID}.csv"
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.getenv("S3_STREAM_BUCKET"),
                                                            'Key': fileName},
                                                    ExpiresIn=expiration)
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
    # Create in-memory text buffer
    memOutput = StringIO()
    dataDict = {}
    # Exclude latlng from CSV, these data will be shared to the public
    csvTypes = ['time', 'altitude', 'velocity_smooth', 'grade_smooth', "distance", "heartrate", "cadence", "temp"]
    # Extract data from stream dictionary
    for streamType in csvTypes:
        dataDict[streamType] = streamData[streamType].data
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

    :param memCSV:
    :param actID:
    :return:
    """

    bucket = os.getenv("S3_STREAM_BUCKET")
    conn = connectToS3()

    try:
        # Add in-memory buffer csv to bucket
        # I think using getvalue and put_object on StringIO solves an issue with the StringIO object not being
        # compatible with other boto3 object creation methods see:
        # https://stackoverflow.com/a/45700716
        # https://stackoverflow.com/a/60293770
        # conn.put_object(Body=memCSV.getvalue(), Bucket=bucket, Key=fileName, ContentType='application/vnd.ms-excel')
        if actID:
            fileName = f"stream_{actID}.csv"
            conn.put_object(Body=file.getvalue(), Bucket=bucket, Key=fileName)
        else:
            fileName = "topoJSONPublicActivities.json"
            conn.put_object(Body=file, Bucket=bucket, Key=fileName)
    except Exception as e:
        application.logger.error(f"Upload to S3 bucket failed in the error: {e}")
        errorEmail.sendErrorEmail(script="UploadToS3Bucket", exceptiontype=e.__class__.__name__, body=e)
    finally:
        pass
        # Close in-memory buffer file, removing it from memory
        # file.close()