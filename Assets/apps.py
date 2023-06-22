from django.apps import AppConfig
import boto3, botocore
from django.conf import settings


class AssetsConfig(AppConfig):
    name = 'Assets'
    s3=boto3.client(
        's3',
        aws_access_key_id=settings.S3_KEY,
        aws_secret_access_key=settings.S3_SECRET
    )
