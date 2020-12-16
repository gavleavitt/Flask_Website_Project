import os
import boto3

# Open boto3 session
session = boto3.session(aws_access_key_id=os.getenv("BOTO3_Flask_ID"),aws_secret_access_key=os.getenv("BOTO3_Flask_KEY"))
s3Con = session.resource('s3')