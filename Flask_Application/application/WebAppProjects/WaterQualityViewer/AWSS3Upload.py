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
    """

    bucket = os.getenv("S3_WATERQUALPDF_BUCKET")
    conn = connectToS3()

    try:
        application.logger.debug(f"Uploading PDF {fileName} located at {filePath} to AWS S3")
        # conn.put_object(Body=filePath, Bucket=bucket, Key=fileName, ContentType="application/pdf")
        conn.upload_file(Filename=filePath, Bucket=bucket, Key=fileName)
        application.logger.debug(f"PDF {fileName} has been uploaded to AWS S3")
    except Exception as e:
        application.logger.error(f"Upload water quality to S3 bucket failed in the error: {e}")
        errorEmail.sendErrorEmail(script="UploadWaterQualityToS3Bucket", exceptiontype=e.__class__.__name__, body=e)