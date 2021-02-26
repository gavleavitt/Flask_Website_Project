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
                             aws_access_key_id=os.environ.get("BOTO3_Flask_ID"),
                             aws_secret_access_key=os.environ.get("BOTO3_Flask_KEY"))
    return s3_client

def create_presigned_url(fileName, expiration=900):
    """Generate a presigned URL to share an S3 object

    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    # print("Generating temp access URL")
    s3_client = connectToS3()
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.getenv("S3_WATERQUALPDF_BUCKET"),
                                                            'Key': fileName.rstrip()},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print("Error!")
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def uploadToS3(fileName, filePath):
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
        conn.put_object(Body=filePath.getvalue(), Bucket=bucket, Key=fileName)
    except Exception as e:
        application.logger.error(f"Upload water quality to S3 bucket failed in the error: {e}")
        errorEmail.sendErrorEmail(script="UploadWaterQualityToS3Bucket", exceptiontype=e.__class__.__name__, body=e)
    finally:
        pass
        # Close in-memory buffer file, removing it from memory
        # filePath.close()