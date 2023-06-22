from Assets.apps import AssetsConfig
from django.conf import settings
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework import status

def upload_to_s3(file,object_key):
    s3=AssetsConfig.s3
    try:
        s3.upload_fileobj(
            file,
            settings.S3_BUCKET,
            object_key
        )
        return True
    except Exception as e:
        return False
    

def extract_object_key(url):
    url = url.replace('https://', '')
    object_key = url[url.index('/') + 1:]

    return object_key

def delete_from_s3(asset_url):
    s3=AssetsConfig.s3
    object_key=extract_object_key(asset_url)
    response = s3.delete_object(
        Bucket=settings.S3_BUCKET,
        Key=object_key
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        return True
    else:
        return False