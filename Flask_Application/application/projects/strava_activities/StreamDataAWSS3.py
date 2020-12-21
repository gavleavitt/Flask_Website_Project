import os
import boto3
from botocore.exceptions import ClientError
import logging
# Open boto3 session


# def connectToS3():
#     session = boto3.session(aws_access_key_id=os.getenv("BOTO3_Flask_ID"),
#                             aws_secret_access_key=os.getenv("BOTO3_Flask_KEY"))
#     s3Con = session.resource('s3')
#     return s3Con

def create_presigned_url(object_name, expiration=300):
    """Generate a presigned URL to share an S3 object

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    print("Generating temp access URL")
    s3_client = boto3.client(service_name='s3',
                             aws_access_key_id=os.getenv("BOTO3_Flask_ID"),
                             aws_secret_access_key=os.getenv("BOTO3_Flask_KEY"))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.getenv("S3_STREAM_BUCKET"),
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print("Error!")
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response